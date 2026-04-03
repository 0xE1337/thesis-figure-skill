#!/usr/bin/env python3
r"""
TikZ 路径规划器 — 自动计算避障正交路径
用法: python3 tikz-path-router.py <routing-spec.json>

输入 JSON 格式:
{
  "nodes": [
    {"name": "A", "x": 2.0, "y": 10.0, "width": 3.0, "height": 1.2},
    {"name": "B", "x": 8.0, "y": 5.0,  "width": 2.5, "height": 1.0}
  ],
  "connections": [
    {"from": "A", "from_anchor": "south", "to": "B", "to_anchor": "north",
     "style": "arrow", "label": "数据流"}
  ],
  "grid_resolution": 0.1
}

输出: 每条连线的 TikZ \draw 代码（含避障拐点坐标）
"""

import json
import sys
import math

try:
    from pathfinding.core.grid import Grid
    from pathfinding.finder.a_star import AStarFinder
except ImportError:
    print("ERROR: pathfinding 未安装。运行: pip3 install pathfinding")
    sys.exit(1)


# ─── 数据结构 ───

class Node:
    def __init__(self, name, x, y, width, height):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def left(self):
        return self.x - self.width / 2

    @property
    def right(self):
        return self.x + self.width / 2

    @property
    def top(self):
        return self.y + self.height / 2

    @property
    def bottom(self):
        return self.y - self.height / 2

    def anchor_pos(self, anchor):
        """Get (x, y) for a named anchor."""
        anchors = {
            "north": (self.x, self.top),
            "south": (self.x, self.bottom),
            "east": (self.right, self.y),
            "west": (self.left, self.y),
            "north east": (self.right, self.top),
            "north west": (self.left, self.top),
            "south east": (self.right, self.bottom),
            "south west": (self.left, self.bottom),
            "center": (self.x, self.y),
        }
        return anchors.get(anchor, (self.x, self.y))


class Connection:
    def __init__(self, from_node, from_anchor, to_node, to_anchor,
                 style="arrow", label=""):
        self.from_node = from_node
        self.from_anchor = from_anchor
        self.to_node = to_node
        self.to_anchor = to_anchor
        self.style = style
        self.label = label


# ─── 网格构建 ───

def build_grid(nodes, resolution, padding=1.0):
    """Build a 2D grid with node rectangles as obstacles."""
    # Find bounding box of all nodes
    all_left = min(n.left for n in nodes) - padding
    all_right = max(n.right for n in nodes) + padding
    all_bottom = min(n.bottom for n in nodes) - padding
    all_top = max(n.top for n in nodes) + padding

    # Grid dimensions
    cols = int(math.ceil((all_right - all_left) / resolution)) + 1
    rows = int(math.ceil((all_top - all_bottom) / resolution)) + 1

    # Cap grid size to prevent memory issues
    if cols * rows > 500000:
        # Increase resolution to fit
        area = (all_right - all_left) * (all_top - all_bottom)
        resolution = math.sqrt(area / 250000)
        cols = int(math.ceil((all_right - all_left) / resolution)) + 1
        rows = int(math.ceil((all_top - all_bottom) / resolution)) + 1

    # Initialize grid (1 = walkable)
    matrix = [[1] * cols for _ in range(rows)]

    # Mark node rectangles as obstacles (0 = blocked)
    # Buffer ensures paths keep visible distance from box borders
    buffer = 0.8  # cm — paths will stay ≥0.8cm from any box edge
    for node in nodes:
        c_min = max(0, int((node.left - buffer - all_left) / resolution))
        c_max = min(cols - 1, int((node.right + buffer - all_left) / resolution))
        # TikZ y increases upward, but grid row 0 is top
        # We'll invert: grid_row = rows - 1 - tikz_row
        r_min = max(0, int((node.bottom - buffer - all_bottom) / resolution))
        r_max = min(rows - 1, int((node.top + buffer - all_bottom) / resolution))
        for r in range(r_min, r_max + 1):
            for c in range(c_min, c_max + 1):
                # Invert row for grid (grid y=0 is top)
                gr = rows - 1 - r
                if 0 <= gr < rows:
                    matrix[gr][c] = 0

    return matrix, all_left, all_bottom, resolution, rows, cols


def tikz_to_grid(x, y, origin_x, origin_y, resolution, rows):
    """Convert TikZ coordinates to grid (col, row)."""
    col = int(round((x - origin_x) / resolution))
    row_from_bottom = int(round((y - origin_y) / resolution))
    row = rows - 1 - row_from_bottom  # invert for grid
    return col, row


def grid_to_tikz(col, row, origin_x, origin_y, resolution, rows):
    """Convert grid (col, row) back to TikZ coordinates."""
    x = origin_x + col * resolution
    row_from_bottom = rows - 1 - row
    y = origin_y + row_from_bottom * resolution
    return x, y


# ─── 路径简化 ───

def simplify_path(points):
    """Remove collinear points, keep only turn points."""
    if len(points) <= 2:
        return points

    simplified = [points[0]]
    for i in range(1, len(points) - 1):
        prev = simplified[-1]
        curr = points[i]
        next_pt = points[i + 1]

        # Check if direction changes
        dx1 = curr[0] - prev[0]
        dy1 = curr[1] - prev[1]
        dx2 = next_pt[0] - curr[0]
        dy2 = next_pt[1] - curr[1]

        # Normalize directions to signs
        s1 = (1 if dx1 > 0 else (-1 if dx1 < 0 else 0),
              1 if dy1 > 0 else (-1 if dy1 < 0 else 0))
        s2 = (1 if dx2 > 0 else (-1 if dx2 < 0 else 0),
              1 if dy2 > 0 else (-1 if dy2 < 0 else 0))

        if s1 != s2:
            simplified.append(curr)

    simplified.append(points[-1])
    return simplified


def snap_to_orthogonal(points):
    """Ensure all segments are strictly horizontal or vertical."""
    if len(points) <= 1:
        return points

    snapped = [points[0]]
    for i in range(1, len(points)):
        prev = snapped[-1]
        curr = points[i]
        dx = abs(curr[0] - prev[0])
        dy = abs(curr[1] - prev[1])

        if dx < 0.05:  # nearly vertical
            snapped.append((prev[0], curr[1]))
        elif dy < 0.05:  # nearly horizontal
            snapped.append((curr[0], prev[1]))
        else:
            # Need to insert an intermediate point (L-shape)
            # Prefer: go horizontal first, then vertical
            snapped.append((curr[0], prev[1]))
            snapped.append(curr)

    return snapped


# ─── 路由 ───

def route_connection(conn, nodes, matrix, origin_x, origin_y,
                     resolution, rows, cols):
    """Route a single connection, returning TikZ coordinate path."""
    # Get start/end positions
    start_x, start_y = conn.from_node.anchor_pos(conn.from_anchor)
    end_x, end_y = conn.to_node.anchor_pos(conn.to_anchor)

    # Convert to grid coordinates
    sc, sr = tikz_to_grid(start_x, start_y, origin_x, origin_y, resolution, rows)
    ec, er = tikz_to_grid(end_x, end_y, origin_x, origin_y, resolution, rows)

    # Clamp to grid bounds
    sc = max(0, min(cols - 1, sc))
    sr = max(0, min(rows - 1, sr))
    ec = max(0, min(cols - 1, ec))
    er = max(0, min(rows - 1, er))

    # Temporarily unblock start and end cells
    grid = Grid(matrix=matrix)
    start_node = grid.node(sc, sr)
    end_node = grid.node(ec, er)

    # Make start/end walkable even if inside obstacle
    start_node.walkable = True
    end_node.walkable = True

    # Find path
    finder = AStarFinder()
    path, _ = finder.find_path(start_node, end_node, grid)

    if not path:
        # Fallback: direct L-shape connection
        return [(start_x, start_y), (end_x, start_y), (end_x, end_y)]

    # Convert grid path back to TikZ coordinates
    tikz_path = []
    for col, row in path:
        x, y = grid_to_tikz(col, row, origin_x, origin_y, resolution, rows)
        tikz_path.append((round(x, 2), round(y, 2)))

    # Simplify: remove collinear points
    tikz_path = simplify_path(tikz_path)

    # Snap to orthogonal
    tikz_path = snap_to_orthogonal(tikz_path)

    # Replace first and last with exact anchor positions
    if tikz_path:
        tikz_path[0] = (round(start_x, 2), round(start_y, 2))
        tikz_path[-1] = (round(end_x, 2), round(end_y, 2))

    return tikz_path


# ─── TikZ 代码生成 ───

def path_to_tikz(conn, path_points):
    """Generate TikZ \\draw command from path points."""
    if not path_points:
        return f"% ERROR: no path found for {conn.from_node.name} -> {conn.to_node.name}"

    style = conn.style or "arrow"
    coords = " -- ".join(f"({x:.2f},{y:.2f})" for x, y in path_points)

    label_part = ""
    if conn.label:
        mid = len(path_points) // 2
        label_part = f" node[midway, above, font=\\scriptsize] {{{conn.label}}}"

    return f"\\draw[{style}, rounded corners=6pt] {coords}{label_part};"


# ─── 主逻辑 ───

def route_all(spec):
    """Route all connections and output TikZ code."""
    # Parse nodes
    node_map = {}
    nodes = []
    for n in spec["nodes"]:
        node = Node(n["name"], n["x"], n["y"], n["width"], n["height"])
        node_map[n["name"]] = node
        nodes.append(node)

    # Parse connections
    connections = []
    for c in spec["connections"]:
        conn = Connection(
            from_node=node_map[c["from"]],
            from_anchor=c.get("from_anchor", "south"),
            to_node=node_map[c["to"]],
            to_anchor=c.get("to_anchor", "north"),
            style=c.get("style", "arrow"),
            label=c.get("label", ""),
        )
        connections.append(conn)

    resolution = spec.get("grid_resolution", 0.15)

    # Build obstacle grid
    matrix, ox, oy, res, rows, cols = build_grid(nodes, resolution)

    print(f"% TikZ 路径规划器自动生成")
    print(f"% 网格: {cols}x{rows}, 分辨率: {res:.2f}cm")
    print(f"% 节点数: {len(nodes)}, 连线数: {len(connections)}")
    print()

    # Route each connection
    for conn in connections:
        path = route_connection(conn, nodes, matrix, ox, oy, res, rows, cols)
        tikz_code = path_to_tikz(conn, path)
        print(f"% {conn.from_node.name}.{conn.from_anchor} -> "
              f"{conn.to_node.name}.{conn.to_anchor}")
        print(tikz_code)
        print()


def main():
    if len(sys.argv) < 2:
        print("用法: python3 tikz-path-router.py <routing-spec.json>")
        print("  或: echo '{...}' | python3 tikz-path-router.py -")
        sys.exit(1)

    if sys.argv[1] == "-":
        spec = json.load(sys.stdin)
    else:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            spec = json.load(f)

    route_all(spec)


if __name__ == "__main__":
    main()
