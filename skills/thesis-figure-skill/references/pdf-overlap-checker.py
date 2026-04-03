#!/usr/bin/env python3
r"""
PDF 重叠检测器 — 编译后自动检测渲染结果中的文字重叠问题
用法: python3 pdf-overlap-checker.py <file.pdf>

基于 pdfplumber 解析 PDF 内部结构，检测：
  1. 文字-文字重叠：两段文字的 bounding box 有交集
  2. 文字溢出容器：文字 bbox 超出其所在矩形框的边界
  3. 文字间距过小：两段文字之间的间隙 < 2pt（即将重叠）

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
    return all_issues


def main():
    if len(sys.argv) < 2:
        print("用法: python3 pdf-overlap-checker.py <file.pdf>")
        sys.exit(1)

    filepath = sys.argv[1]
    issues = validate_pdf(filepath)

    if not issues:
        print("✅ PASS — 未发现重叠问题")
        sys.exit(0)

    errors = [i for i in issues if i.level == "ERROR"]
    warns = [i for i in issues if i.level == "WARN"]

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
