#!/usr/bin/env python3
r"""
PDF 重叠检测器 — 编译后自动检测渲染结果中的多种几何问题。

用法:
    python3 pdf-overlap-checker.py <file.pdf>            # 人读文本输出
    python3 pdf-overlap-checker.py <file.pdf> --json     # 结构化输出供 sub-agent 消费

7 类检测（5 基础 + 2 candidate-triage）：
  基础 5 类（直接 fix）：
    text-overlap        两段文字 bbox 相交（IoU > 0.03）            [ERROR]
    text-overflow       文字溢出其容器矩形                          [ERROR/WARN]
    off-center          容器内容偏离中心 / 顶部留白过多              [WARN]
    text-line           文字被水平/垂直线穿过                        [WARN]
    line-crossing       多条 line segment 互相交叉（聚合计数）       [WARN]
  Candidate 2 类（需 sub-agent triage 区分 ignore/fix）：
    line-through-node   line 真穿过 filled rect 内部（PyMuPDF 几何） [ERROR, candidate]
    node-overlap        两个 sibling node rect 几何重叠              [ERROR, candidate]

后两类需 PyMuPDF（pip install pymupdf）。缺失时会打印 ERROR 并退出 — 不静默跳过。

输出: 逐条报告问题，无问题则输出 PASS
退出码: 0=全部通过, 1=有警告, 2=有错误
"""

import sys
from dataclasses import dataclass


@dataclass
class BBox:
    x0: float
    top: float
    x1: float
    bottom: float
    label: str = ""

    @property
    def width(self):
        return self.x1 - self.x0

    @property
    def height(self):
        return self.bottom - self.top

    @property
    def cx(self):
        return (self.x0 + self.x1) / 2

    @property
    def cy(self):
        return (self.top + self.bottom) / 2


@dataclass
class Issue:
    level: str  # ERROR, WARN
    category: str
    message: str


def bbox_overlap(a: BBox, b: BBox) -> tuple[float, float]:
    """Return (overlap_x, overlap_y) in points. Positive = overlapping."""
    overlap_x = min(a.x1, b.x1) - max(a.x0, b.x0)
    overlap_y = min(a.bottom, b.bottom) - max(a.top, b.top)
    return overlap_x, overlap_y


def bbox_iou(a: BBox, b: BBox) -> float:
    """Intersection over Union of two bounding boxes."""
    ox, oy = bbox_overlap(a, b)
    if ox <= 0 or oy <= 0:
        return 0.0
    intersection = ox * oy
    area_a = a.width * a.height
    area_b = b.width * b.height
    union = area_a + area_b - intersection
    if union <= 0:
        return 0.0
    return intersection / union


def gap_between(a: BBox, b: BBox) -> float:
    """Minimum gap between two bboxes (negative = overlapping)."""
    ox, oy = bbox_overlap(a, b)
    if ox > 0 and oy > 0:
        return -min(ox, oy)  # overlapping
    # Not overlapping - find closest gap
    gap_x = max(a.x0, b.x0) - min(a.x1, b.x1)
    gap_y = max(a.top, b.top) - min(a.bottom, b.bottom)
    if gap_x > 0 and gap_y > 0:
        return min(gap_x, gap_y)
    return max(gap_x, gap_y) if gap_x > 0 or gap_y > 0 else -min(abs(gap_x), abs(gap_y))


def is_same_text(a: BBox, b: BBox) -> bool:
    """Check if two words are essentially the same element (overlaid intentionally)."""
    return (abs(a.x0 - b.x0) < 1.0 and abs(a.top - b.top) < 1.0 and
            abs(a.x1 - b.x1) < 1.0 and abs(a.bottom - b.bottom) < 1.0)


def is_inside(inner: BBox, outer: BBox, margin: float = 0) -> bool:
    """Check if inner bbox is fully inside outer bbox with optional margin."""
    return (inner.x0 >= outer.x0 - margin and
            inner.x1 <= outer.x1 + margin and
            inner.top >= outer.top - margin and
            inner.bottom <= outer.bottom + margin)


def find_container(word: BBox, rects: list[BBox]) -> BBox | None:
    """Find the smallest rectangle that contains the word's center."""
    best = None
    best_area = float('inf')

    for rect in rects:
        # Skip very small rects (decorations) and very large rects (page-level backgrounds)
        if rect.width < 10 or rect.height < 8:
            continue
        if rect.width > 500 and rect.height > 500:
            continue

        # Check if word center is inside rect
        if (rect.x0 <= word.cx <= rect.x1 and
                rect.top <= word.cy <= rect.bottom):
            area = rect.width * rect.height
            if area < best_area:
                best = rect
                best_area = area

    return best


def check_word_overlaps(words: list[BBox]) -> list[Issue]:
    """Check nearby word pairs for overlapping bounding boxes."""
    issues = []
    MIN_GAP = 1.5  # minimum gap in points
    PROXIMITY = 50.0  # compare words within 50pt (increased from 30)

    checked = set()
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            a, b = words[i], words[j]

            # Quick proximity filter — skip pairs that are far apart
            if abs(a.cx - b.cx) > PROXIMITY + a.width / 2 + b.width / 2:
                continue
            if abs(a.cy - b.cy) > PROXIMITY + a.height / 2 + b.height / 2:
                continue

            # Skip if same text at same position (intentional)
            if is_same_text(a, b):
                continue

            # Skip single-char math subscripts (both must be tiny single chars)
            if a.width < 5 and b.width < 5 and len(a.label) <= 1 and len(b.label) <= 1:
                continue

            pair_key = (min(a.label, b.label), max(a.label, b.label))
            if pair_key in checked:
                continue

            ox, oy = bbox_overlap(a, b)
            if ox > 0 and oy > 0:
                # Skip intra-word kerning false positives:
                # pdfplumber occasionally splits a single tightly-kerned word
                # (e.g. "Av" in "FedAvg") into adjacent fragments whose bboxes
                # have <2pt horizontal overlap while sharing >=90% of y-range.
                # Treat these as a single word, not as colliding labels.
                y_share = min(a.bottom, b.bottom) - max(a.top, b.top)
                y_min_h = min(a.height, b.height)
                if y_min_h > 0 and y_share / y_min_h >= 0.9 and ox < 2.0:
                    continue

                iou = bbox_iou(a, b)
                if iou > 0.03:
                    issues.append(Issue(
                        level="ERROR",
                        category="text-overlap",
                        message=f"文字重叠: \"{a.label}\" 和 \"{b.label}\" "
                                f"IoU={iou:.3f} (重叠 {ox:.1f}×{oy:.1f}pt)"
                    ))
                    checked.add(pair_key)
            else:
                # Check tight spacing only for truly adjacent elements
                g = gap_between(a, b)
                if 0 < g < MIN_GAP:
                    # Must be in same row (y overlap) or same column (x overlap)
                    y_overlap = min(a.bottom, b.bottom) - max(a.top, b.top)
                    x_overlap = min(a.x1, b.x1) - max(a.x0, b.x0)
                    if y_overlap > min(a.height, b.height) * 0.5 or \
                       x_overlap > min(a.width, b.width) * 0.5:
                        issues.append(Issue(
                            level="WARN",
                            category="text-tight",
                            message=f"文字间距过小: \"{a.label}\" 和 \"{b.label}\" "
                                    f"间距仅 {g:.1f}pt"
                        ))
                        checked.add(pair_key)

    return issues


def check_text_overflow(words: list[BBox], rects: list[BBox]) -> list[Issue]:
    """Check if any text overflows its container rectangle."""
    issues = []
    TOLERANCE = 2.0  # tolerance in points

    for word in words:
        container = find_container(word, rects)
        if container is None:
            continue

        # Check each side
        overflows = []
        if word.x0 < container.x0 - TOLERANCE:
            overflows.append(f"左溢出 {container.x0 - word.x0:.1f}pt")
        if word.x1 > container.x1 + TOLERANCE:
            overflows.append(f"右溢出 {word.x1 - container.x1:.1f}pt")
        if word.top < container.top - TOLERANCE:
            overflows.append(f"上溢出 {container.top - word.top:.1f}pt")
        if word.bottom > container.bottom + TOLERANCE:
            overflows.append(f"下溢出 {word.bottom - container.bottom:.1f}pt")

        if overflows:
            max_overflow = max(
                container.x0 - word.x0 if word.x0 < container.x0 else 0,
                word.x1 - container.x1 if word.x1 > container.x1 else 0,
                container.top - word.top if word.top < container.top else 0,
                word.bottom - container.bottom if word.bottom > container.bottom else 0,
            )
            level = "ERROR" if max_overflow > 5.0 else "WARN"
            issues.append(Issue(
                level=level,
                category="text-overflow",
                message=f"文字溢出容器: \"{word.label}\" {', '.join(overflows)}"
            ))

    return issues


def check_content_balance(words: list[BBox], rects: list[BBox]) -> list[Issue]:
    """Check if content inside large containers is reasonably centered."""
    issues = []
    MIN_CONTAINER = 80.0  # only check containers > 80pt (about 2.8cm)

    for rect in rects:
        if rect.width < MIN_CONTAINER or rect.height < MIN_CONTAINER:
            continue
        # Skip very large rects (page-level)
        if rect.width > 500 and rect.height > 500:
            continue

        # Find all words inside this container
        inside_words = [w for w in words
                        if rect.x0 <= w.cx <= rect.x1 and rect.top <= w.cy <= rect.bottom]
        if len(inside_words) < 2:
            continue

        # Calculate content bounding box
        content_x0 = min(w.x0 for w in inside_words)
        content_x1 = max(w.x1 for w in inside_words)
        content_top = min(w.top for w in inside_words)
        content_bottom = max(w.bottom for w in inside_words)

        # Check horizontal centering
        left_margin = content_x0 - rect.x0
        right_margin = rect.x1 - content_x1
        if rect.width > 100 and left_margin > 0 and right_margin > 0:
            margin_ratio = max(left_margin, right_margin) / max(min(left_margin, right_margin), 1)
            if margin_ratio > 4.0:
                issues.append(Issue(
                    level="WARN",
                    category="off-center",
                    message=f"内容偏移: 容器({rect.width:.0f}×{rect.height:.0f}pt) "
                            f"左margin={left_margin:.0f}pt 右margin={right_margin:.0f}pt "
                            f"(比值 {margin_ratio:.1f}:1)"
                ))

        # Check top-heavy (title bar takes too much space)
        top_margin = content_top - rect.top
        bottom_margin = rect.bottom - content_bottom
        if rect.height > 100 and top_margin > 0 and bottom_margin > 0:
            if top_margin > rect.height * 0.4:
                issues.append(Issue(
                    level="WARN",
                    category="top-heavy",
                    message=f"上方留白过多: 容器高 {rect.height:.0f}pt, "
                            f"上方留白 {top_margin:.0f}pt ({top_margin/rect.height*100:.0f}%)"
                ))

    return issues


def check_text_line_overlap(words: list[BBox], lines: list[BBox]) -> list[Issue]:
    """Check if text overlaps with lines (arrows, zone borders, connections)."""
    issues = []
    BUFFER = 2.0  # minimum distance from text to line in points

    for word in words:
        if word.width < 8:  # skip tiny text
            continue
        for line in lines:
            # Expand line bbox by buffer
            lx0 = min(line.x0, line.x1) - BUFFER
            ly0 = min(line.top, line.bottom) - BUFFER
            lx1 = max(line.x0, line.x1) + BUFFER
            ly1 = max(line.top, line.bottom) + BUFFER

            # Check if word bbox intersects expanded line bbox
            if (word.x0 < lx1 and word.x1 > lx0 and
                    word.top < ly1 and word.bottom > ly0):
                # Calculate how much the word center is inside the line region
                # Only flag if the line actually crosses through the text area
                # (not just touching at edges)
                line_is_horizontal = abs(line.bottom - line.top) < 3
                line_is_vertical = abs(line.x1 - line.x0) < 3

                if line_is_horizontal:
                    line_y = (line.top + line.bottom) / 2
                    if word.top + 2 < line_y < word.bottom - 2:
                        issues.append(Issue(
                            level="WARN",
                            category="text-line",
                            message=f"线穿过文字: \"{word.label}\" "
                                    f"(水平线 y={line_y:.0f} 穿过文字区域 "
                                    f"y={word.top:.0f}-{word.bottom:.0f})"
                        ))
                elif line_is_vertical:
                    line_x = (line.x0 + line.x1) / 2
                    if word.x0 + 2 < line_x < word.x1 - 2:
                        issues.append(Issue(
                            level="WARN",
                            category="text-line",
                            message=f"线穿过文字: \"{word.label}\" "
                                    f"(垂直线 x={line_x:.0f} 穿过文字区域 "
                                    f"x={word.x0:.0f}-{word.x1:.0f})"
                        ))
    return issues


def segments_intersect(ax0, ay0, ax1, ay1, bx0, by0, bx1, by1) -> bool:
    """Check if two line segments intersect (excluding shared endpoints)."""
    def cross(ox, oy, ax, ay, bx, by):
        return (ax - ox) * (by - oy) - (ay - oy) * (bx - ox)

    d1 = cross(bx0, by0, bx1, by1, ax0, ay0)
    d2 = cross(bx0, by0, bx1, by1, ax1, ay1)
    d3 = cross(ax0, ay0, ax1, ay1, bx0, by0)
    d4 = cross(ax0, ay0, ax1, ay1, bx1, by1)

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    return False


def check_line_crossings(lines: list[BBox]) -> list[Issue]:
    """Detect lines crossing each other — messy connection areas."""
    issues = []
    crossings = 0
    MIN_LENGTH = 15.0  # ignore tiny lines (box borders, ticks)

    # Filter to meaningful lines
    real_lines = []
    for ln in lines:
        length = ((ln.x1 - ln.x0)**2 + (ln.bottom - ln.top)**2)**0.5
        if length >= MIN_LENGTH:
            real_lines.append(ln)

    for i in range(len(real_lines)):
        for j in range(i + 1, len(real_lines)):
            a, b = real_lines[i], real_lines[j]
            if segments_intersect(a.x0, a.top, a.x1, a.bottom,
                                  b.x0, b.top, b.x1, b.bottom):
                crossings += 1

    if crossings > 0:
        issues.append(Issue(
            level="WARN",
            category="line-crossing",
            message=f"检测到 {crossings} 处连线交叉。"
                    f"请确认每处交叉是否必要——"
                    f"必要的保留，可避免的重新路由"
        ))

    return issues


@dataclass
class Segment:
    """A line segment with real endpoints (not just a bbox)."""
    x0: float
    y0: float
    x1: float
    y1: float
    dashed: bool = False
    color: tuple = (0, 0, 0)
    path_id: int = -1  # which PyMuPDF drawing path this segment belongs to

    def length(self) -> float:
        return ((self.x1 - self.x0) ** 2 + (self.y1 - self.y0) ** 2) ** 0.5


def liang_barsky_clip(seg: Segment, rect: BBox) -> tuple[float, float] | None:
    """Liang-Barsky line-rect clipping. Returns (t_enter, t_exit) in [0,1] or None.

    Coordinate convention: PyMuPDF uses top-left origin, y grows downward.
    rect.top < rect.bottom (since top=y_min, bottom=y_max in our BBox).
    """
    dx = seg.x1 - seg.x0
    dy = seg.y1 - seg.y0
    p = [-dx, dx, -dy, dy]
    q = [seg.x0 - rect.x0, rect.x1 - seg.x0, seg.y0 - rect.top, rect.bottom - seg.y0]

    t_enter, t_exit = 0.0, 1.0
    for i in range(4):
        if p[i] == 0:
            if q[i] < 0:
                return None  # parallel and outside
        else:
            t = q[i] / p[i]
            if p[i] < 0:
                t_enter = max(t_enter, t)
            else:
                t_exit = min(t_exit, t)
    if t_enter > t_exit:
        return None
    return t_enter, t_exit


def point_on_rect_boundary(x: float, y: float, rect: BBox, tol: float = 1.5) -> bool:
    """Check if (x, y) sits on rect's edge within tolerance."""
    on_h = (abs(y - rect.top) <= tol or abs(y - rect.bottom) <= tol) and \
           (rect.x0 - tol <= x <= rect.x1 + tol)
    on_v = (abs(x - rect.x0) <= tol or abs(x - rect.x1) <= tol) and \
           (rect.top - tol <= y <= rect.bottom + tol)
    return on_h or on_v


def point_in_rect(x: float, y: float, rect: BBox, margin: float = -2.0) -> bool:
    """Check if (x, y) is strictly inside rect (with shrink margin for tolerance)."""
    return (rect.x0 - margin <= x <= rect.x1 + margin and
            rect.top - margin <= y <= rect.bottom + margin)


def check_line_through_nodes(
    segments: list[Segment],
    rects: list[BBox],
    rect_path_ids: list[int] | None = None,
) -> list[Issue]:
    """Detect lines whose interior passes through a filled rectangle node.

    Logic:
      For each segment AB and each candidate node rect R:
        - Skip if segment came from the same PyMuPDF path that produced R
          (a node's outline segments trivially "cross" its own bbox).
        - Clip AB against R via Liang-Barsky.
        - If both endpoints of AB are outside R and the clipped interval
          [t_in, t_out] has t_in > 0.05 and t_out < 0.95 (i.e. line crosses
          the interior, not just touching at endpoints) → flag.

    Filters:
      - Skip large rects (page-level zones): width > 140 OR height > 90.
      - Skip tiny rects (decorations): width < 6 OR height < 6.
      - Skip very short segments: length < 15pt (likely box borders themselves).
      - Cluster suppression: if a rect is crossed by 4+ distinct segments,
        it's likely a convergence node — drop the cluster.
    """
    if rect_path_ids is None:
        rect_path_ids = [-1] * len(rects)
    raw_hits = []     # collect first, cluster-filter second
    flagged = set()

    # A "node" rect must be plausibly box-shaped *and* small enough that a line
    # passing through its interior is suspicious.  Zone backgrounds (large
    # filled rectangles that hold multiple nodes) are intentionally crossed by
    # internal connections, so we must exclude them or the detector explodes.
    MAX_W = 140      # ~5cm — anything wider is a zone, not a node
    MAX_H = 90       # ~3cm
    MAX_AREA = 12500 # pt² — full 140×90 box allowed. Hero boxes commonly
                     # reach 4.4cm × 2.2cm (=7750pt²) so the prior 7500 cap
                     # silently excluded Pedersen-sized heroes (fig97 bug).
    MIN_DIM = 6      # below this is decoration / glyph artifact

    candidate_rects = [
        (ri, r) for ri, r in enumerate(rects)
        if MIN_DIM <= r.width <= MAX_W
        and MIN_DIM <= r.height <= MAX_H
        and r.width * r.height <= MAX_AREA
    ]

    for seg in segments:
        if seg.length() < 15:
            continue
        for ri, rect in candidate_rects:
            both_inside = False  # explicit init so the bypass check below is robust
            # Skip "node's own outline segment crosses its own bbox" false positives.
            if seg.path_id >= 0 and rect_path_ids[ri] == seg.path_id:
                continue
            # Endpoint-on-boundary handling: an arrow that terminates at a
            # node's edge is *usually* a clean incoming connection — but NOT
            # if its stem also travels through the node's interior on the way
            # to that edge.  fig97 (Batch 10) hit this: an L-bend ((A.south) |-
            # (B.west)) where A's x sat inside B's x range routes the
            # horizontal leg *through* B's interior before landing on B.west.
            # So we only auto-skip when the endpoint approaches from outside.
            ep0_on_boundary = point_on_rect_boundary(seg.x0, seg.y0, rect)
            ep1_on_boundary = point_on_rect_boundary(seg.x1, seg.y1, rect)
            if ep0_on_boundary and ep1_on_boundary:
                # Both endpoints on boundary — could be either:
                #  (a) the rect's own stroke edge (top/bottom/left/right line),
                #      drawn by a separate "stroke" path even when fill came
                #      from another path → SKIP these.
                #  (b) a spanning chord through the node interior — true bug.
                # Distinguish: check if seg lies along one of the 4 edges.
                tol = 2.0
                on_top    = abs(seg.y0 - rect.top)    <= tol and abs(seg.y1 - rect.top)    <= tol
                on_bot    = abs(seg.y0 - rect.bottom) <= tol and abs(seg.y1 - rect.bottom) <= tol
                on_left   = abs(seg.x0 - rect.x0)     <= tol and abs(seg.x1 - rect.x0)     <= tol
                on_right  = abs(seg.x0 - rect.x1)     <= tol and abs(seg.x1 - rect.x1)     <= tol
                if on_top or on_bot or on_left or on_right:
                    continue  # rect's own edge
                # Not on an edge → spanning chord through interior → flag.
            elif ep0_on_boundary or ep1_on_boundary:
                # Check whether the *other* endpoint is outside the rect.
                # If yes AND the line's interior dwell-fraction is large,
                # the line is routing through the body to reach the edge.
                other_x = seg.x1 if ep0_on_boundary else seg.x0
                other_y = seg.y1 if ep0_on_boundary else seg.y0
                if point_in_rect(other_x, other_y, rect, margin=-3):
                    # Other endpoint inside → not a "pass through" case;
                    # it's a connection between an external point and an
                    # internal anchor.  Skip.
                    continue
                # Other endpoint outside: compute how much of the segment
                # actually lies *inside* the rect.  If > 30% of length, this
                # is the |- pierce bug; flag it.  Otherwise it's a normal
                # connection just touching the boundary at endpoint.
                clip_chk = liang_barsky_clip(seg, rect)
                if clip_chk is None:
                    continue
                inside_frac = clip_chk[1] - clip_chk[0]
                if inside_frac < 0.3:
                    continue
                # Fall through to the rest of the checks (which will re-clip
                # and emit the issue).
            else:
                ep0_inside = point_in_rect(seg.x0, seg.y0, rect, margin=-3)
                ep1_inside = point_in_rect(seg.x1, seg.y1, rect, margin=-3)
                if ep0_inside and ep1_inside:
                    # BOTH endpoints inside the rect — this is the `|-` /
                    # `-|` pierce pattern (fig97 Batch 10):
                    #   \draw[arrow] (A.south) |- (B.west)
                    # generates a short horizontal segment fully *inside* B,
                    # running from (A.x, B.cy) to (B.cx_inner, B.cy).
                    # Flag it as a line-through-node bug.  Spine filter above
                    # already excluded "long axis lines on rect's centerline"
                    # legitimate cases (lifelines).
                    both_inside = True  # used below to bypass t_in/t_out check
                else:
                    both_inside = False
                    if ep0_inside or ep1_inside:
                        # One inside, one outside — line crosses the boundary
                        # somewhere in the middle.  Skip: this is the normal
                        # "anchor=center" / "label points inward" case.
                        continue
            # Spine filter: a vertical line on the rect's vertical centerline
            # (±3pt) and much longer than the rect's height is a designed
            # "spine" — e.g. a sequence-diagram lifeline passing through its
            # actor header box, or a swimlane axis crossing a phase label.
            # Same for horizontal lines on the rect's horizontal centerline.
            is_vertical = abs(seg.x1 - seg.x0) < 1.0
            is_horizontal = abs(seg.y1 - seg.y0) < 1.0
            rect_cx = (rect.x0 + rect.x1) / 2
            rect_cy = (rect.top + rect.bottom) / 2
            if is_vertical and abs(seg.x0 - rect_cx) <= 3 \
                    and seg.length() > rect.height * 3:
                continue
            if is_horizontal and abs(seg.y0 - rect_cy) <= 3 \
                    and seg.length() > rect.width * 3:
                continue
            # --- Edge-coincident (outline) suppression --------------------
            # A segment that runs parallel to a rect edge and sits within
            # EDGE_BAND of it is the node's own border, not a line passing
            # *through* the node.  This is the dominant line-through-node
            # false positive (fig140 Batch 15: 18/18 hits on clean figure):
            # TikZ draws a filled box as a fill path (bbox) PLUS a separate
            # stroke path (the 4 border segments), so the border segments
            # carry a different path_id than the fill rect and escape the
            # same-path self-skip above; the fill/stroke bboxes also differ
            # by ~2-3pt (line width, rounded corners), so the two-endpoints-
            # on-boundary edge check (tol=2.0) misses them.  A true "line
            # through node" crosses the interior well away from any edge, so
            # a tight band cannot suppress it.  Applied only to axis-aligned
            # segments — diagonal chords through a node are never edges.
            #
            # The band is proportional to the rect's short side (capped by an
            # absolute floor) so a rounded-rectangle's straight edge run —
            # which sits one corner-radius inside the bbox (fig148 stage boxes:
            # ~23pt radius on a 64pt-tall box = 36% of the short side) — is
            # still recognised as an edge.  A true through-line crosses the
            # central ~20% band, which no edge suppression reaches.  Widening
            # recall here costs nothing: across the whole archive audit,
            # line-through-node never once flagged a real defect — real defects
            # are text-class (text-overlap / text-line), handled separately.
            EDGE_BAND = max(3.5, 0.40 * min(rect.width, rect.height))
            seg_is_h = abs(seg.y1 - seg.y0) < 2.0
            seg_is_v = abs(seg.x1 - seg.x0) < 2.0
            if seg_is_h:
                seg_y = (seg.y0 + seg.y1) / 2
                if min(abs(seg_y - rect.top), abs(seg_y - rect.bottom)) <= EDGE_BAND:
                    continue
            elif seg_is_v:
                seg_x = (seg.x0 + seg.x1) / 2
                if min(abs(seg_x - rect.x0), abs(seg_x - rect.x1)) <= EDGE_BAND:
                    continue

            clip = liang_barsky_clip(seg, rect)
            if clip is None:
                continue
            t_in, t_out = clip
            # Require crossing to be "through" — not just glancing edge.
            # Two exceptions:
            #   (a) endpoint-on-boundary case: t_in (or t_out) is legitimately
            #       0 (or 1).  Boundary filter above already gated this.
            #   (b) both-endpoints-inside case: t_in=0 and t_out=1 always —
            #       the segment lives entirely inside the rect.  This is the
            #       fig97 |- pierce bug; allow it through.
            ep_on_boundary = (ep0_on_boundary or ep1_on_boundary)
            bypass_through_check = ep_on_boundary or both_inside
            if not bypass_through_check:
                if t_in <= 0.05 or t_out >= 0.95:
                    continue
            crossing_length = (t_out - t_in) * seg.length()
            if crossing_length < 3:  # very short crossing — likely numerical noise
                continue
            key = (round(seg.x0), round(seg.y0), round(seg.x1), round(seg.y1), ri)
            if key in flagged:
                continue
            flagged.add(key)
            dash_tag = "dashed " if seg.dashed else ""
            raw_hits.append((ri, Issue(
                level="ERROR",
                category="line-through-node",
                message=f"{dash_tag}线穿过节点: 从({seg.x0:.0f},{seg.y0:.0f})→"
                        f"({seg.x1:.0f},{seg.y1:.0f}) 穿过 "
                        f"rect[{rect.x0:.0f},{rect.top:.0f},{rect.x1:.0f},{rect.bottom:.0f}] "
                        f"内部 (crossing {crossing_length:.0f}pt)"
            )))

    # Cluster suppression: if a single rect is crossed by ≥4 distinct segments,
    # it is almost certainly a convergence node (e.g. CA3/CA1 pyramidal neuron
    # in a hippocampal network) or a misclassified zone — drop all hits on it.
    # Real "line accidentally crossing a node" bugs hit 1-3 segments per rect.
    CLUSTER_THRESHOLD = 4
    hits_per_rect: dict[int, int] = {}
    for ri, _ in raw_hits:
        hits_per_rect[ri] = hits_per_rect.get(ri, 0) + 1
    return [iss for ri, iss in raw_hits if hits_per_rect[ri] < CLUSTER_THRESHOLD]


def _seg_is_rect_edge(sy_or_sx: float, span0: float, span1: float,
                      rects: list[BBox], horizontal: bool) -> bool:
    """True if an axis-aligned line coincides with some rect's edge (so it is a
    box/zone border, not a leader).  Horizontal line: its y matches a rect's
    top/bottom and its x-span overlaps that rect.  Vertical: symmetric."""
    EDGE_TOL = 3.5
    for r in rects:
        if horizontal:
            if min(abs(sy_or_sx - r.top), abs(sy_or_sx - r.bottom)) <= EDGE_TOL \
                    and span0 < r.x1 and span1 > r.x0:
                return True
        else:
            if min(abs(sy_or_sx - r.x0), abs(sy_or_sx - r.x1)) <= EDGE_TOL \
                    and span0 < r.bottom and span1 > r.top:
                return True
    return False


def check_text_strikethrough(
    words: list[BBox], segments: list[Segment], rects: list[BBox]
) -> list[Issue]:
    r"""Detect a line/arrow/leader passing through the CENTER of a text label —
    a strikethrough that garbles the label.

    Two archive defects this catches that the WARN-level text-line advisory
    (pdfplumber-based) missed or under-graded:
      - fig146 (VAE): a DASHED `ε∼N(0,I)` leader runs straight through its own
        caption.  pdfplumber drops dashed strokes, so text-line never saw it.
        PyMuPDF segments carry the dash flag, so we see it here.
      - fig95 (glycolysis): the main-spine arrow passes through the phase
        labels.  text-line flagged it only as WARN; a through-the-center
        strike is a hard defect, not an advisory.

    High-confidence ERROR — fires only when an axis-aligned segment (a) crosses
    the word's central band, (b) extends >= EXT past BOTH ends of the word, and
    (c) is NOT one of a rect's own edges.  Test (b) rejects fraction bars,
    underlines, and subscript rules (none straddle the whole word); test (c)
    rejects box/zone borders that happen to run at a title's height (fig147
    Transformer-Encoder zone top edge over its "Output: T…" title).  A genuine
    leader (fig146) sits in open space, coincident with no rect edge.
    """
    issues: list[Issue] = []
    MIN_W = 10.0     # skip single glyphs / tiny fragments (bare sub/superscripts)
    EXT = 8.0        # segment must extend >= EXT pt past each end of the word
    BUF = 2.0        # central band = word minus BUF pt top & bottom (abs, matches
                     # check_text_line_overlap; proportional bands miss by <1pt)

    for w in words:
        if w.width < MIN_W or w.height < 4:
            continue
        for s in segments:
            is_h = abs(s.y1 - s.y0) < 2.0
            is_v = abs(s.x1 - s.x0) < 2.0
            if is_h:
                sy = (s.y0 + s.y1) / 2
                if not (w.top + BUF < sy < w.bottom - BUF):
                    continue
                sx0, sx1 = min(s.x0, s.x1), max(s.x0, s.x1)
                if not (sx0 <= w.x0 - EXT and sx1 >= w.x1 + EXT):
                    continue
                if _seg_is_rect_edge(sy, sx0, sx1, rects, horizontal=True):
                    continue
                tag = "虚线" if s.dashed else "线"
                issues.append(Issue(
                    level="ERROR",
                    category="text-strikethrough",
                    message=f"{tag}穿删文字: \"{w.label}\" "
                            f"(水平{tag} y={sy:.0f} 贯穿文字中心 "
                            f"y={w.top:.0f}-{w.bottom:.0f}, 两端超出文字)"
                ))
                break
            elif is_v:
                sx = (s.x0 + s.x1) / 2
                if not (w.x0 + BUF < sx < w.x1 - BUF):
                    continue
                sy0, sy1 = min(s.y0, s.y1), max(s.y0, s.y1)
                if not (sy0 <= w.top - EXT and sy1 >= w.bottom + EXT):
                    continue
                if _seg_is_rect_edge(sx, sy0, sy1, rects, horizontal=False):
                    continue
                tag = "虚线" if s.dashed else "线"
                issues.append(Issue(
                    level="ERROR",
                    category="text-strikethrough",
                    message=f"{tag}穿删文字: \"{w.label}\" "
                            f"(垂直{tag} x={sx:.0f} 贯穿文字中心 "
                            f"x={w.x0:.0f}-{w.x1:.0f}, 两端超出文字)"
                ))
                break

    return issues


def check_node_overlap(
    rects: list[BBox],
    rect_path_ids: list[int] | None = None,
) -> list[Issue]:
    """Detect pairs of node-sized rects that geometrically overlap (sibling
    overlap, not parent-child containment).

    Filters:
      - Both rects must be node-sized (6-140pt × 6-90pt).
      - Skip pairs from the same drawing path (same node).
      - Skip pairs where one fully contains the other (zone-in-zone, panel
        holding a child node).
      - Require IoU ≥ 0.05 — micro overlaps from bbox synthesis are noise.
    """
    if rect_path_ids is None:
        rect_path_ids = [-1] * len(rects)
    issues = []
    # Tighter min dim than line-through-node check: glyph fills are 4-8pt and
    # would generate spurious overlaps. A real node is at least ~10pt on its
    # short side. Y-fork junction dots (~4-5pt) are intentionally excluded —
    # overlap detection at that scale is noise.
    MIN_DIM, MAX_W, MAX_H = 10, 140, 90
    MIN_IOU = 0.05

    nodes = [
        (i, r, rect_path_ids[i])
        for i, r in enumerate(rects)
        if MIN_DIM <= r.width <= MAX_W and MIN_DIM <= r.height <= MAX_H
    ]

    seen_pairs = set()
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            _ri, a, pi = nodes[i]
            _rj, b, pj = nodes[j]
            if pi >= 0 and pi == pj:
                continue  # same drawing path
            # Skip identical rects (two paths drew the same outline + fill)
            if abs(a.x0 - b.x0) < 1 and abs(a.x1 - b.x1) < 1 \
                    and abs(a.top - b.top) < 1 and abs(a.bottom - b.bottom) < 1:
                continue
            # Drop-shadow pattern: TikZ `drop shadow` style draws the same box
            # twice — a grey shadow offset by ~2-3pt + the main fill rect.
            # Two rects of nearly identical W/H whose centers differ by ≤5pt
            # in both axes is overwhelmingly drop shadow, not a real overlap.
            if abs(a.width - b.width) < 3 and abs(a.height - b.height) < 3:
                a_cx, a_cy = (a.x0 + a.x1) / 2, (a.top + a.bottom) / 2
                b_cx, b_cy = (b.x0 + b.x1) / 2, (b.top + b.bottom) / 2
                if abs(a_cx - b_cx) <= 5 and abs(a_cy - b_cy) <= 5 \
                        and (abs(a_cx - b_cx) > 0.5 or abs(a_cy - b_cy) > 0.5):
                    continue  # drop shadow twin
            # Parent-child? one fully inside the other → OK
            if is_inside(a, b, margin=2) or is_inside(b, a, margin=2):
                continue
            iou = bbox_iou(a, b)
            if iou < MIN_IOU:
                continue
            key = (round(a.x0), round(a.top), round(a.x1), round(a.bottom),
                   round(b.x0), round(b.top), round(b.x1), round(b.bottom))
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            ox, oy = bbox_overlap(a, b)
            issues.append(Issue(
                level="ERROR",
                category="node-overlap",
                message=f"节点重叠: rect[{a.x0:.0f},{a.top:.0f},{a.x1:.0f},{a.bottom:.0f}] "
                        f"vs rect[{b.x0:.0f},{b.top:.0f},{b.x1:.0f},{b.bottom:.0f}] "
                        f"IoU={iou:.3f} (重叠 {ox:.1f}×{oy:.1f}pt)"
            ))
    return issues


def extract_pymupdf_geometry(filepath: str):
    """Use PyMuPDF to extract real line endpoints + curves + filled rects.

    Returns (segments, curves_as_bboxes, rects_filled, rects_stroke,
              rects_filled_path_id).  Each Segment carries its own
              `path_id` so callers can skip self-comparisons (a node's
              outline segments vs the same node's bbox rect).
    Falls back to (None, None, None, None, None) if PyMuPDF unavailable.
    """
    try:
        import fitz
    except ImportError:
        # LOUD failure — do not silently skip line-through-node + node-overlap.
        # Sub-agents reading the report would otherwise believe these checks
        # passed when they were never run.
        print(
            "ERROR: pymupdf 未安装。line-through-node + node-overlap 两类检测"
            "将不会运行。\n"
            "  安装: pip install pymupdf",
            file=sys.stderr,
        )
        return None, None, None, None, None

    pdf = fitz.open(filepath)
    if pdf.page_count == 0:
        return [], [], [], [], []
    page = pdf[0]
    drawings = page.get_drawings()

    segments: list[Segment] = []
    curve_bboxes: list[BBox] = []
    rects_filled: list[BBox] = []
    rects_stroke: list[BBox] = []

    # Track which path id each filled rect came from, so check_line_through_nodes
    # can skip "a path's own segments cross its own bbox" false positives.
    rects_filled_path_id: list[int] = []  # parallel to rects_filled

    for pid, d in enumerate(drawings):
        is_dashed = bool(d.get("dashes"))
        stroke = d.get("color")
        fill = d.get("fill")
        # Track this path's overall bbox so we can register a *filled* path
        # (TikZ-style filled box drawn as 4 line segments) as a node rect.
        path_xs: list[float] = []
        path_ys: list[float] = []

        for it in d.get("items", []):
            op = it[0]
            if op == "l":
                p1, p2 = it[1], it[2]
                segments.append(Segment(
                    x0=p1.x, y0=p1.y, x1=p2.x, y1=p2.y,
                    dashed=is_dashed, color=stroke or (0, 0, 0), path_id=pid
                ))
                path_xs.extend([p1.x, p2.x])
                path_ys.extend([p1.y, p2.y])
            elif op == "c":
                # Bezier control points: p0, p1, p2, p3
                pts = [it[1], it[2], it[3], it[4]] if len(it) > 4 else list(it[1:])
                if pts:
                    xs = [p.x for p in pts]
                    ys = [p.y for p in pts]
                    curve_bboxes.append(BBox(
                        x0=min(xs), top=min(ys),
                        x1=max(xs), bottom=max(ys),
                        label="bezier"
                    ))
                    path_xs.extend(xs)
                    path_ys.extend(ys)
                    # Also approximate the curve with chord segments for through-node test
                    if len(pts) >= 2:
                        for i in range(len(pts) - 1):
                            segments.append(Segment(
                                x0=pts[i].x, y0=pts[i].y,
                                x1=pts[i + 1].x, y1=pts[i + 1].y,
                                dashed=is_dashed, color=stroke or (0, 0, 0),
                                path_id=pid
                            ))
            elif op == "re":
                r = it[1]
                bb = BBox(x0=r.x0, top=r.y0, x1=r.x1, bottom=r.y1, label="rect")
                if fill is not None:
                    rects_filled.append(bb)
                    rects_filled_path_id.append(pid)
                else:
                    rects_stroke.append(bb)
                path_xs.extend([r.x0, r.x1])
                path_ys.extend([r.y0, r.y1])

        # If the path is filled (fill color set) AND has geometric extent that
        # *isn't* already captured by a `re` operator above, register it as a
        # synthesized filled rect (covers the common TikZ case of a node drawn
        # as 4 lines + fill).
        if fill is not None and path_xs and path_ys:
            x0, x1 = min(path_xs), max(path_xs)
            y0, y1 = min(path_ys), max(path_ys)
            w, h = x1 - x0, y1 - y0
            # Skip degenerate (line-shaped) and page-sized fills.
            if w >= 4 and h >= 4 and not (w > 500 and h > 500):
                rects_filled.append(BBox(
                    x0=x0, top=y0, x1=x1, bottom=y1, label="filled-path"
                ))
                rects_filled_path_id.append(pid)

    pdf.close()
    return segments, curve_bboxes, rects_filled, rects_stroke, rects_filled_path_id


def validate_pdf(filepath: str) -> list[Issue]:
    """Main validation: extract PDF elements and check for overlaps."""
    try:
        import pdfplumber
    except ImportError:
        print("ERROR: pdfplumber 未安装。运行: pip install pdfplumber")
        sys.exit(1)

    pdf = pdfplumber.open(filepath)
    if not pdf.pages:
        print("ERROR: PDF 没有页面")
        sys.exit(1)

    page = pdf.pages[0]

    # Extract words with bounding boxes
    raw_words = page.extract_words(
        keep_blank_chars=False,
        x_tolerance=3,
        y_tolerance=3,
    )

    words = []
    for w in raw_words:
        text = w.get("text", "").strip()
        if not text or len(text) < 1:
            continue
        words.append(BBox(
            x0=float(w["x0"]),
            top=float(w["top"]),
            x1=float(w["x1"]),
            bottom=float(w["bottom"]),
            label=text[:25],  # truncate for display
        ))

    # Extract rectangles (container boxes)
    raw_rects = page.rects or []
    rects = []
    for r in raw_rects:
        rects.append(BBox(
            x0=float(r["x0"]),
            top=float(r["top"]),
            x1=float(r["x1"]),
            bottom=float(r["bottom"]),
            label="rect",
        ))

    # Extract lines (arrows, connections, zone borders)
    raw_lines = page.lines or []
    pdf_lines = []
    for ln in raw_lines:
        pdf_lines.append(BBox(
            x0=float(ln["x0"]),
            top=float(ln["top"]),
            x1=float(ln["x1"]),
            bottom=float(ln["bottom"]),
            label="line",
        ))

    # Also extract curves (dashed lines, arcs, bezier paths)
    raw_curves = page.curves or []
    for crv in raw_curves:
        # Use the bounding box of the curve's points
        pts = crv.get("pts", [])
        if not pts:
            continue
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        if xs and ys:
            pdf_lines.append(BBox(
                x0=min(xs), top=min(ys),
                x1=max(xs), bottom=max(ys),
                label="curve",
            ))

    all_issues: list[Issue] = []

    # 1. Text-text overlap
    all_issues.extend(check_word_overlaps(words))

    # 2. Text overflow from container
    if rects:
        all_issues.extend(check_text_overflow(words, rects))

    # 3. Content centering and balance inside containers
    if rects:
        all_issues.extend(check_content_balance(words, rects))

    # 4. Text-line overlap (text crossed by arrows or zone borders)
    if pdf_lines:
        all_issues.extend(check_text_line_overlap(words, pdf_lines))

    # 5. Line-line crossings (messy connection areas)
    if pdf_lines:
        all_issues.extend(check_line_crossings(pdf_lines))

    pdf.close()

    # 6. Line-through-node (PyMuPDF segments + best-available rect set).
    #
    # PyMuPDF gives real line endpoints (pdfplumber only gives line bboxes, losing
    # diagonal direction).  But many TikZ box-shaped nodes are drawn as 4-line
    # paths rather than `re` operators, so `rects_filled` from PyMuPDF is often
    # empty.  In that case fall back to pdfplumber's `rects` list (already
    # extracted above as the `rects` local), which recognizes node-sized
    # rectangles regardless of how they were drawn.
    segments, _curves, rects_filled, _rects_stroke, rect_pids = extract_pymupdf_geometry(filepath)
    if segments is not None:
        # 8. Text-strikethrough (a line/leader through a label's center).
        # Uses PyMuPDF segments so DASHED leaders are seen (pdfplumber drops
        # them, so the pdfplumber-based text-line advisory above misses them).
        # rects (pdfplumber stroke rects + PyMuPDF filled) let it reject
        # box/zone borders that merely run at a title's height.
        all_issues.extend(check_text_strikethrough(words, segments, rects + rects_filled))
        if rects_filled:
            node_rects = rects_filled
            node_rect_pids = rect_pids
        else:
            node_rects = rects
            node_rect_pids = [-1] * len(rects)  # pdfplumber rects have no path id
        if node_rects:
            all_issues.extend(check_line_through_nodes(segments, node_rects, node_rect_pids))
            # 7. Node-vs-node geometric overlap (sibling intersection).
            all_issues.extend(check_node_overlap(node_rects, node_rect_pids))

    return all_issues


def main():
    if len(sys.argv) < 2:
        print("用法: python3 pdf-overlap-checker.py <file.pdf> [--json]")
        sys.exit(1)

    json_mode = "--json" in sys.argv
    filepath = next(a for a in sys.argv[1:] if not a.startswith("--"))
    issues = validate_pdf(filepath)

    errors = [i for i in issues if i.level == "ERROR"]
    warns = [i for i in issues if i.level == "WARN"]

    if json_mode:
        import json
        out = {
            "file": filepath,
            "errors": [{"category": i.category, "message": i.message} for i in errors],
            "warnings": [{"category": i.category, "message": i.message} for i in warns],
            "summary": {"error_count": len(errors), "warning_count": len(warns)},
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        sys.exit(2 if errors else (1 if warns else 0))

    if not issues:
        print("✅ PASS — 未发现重叠问题")
        sys.exit(0)

    print(f"{'=' * 60}")
    print(f"PDF 重叠检测报告: {filepath}")
    print(f"{'=' * 60}")

    if errors:
        print(f"\n🔴 错误 ({len(errors)} 个) — 必须修复:")
        for i, issue in enumerate(errors, 1):
            print(f"  {i}. [{issue.category}] {issue.message}")

    if warns:
        print(f"\n🟡 警告 ({len(warns)} 个) — 建议修复:")
        for i, issue in enumerate(warns, 1):
            print(f"  {i}. [{issue.category}] {issue.message}")

    print(f"\n{'=' * 60}")
    print(f"总计: {len(errors)} 错误, {len(warns)} 警告")

    sys.exit(2 if errors else 1)


if __name__ == "__main__":
    main()
