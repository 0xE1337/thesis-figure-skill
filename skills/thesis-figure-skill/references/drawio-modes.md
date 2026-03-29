## draw.io 科研展示图

### 何时使用

用户提及"技术路线图""研究框架""科研展示"，或参考图有3D透视/同心嵌套/倒金字塔/散布关键词等视觉效果。

### HTML 预览技术选型（关键教训）

**纯 CSS Flexbox/Grid 适合**：三层横向分区（模式A）、流水线链条（模式C）、三栏展开（模式E）——这些都是**规则矩形布局**。

**必须用 SVG 的场景**：3D 透视梯形/菱形嵌套（模式B）、散布关键词自由定位、放射线装饰、弧形连接线。**禁止用 CSS clip-path + preserveAspectRatio="none" 模拟梯形**——高度不可控会导致布局崩溃。

**CSS + 内嵌 SVG 混合模式**（模式F 专用）：整体页面用 CSS Flexbox 布局（行、侧栏、中心区），但在需要精确绘制的子区域内嵌 `<svg>` 元素——如 3D 圆柱体网络节点、树状连线、汇聚箭头。**规则**：
- CSS 负责宏观布局（行排列、侧栏、区块间距）
- SVG 负责微观精确绘制（圆柱体、连线、箭头、圆点）
- **SVG 和相邻 CSS 元素的对齐**：SVG 高度必须和相邻 flex 容器的高度一致，相邻 flex 容器内的子元素用 `justify-content: space-between` + 固定 `height`（等于 SVG 高度）实现等分，确保 SVG 内元素的 y 坐标和 CSS 子元素的垂直中心对齐（反复踩坑的规则）

**SVG 实现规则**：
- 整张图用单个 `<svg viewBox="0 0 W H">` 包裹，所有元素（梯形、文字、标签、侧栏）都在 SVG 内用绝对坐标
- **不混用 SVG 和 CSS 布局**——要么全 SVG（模式B/D），要么全 CSS（模式A/C/E），**模式F 除外**（模式F 用 CSS 整体布局 + 局部 SVG 绘制精确图形）
- 3D 透视梯形用 `<polygon>` 画4个面（前面板+顶面+左侧面+右侧面），不同透明度 fill 模拟光影
- 文字用 `<text>` + `text-anchor="middle"` 精确定位
- 竖排文字用 `writing-mode="tb"`

### 配色方案

**不要每张图都用紫色主题**——根据论文领域选择合适的配色方案。以下提供 4 套经过审美验证的配色，每套都包含主色、辅色、强调色、背景色：

**方案 A：学术蓝灰**（适合：计算机网络、系统架构、工程类）
- 主色：#1565C0（深蓝）→ 标题横幅、主分组框边框
- 辅色：#E3F2FD（浅蓝）→ 分组框背景、卡片背景
- 强调色：#FF6F00（琥珀橙）→ 核心模块、编号圆、强调标签
- 中性色：#ECEFF1/#CFD8DC（蓝灰）→ 辅助区域、子分组
- 文字：#1A237E（深蓝黑）→ 标题；#37474F（深灰蓝）→ 正文
- 标题胶囊：fillColor=#1565C0; gradientColor=#1976D2; fontColor=#FFFFFF

**方案 B：粉紫渐变**（适合：AI/深度学习、数据科学、生物信息）
- 主色：#7B1FA2（深紫）→ 标题横幅
- 辅色：#F3E5F5（浅紫）/ #FCE4EC（浅粉）→ 背景
- 强调色：#C2185B（品红）→ 空心字、强调标签
- 标题胶囊：fillColor=#5C6BC0; gradientColor=#7986CB; fontColor=#FFFFFF
- 编号圆：fillColor=#FFD54F; strokeColor=#E65100（金黄）

**方案 C：翠绿自然**（适合：物联网、智慧农业、环境科学、可持续发展）
- 主色：#2E7D32（深绿）→ 标题横幅
- 辅色：#E8F5E9（浅绿）/ #F1F8E9（浅黄绿）→ 背景
- 强调色：#E65100（深橙）→ 核心模块、警告标签
- 中性色：#EFEBE9（暖灰）→ 辅助区域
- 标题胶囊：fillColor=#2E7D32; gradientColor=#43A047; fontColor=#FFFFFF

**方案 D：科技深色**（适合：安全、密码学、区块链、网络攻防）
- 主色：#263238（深蓝灰）→ 标题横幅
- 辅色：#ECEFF1（冰灰）/ #E8EAF6（淡蓝灰）→ 背景
- 强调色：#D32F2F（警示红）→ 安全告警、攻击路径
- 辅助强调：#00897B（青绿）→ 防御措施、安全模块
- 标题胶囊：fillColor=#263238; gradientColor=#37474F; fontColor=#FFFFFF

**配色选择规则**：
1. 在画图指令的"领域识别"步骤中确定论文领域
2. 按上表选择最匹配的方案（默认方案A，不再默认紫色）
3. 整图只用一套方案的颜色，不要跨方案混搭
4. 如果用户有明确的颜色偏好或参考图，优先按用户要求

**配色审美原则**：
- **同一张图最多用 3 种主色**（主色+辅色+强调色），过多颜色显得杂乱
- **强调色只用在 1-2 个核心元素上**，不要到处都是强调色
- **背景色要够浅**（接近白色），保证文字对比度
- **相邻分组用同色系深浅区分**，而非不同色系——如浅蓝/中蓝/深蓝，而非蓝/绿/橙

如用户要求用 TikZ 统一色板，则按 drawBlueFill/Line 等映射。

### 5 种布局模式

**模式 A：三层横向分区**（纯CSS）
- Flexbox 三栏布局，编号圆分隔

**模式 B：3D 透视倒金字塔**（纯SVG）★最复杂
- 多层梯形嵌套，从外到内收窄
- 每层梯形4面：`<polygon>` 前面板 + 顶面 + 左右侧面
- 梯形坐标计算：外层上边 `(x1,y1)-(x2,y1)` 宽，下边 `(x1+offset, y2)-(x2-offset, y2)` 窄
- 散布关键词用 `<text>` 自由定位在梯形内部/周围
- 左右侧栏在 SVG 内用 `writing-mode="tb"` 竖排

**模式 C：流水线链条**（纯CSS）
- Flexbox 圆形节点 + 加号水平排列

**模式 D：左右侧栏 + 中心嵌套**（纯SVG，配合模式B使用）
- 侧栏在 SVG 左右两侧，竖排文字+强调标签
- 弧形装饰线从中心发散到两侧：`<path d="M ... Q ..." />`

**模式 E：总论-展开-归纳**（纯CSS）
- 顶部强调框 → 三栏 → 底部箭头流程
- 左侧编号圆（一/二/三）+ 空心描边竖排分区标题
- 每层用 Flexbox 分左侧栏（side）+ 右侧内容（body）

**模式 F：分层技术路线图**（draw.io XML 实现）★常见论文配图
> draw.io XML 的模式F注意事项：3D 圆柱体用椭圆+矩形拼接时需注意接缝（侧面矩形的 fill 必须与椭圆一致且无 stroke，靠左右竖线勾勒轮廓）。空心描边字在 draw.io 中用 `fontColor=none;strokeColor=#7B1FA2;` 近似实现，效果不如 SVG 但可接受。

**模式F 布局硬性要求**：
- **论文总标题必须在最顶部**——整张图第一行就是论文标题（深色渐变横幅），不能被"研究背景"等子标题挡在下面
- **左右侧竖排标签必须是竖排文字，阅读方向从上到下**。在 draw.io XML 中：
  - 用 `horizontal=0;` 实现竖排，但注意 draw.io 的 `horizontal=0` 默认是从下往上读（逆时针90度旋转），这**不是**我们要的效果
  - **正确做法**：用 `rotation=-90;` 或 `vertical-align:middle;` + 每个字之间用 `<br>` 换行（如 `研<br>究<br>背<br>景`），确保从上往下阅读
  - **禁止**：文字需要歪头/翻转才能阅读的方向
- 典型从上到下顺序：论文标题 → 研究背景 → 问题提出 → 研究框架 → 主题横幅 → 研究内容 → 结论展望
- **所有内容区域必须水平居中**——标题横幅、子标题、卡片行、研究内容框都以页面中轴线对称。如果某一行只有 2 个卡片而其他行有 3 个，这 2 个卡片也要在该行内居中，不能左对齐
- **框内字体应尽量填满框**——如果框还有空间，字体不应该太小（fontSize ≥ 11）。框的大小是为内容服务的，不是内容迁就框的大小
- **太短的箭头直接删除**——如果两个元素上下紧挨（间距 < 30px），不需要画向下箭头，垂直排列本身已经暗示了方向。只看到箭头头看不到线段的箭头是多余的
- 典型结构：研究背景 → 问题提出 → 研究框架 → 论文主题横幅 → 研究内容（含网络节点图）→ 结论展望
- 左侧紫色竖排分区标签 + 右侧浅灰竖排注释标签
- 中间内容区：CSS Flexbox 行布局，每行用 `.row > .side-left + .center + .side-right`
- 渐变色标题胶囊（蓝紫渐变白字）、深紫渐变主标题/主题横幅
- **3D 圆柱体网络节点**用内嵌 SVG 绘制（见下方模板）
- **树状连线**（一个父框分出多条竖线连到子框）用内嵌 SVG 绘制
- 研究内容区块用 dashed border 虚线框包裹
- **关键对齐规则**：SVG 内圆点/连线 y 坐标必须和相邻 CSS 卡片的垂直中心对齐——做法：CSS 侧栏容器设 `height` = SVG高度，`justify-content: space-between`，每个卡片设固定 `height` + `display:flex; align-items:center`

### draw.io 路线图最低复杂度标准

draw.io 路线图（尤其是模式F）的价值在于**丰富的视觉层次和装饰性**。如果画出来只是简单的色块+箭头，不如直接用 TikZ。

**最低复杂度要求**（不满足则不应该选 draw.io）：
- **层级数量 ≥ 4**：简单的 3 阶段串联用 TikZ 就够了，draw.io 应该用在更复杂的场景
- **视觉元素种类 ≥ 5**：必须包含以下元素中的至少 5 种：
  - 渐变色标题胶囊
  - 左/右侧竖排分区标签
  - 空心描边字
  - 虚线框分组
  - 3D 圆柱体/立体元素
  - 树状连线（父框分叉到多个子框）
  - 散布关键词装饰
  - 编号圆
  - 深色横幅（紫底白字）
  - 箭头形五边形框
  - 汇聚箭头
- **布局层次 ≥ 3 级**：如"分区标签 → 内容卡片 → 卡片内子元素"，不能只有单层平铺
- **连线类型 ≥ 2 种**：如"实线数据流 + 虚线反馈回路"，不能全部用同一种箭头

**对照参考图（10_layered_roadmap.png）的标杆**：
- 6 个层级（研究背景→问题提出→研究框架→主题横幅→研究内容→结论展望）
- 左侧紫色竖排标签 + 右侧灰色竖排标签
- 3D 圆柱体网络节点（GAN/CNN/GRU/RNN/GNN/LSTM）
- 树状连线（父框→子框分叉）
- 空心描边字分区标题
- 深紫渐变横幅
- 散布关键词
- 多研究内容区块并排

**如果用户要求的图内容确实简单（如只有3个阶段4个模块），则应该用 TikZ 而非 draw.io**——draw.io 的优势是装饰性，用它画简单图是大材小用。

### 视觉花样库（从真实参考图总结）

**SVG 3D 圆柱体网络节点**（模式F核心元素）——用于展示 GAN/CNN/RNN 等网络模型：
```html
<!-- 单个3D圆柱体：底面椭圆+侧面矩形+顶面椭圆+文字 -->
<g>
  <ellipse cx="90" cy="42" rx="36" ry="9" fill="#c4b0d8" stroke="#8a6ca6" stroke-width="1"/>
  <rect x="54" y="22" width="72" height="20" fill="#c4b0d8" stroke="none"/>
  <line x1="54" y1="22" x2="54" y2="42" stroke="#8a6ca6" stroke-width="1"/>
  <line x1="126" y1="22" x2="126" y2="42" stroke="#8a6ca6" stroke-width="1"/>
  <ellipse cx="90" cy="22" rx="36" ry="9" fill="#d8ccec" stroke="#8a6ca6" stroke-width="1"/>
  <text x="90" y="36" text-anchor="middle" font-size="12" font-weight="700"
    fill="#4a2070" font-family="sans-serif">GAN</text>
</g>
```
- 结构：底椭圆（深色）→ 侧面矩形（同色无边框）→ 左右竖线 → 顶椭圆（浅色）→ 文字
- 每对节点中间用 `⇔` 符号连接
- 左右两侧用圆点 `<circle r="4">` + 横线 `<line>` 连接到外部侧栏卡片
- **⚠️ SVG 圆点+横线必须精确连接到侧栏卡片**（反复踩坑）：
  - 横线的起点 x = SVG 左/右边界（如 x=0 或 x=SVG宽度）
  - 横线的终点必须**延伸到 SVG 外部**，与相邻 CSS 侧栏卡片的垂直中心在同一 y 坐标
  - 如果横线看起来"没接上"——通常是 SVG viewBox 裁掉了超出范围的线。解决方法：增大 SVG viewBox 宽度，或用 `overflow: visible` 允许线条超出 SVG 边界
  - **每条横线的 y 坐标必须等于对应圆柱体的垂直中心 y**，不能有偏差
- **6色区分**：紫(GAN)、蓝(CNN)、绿(GRU)、橙(RNN)、黄(GNN)、粉红(LSTM)
- 3行×2列布局，行间距约56px，SVG总高170px
- **与CSS侧栏对齐**：相邻 `.rc-side` 容器必须设 `height: 170px`（=SVG高度）+ `justify-content: space-between`，每个 `.rc-side-item` 设 `height: 44px` + `display:flex; align-items:center`

**SVG 树状连线**（模式F核心元素）——一个父框分叉连到多个子框：
```html
<!-- 父框底部中心 → 垂直线 → 水平线 → 3条垂直分支 → 3个子框 -->
<line x1="96" y1="52" x2="96" y2="64" stroke="#999" stroke-width="1"/>
<line x1="26" y1="64" x2="166" y2="64" stroke="#999" stroke-width="1"/>
<line x1="26" y1="64" x2="26" y2="70" stroke="#999" stroke-width="1"/>
<line x1="96" y1="64" x2="96" y2="70" stroke="#999" stroke-width="1"/>
<line x1="166" y1="64" x2="166" y2="70" stroke="#999" stroke-width="1"/>
<!-- 子框 -->
<rect x="2" y="70" width="48" height="26" rx="4" fill="#f5f2ee" stroke="#d0c8c0"/>
```
- 父框中心 x 坐标 = 水平线中点
- 3个子框等间距分布在水平线下方
- 连线颜色 `#999`，stroke-width 1-1.2

**SVG 汇聚箭头**——左右两条线汇聚到中间一点并带向下箭头：
```html
<svg width="680" height="22" viewBox="0 0 680 22">
  <line x1="95" y1="0" x2="95" y2="10" stroke="#999" stroke-width="1.3"/>
  <line x1="95" y1="10" x2="340" y2="10" stroke="#999" stroke-width="1.3"/>
  <line x1="585" y1="0" x2="585" y2="10" stroke="#999" stroke-width="1.3"/>
  <line x1="585" y1="10" x2="340" y2="10" stroke="#999" stroke-width="1.3"/>
  <polygon points="340,18 336,10 344,10" fill="#999"/>
</svg>
```

**空心描边大字**（SVG实现）——科研展示图的常见装饰手法，用于分区标题或栏目标题：
```html
<svg width="44" height="155" viewBox="0 0 44 155">
  <text x="22" y="32" text-anchor="middle" font-size="28" font-weight="900"
    fill="none" stroke="#C2185B" stroke-width="0.7"
    font-family="Microsoft YaHei,PingFang SC,sans-serif">标</text>
  <text x="22" y="68" ...>题</text>
</svg>
```
- **关键参数**：`fill="none"` + `stroke` + `stroke-width`
- **stroke-width 必须控制在 0.6-0.8**，过粗（≥1.2）会导致笔画间隙被填满，字变模糊不清
- **stroke 颜色必须足够深**（如 `#7B1FA2` 或 `#C2185B`），浅色描边（如 `#ccc`）在白色/浅灰背景上几乎不可见
- 字号 26-30 适合分区标题，字号 22-26 适合栏目标题
- **渲染后必须检查空心字可读性**：在截图中缩放到实际显示大小，如果需要凑近看才能辨认，说明字号太小或描边太细
- 字间距（dy）约为字号的 1.2-1.3 倍
- 空心字只用于装饰性标题，正文内容不用

**金黄渐变编号圆**：
```css
.num-circle {
  background: linear-gradient(135deg, #FFD54F, #FFB300);
  border: 3px solid #E65100;
  box-shadow: 0 2px 6px rgba(230,81,0,0.25);
}
```

**左侧粉红竖条装饰**（CSS伪元素）：
```css
.side::before {
  content: '';
  position: absolute;
  left: 6px; top: 0; bottom: 0;
  width: 5px;
  background: linear-gradient(to bottom, #E91E63, #F48FB1);
  border-radius: 3px;
}
```

**深色渐变横幅**（白字，强阴影）——用于一级标题/核心发现：
```css
.banner {
  background: linear-gradient(135deg, #7B1FA2 0%, #9C27B0 40%, #8E24AA 100%);
  color: #fff;
  box-shadow: 0 4px 14px rgba(123,31,162,0.3);
}
```

**悬浮标题胶囊**（深色底白字，浮在卡片顶部）：
```css
.col-card { padding: 30px 12px 14px; position: relative; }
.ct {
  position: absolute;
  top: -4px;  /* 不能太高（-16px会遮挡），保持在卡片顶边附近 */
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #5C6BC0, #7986CB);
  color: #fff;
  white-space: nowrap;
}
```

**带左竖条的标题框**（蓝色/棕色两种风格）：
```html
<div class="titled-box">
  <div class="bar bar-blue"></div>  <!-- 5-6px宽竖条 -->
  <div class="tb-inner tb-blue">智能表面</div>
</div>
```
- 蓝色系：`bar #5C6BC0`, `bg #E8EAF6`, `text #283593`, `border #9FA8DA`
- 棕色系：`bar #8D6E63`, `bg #EFEBE9`, `text #4E342E`, `border #BCAAA4`
- 粉色系（强调）：`bg #FCE4EC`, `text #C2185B`, `border #F48FB1`

**箭头形五边形框**（SVG polygon）——用于流程串联：
```html
<div class="af">
  <svg viewBox="0 0 100 54" preserveAspectRatio="none">
    <!-- 第一个框（无左缺口） -->
    <polygon points="0,2 88,2 99,27 88,52 0,52" fill="#f5f2ee" stroke="#ccc"/>
    <!-- 后续框（有左缺口） -->
    <polygon points="2,2 88,2 99,27 88,52 2,52 13,27" fill="#f0ede6" stroke="#ccc"/>
  </svg>
  <div class="txt">文字内容</div>
</div>
```

**渐变箭头流**（底部总结流程）——用 SVG polygon + linearGradient：
- 粉→蓝→紫渐变，每段有尖角箭头过渡
- 第一段：右侧尖角，左侧平
- 后续段：左右均有尖角/缺口

**流水线圆形节点**：
- 圆形带粉紫渐变：`background: linear-gradient(145deg, #F0E8F5, #E8DDF0)`
- 边框紫色：`border: 2.5px solid #8E6CA8`
- 背景长条：在圆形节点后面加一条渐变长条（opacity 0.25）增加连贯感

**竖排多列内容**（如"卫星遥感/航空遥感/农业遥感"）——**必须用 CSS grid 对齐**：
```css
.tag-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 4px 16px;
  text-align: center;
}
```
禁止用 flex + 自由文字排列——会导致列不对齐。

### 3D 透视梯形绘制模板（模式B核心）

```svg
<!-- 外层梯形（最大，上宽下窄） -->
<polygon points="130,155 730,155 660,650 200,650"
    fill="rgba(245,240,248,0.35)" stroke="#ccc" stroke-width="1.2"/>
<!-- 顶面（3D厚度） -->
<polygon points="130,155 730,155 750,140 150,140"
    fill="rgba(230,220,235,0.2)" stroke="#ccc" stroke-width="0.8"/>
<!-- 左侧面 -->
<polygon points="130,155 150,140 220,635 200,650"
    fill="rgba(220,210,225,0.15)" stroke="#ccc" stroke-width="0.5"/>
<!-- 右侧面 -->
<polygon points="730,155 750,140 680,635 660,650"
    fill="rgba(220,210,225,0.15)" stroke="#ccc" stroke-width="0.5"/>
```

每层内收比例约 8-12%，层间 y 间距约 50-70px。

### XML 骨架

```xml
<mxfile host="app.diagrams.net">
  <diagram name="路线图" id="roadmap">
    <mxGraphModel dx="1422" dy="900" grid="1" gridSize="10"
        guides="1" tooltips="1" connect="1" arrows="1"
        fold="1" page="1" pageScale="1"
        pageWidth="1200" pageHeight="1600" math="0" shadow="1">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 节点和连线 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 常用 style 速查

| 元素 | 关键 style 片段 |
|------|---------------|
| 主标题框 | `rounded=1;fillColor=#FCE4EC;strokeColor=#C2185B;strokeWidth=3;shadow=1;` |
| 深色横幅（紫底白字） | `rounded=1;fillColor=#7B1FA2;strokeColor=#9C27B0;fontColor=#FFFFFF;fontSize=18;fontStyle=1;shadow=1;` |
| 横幅（蓝灰） | `rounded=1;fillColor=#E8EAF6;strokeColor=#7986CB;strokeWidth=2;arcSize=40;` |
| 横幅（紫灰） | `rounded=1;fillColor=#E0D8F0;strokeColor=#A090C0;strokeWidth=2;arcSize=40;` |
| 标题胶囊（蓝底白字） | `rounded=1;fillColor=#5C6BC0;strokeColor=#7986CB;fontColor=#FFFFFF;fontStyle=1;shadow=1;` |
| 标题胶囊（棕色系） | `rounded=1;fillColor=#EFEBE9;strokeColor=#BCAAA4;fontColor=#4E342E;fontStyle=1;` |
| 强调标签（粉色） | `rounded=1;fillColor=#FCE4EC;strokeColor=#F48FB1;fontColor=#C2185B;fontStyle=1;arcSize=30;` |
| 内容卡片 | `rounded=1;fillColor=#FFFFFF;strokeColor=#BDBDBD;shadow=1;` |
| 编号圆（金黄） | `ellipse;fillColor=#FFD54F;strokeColor=#E65100;fontColor=#E65100;fontStyle=1;strokeWidth=3;` |
| 散布关键词（强调色） | `text;html=1;fontColor=【方案强调色】;fontStyle=3;fontSize=9;` |
| 散布关键词（灰） | `text;html=1;fontColor=#888;fontStyle=2;fontSize=9;` |
| 竖排文字 | `text;html=1;horizontal=0;fontSize=10;fontStyle=1;` |
| 入口/出口框 | `rounded=1;fillColor=#FFFFFF;strokeColor=#999;fontSize=12;` |
| 链条圆（粉紫渐变） | `ellipse;fillColor=#F0E8F5;strokeColor=#8E6CA8;fontStyle=1;fontColor=#4A148C;strokeWidth=2;` |
| 链条加号 | `text;fillColor=none;strokeColor=none;fontColor=#E65100;fontSize=20;fontStyle=1;` |
| 链条加号（强调） | `text;fillColor=none;strokeColor=none;fontColor=#C2185B;fontSize=24;fontStyle=1;` |
| 箭头形框 | 用 HTML 的 SVG polygon 实现，draw.io 中用 `shape=mxgraph.arrows2.arrow;` |

### 交付物

每次必须同时交付：
1. **`.drawio` XML 文件**——可在 app.diagrams.net 打开编辑
2. **预览图（PNG）**——用 `drawio -x -f pdf -o output.pdf input.drawio && pdftoppm -png -r 300 output.pdf preview` 导出（draw.io CLI 的 PNG 直出在部分环境有兼容问题，走 PDF 中转更稳定）。如果 `drawio` 命令不可用，提示用户 `brew install --cask drawio`
3. **（可选）`.html` 预览文件**——对于使用 HTML+CSS+SVG 模式（模式A-F）的图，同时交付 HTML 预览

### 评分与迭代（draw.io 模式）

draw.io / HTML 预览图**同样需要评分迭代**，和 TikZ 流程一致。由于 HTML 无法自动编译验证，需要更严格的人工审查。

**评分流程**：生成 HTML 后，逐项对照以下六维度打分（各 1-5 分）：

| 维度 | 检查要点 |
|------|---------|
| 完整性 | 原图/文案中的所有模块、标签、连线是否都已包含，无遗漏 |
| 准确性 | 文字内容正确无误，模块归属关系与原图一致 |
| 布局合理 | 各区域间距均匀，不拥挤不松散，层次分明 |
| 视觉花样 | 是否复刻了原图的装饰元素（空心字、竖条、渐变、阴影、箭头形框等），不能过于素淡 |
| 配色统一 | 同类元素颜色一致，不出现随意配色，整体和谐 |
| 文字可读 | 字号合适、无重叠遮挡、空心字清晰、多列文字对齐 |

**评分规则**：
- **总分 = 30 且无缺陷** → 交付给用户
- **总分 < 30** → 必须继续迭代修复，不展示给用户
- **总分 < 25** → 重大问题，回到分析阶段重新设计

**常见扣分项**（draw.io 模式特有）：
- 空心描边字模糊不清（stroke-width 过粗）→ 文字可读 -2
- 多列竖排文字错位（未用 grid）→ 布局合理 -2
- 悬浮标题遮盖卡片边框或超出容器 → 布局合理 -1
- 缺少原图中的装饰元素（竖条、渐变横幅、箭头框等）→ 视觉花样 -2
- 左侧分区标题字号过大，喧宾夺主 → 文字可读 -1
- 箭头形框尖角方向不统一 → 布局合理 -1
- HTML 在窄屏下溢出 → 布局合理 -1

**紧凑度是模式F的核心要求**——学术路线图应信息密度高、空间利用率高。以下间距参考值（基于参考图 10_layered_roadmap.png 实测）：
- 层级之间间距：8-12px（不要超过 15px）
- 卡片内 padding：6-10px（不要超过 14px）
- 行间 gap：6-8px
- 侧栏与内容区间距：4-6px
- 研究内容虚线框内 padding：8-12px
- **如果渲染后发现大面积留白，首先缩减 padding/margin/gap，而非增加内容填充**

**常见扣分项**（模式F 分层技术路线图特有）：
- SVG 圆柱体圆点与侧栏卡片垂直不对齐 → 布局合理 -2
- 3D 圆柱体缺少顶面椭圆（看起来像扁平矩形而非立体） → 视觉花样 -2
- 树状连线的水平分叉线不居中或子框间距不均 → 布局合理 -1
- 参考图无底部数据库圆柱却多画了（过度添加元素） → 准确性 -1
- 左右侧栏宽度不统一或竖排文字溢出 → 布局合理 -1
- 紧凑模式下仍有大面积空白（padding/margin 未缩减）→ 布局合理 -1

**迭代要求**：
- 每次修改后说明改了什么
- 针对扣分项精确修复，最小化改动
- 如果用户提供了截图反馈，优先修复截图中指出的问题

### draw.io XML 连线最佳实践（与 TikZ 的关键差异）

draw.io XML 模式下的连线规则**不同于 TikZ**，以下是专项指导：

**orthogonalEdgeStyle 自动路由**：
- draw.io 的 `orthogonalEdgeStyle` 会自动寻路，但只在节点不密集时效果好
- 当多条连线汇聚到同一节点时，自动路由可能产生重叠——此时需用 `exitX/exitY/entryX/entryY` 精确控制出入点
- **禁止手动 waypoints 穿越框体**：即使 waypoint 坐标在框体内部，orthogonalEdgeStyle 也不会绕开——它只按 waypoints 走

**连线不穿越分组框和文字**（最常见问题）：
- 跨分组的连线必须从源节点的边缘出发（如 `exitY=1` 表示从底部出），经过分组间的 gap 区域，再进入目标分组
- **分组间 gap ≥ 60px**（推荐 80px）：gap 太窄会导致连线标签和分组框重叠
- 跨分组连线的中转 waypoint 的 y 坐标必须在 gap 区域内（源分组底部 y < waypoint y < 目标分组顶部 y）
- **连线不能穿过任何文字标签**——包括节点内文字、分组框标题、连线标签。渲染后逐条检查每条连线路径上是否有文字被遮挡
- **连线标签不能骑在节点文字上**——标签只放在连线经过空白区域的段上

**扇出/汇聚连线**：
- 多条线从同一节点出发时，使用不同的 `exitX` 值（如 0.2, 0.5, 0.8）分散出口，避免所有线从同一点出发
- 汇聚到同一节点时同理，使用不同的 `entryX` 值
- **禁止**多条线共享同一 rail y 坐标——至少错开 15-20px

**反馈回路走框外**：
- 反馈回路（从下层回到上层）必须走分组框外侧（x > 分组框右边界 + 20px）
- 分组框右边界需预留反馈回路空间，pageWidth 相应增加

**文字溢出防护**：
- 节点 width 必须 ≥ 文字估算宽度 + 20px 余量（英文约 7px/字符，中文约 14px/字符）
- 长标签用 `whiteSpace=wrap;html=1;` 允许自动换行
- 中英文混合标签统一用"英文\n中文注释"格式或全部用括号混排，整图一致

**draw.io 渐变色**（与 CSS 不同）：
- draw.io XML 不支持 CSS `linear-gradient`，必须用原生属性：
  ```
  fillColor=#5C6BC0;gradientColor=#9575CD;gradientDirection=south;
  ```
- `gradientDirection` 可选值：`south`（默认，上→下）、`east`（左→右）、`north`（下→上）、`west`（右→左）
- 双色渐变：`fillColor` = 起始色，`gradientColor` = 结束色

**画图指令中的 rail 分配对 draw.io 不完全适用**：
- TikZ 需要精确的 rail x 坐标，但 draw.io 的 orthogonalEdgeStyle 会自动路由
- 在 draw.io 画图指令中，将"rail 分配"替换为"连线出入点分配"——明确每条线的 exitX/exitY/entryX/entryY

### 自检

- HTML 预览在浏览器中布局正常，无溢出/错位
- SVG 梯形的坐标逐层内收，视觉上形成透视感
- 散布关键词不压盖核心文字
- 侧栏竖排文字与中心嵌套等高对齐
- draw.io XML 层级完整，id 唯一
- 配色一致（HTML 和 drawio 用同一套颜色值）
- **空心描边字清晰可读**：stroke-width ≤ 0.8，字号 ≥ 26，笔画间隙明显可见
- **左侧分区标题字号适中**：不能比右侧内容区主标题更大，通常 font-size 26-30
- **多列竖排内容用 grid 对齐**：禁止 flex 自由排列导致列错位
- **箭头形框的尖角方向统一**：第一个框左平右尖，后续框左凹右尖
- **视觉花样丰富度**：检查是否包含了参考图中的装饰元素（竖条、渐变、阴影、空心字等），避免输出过于素淡

### draw.io XML 结构验证（编译替代方案）

draw.io 无法像 TikZ 一样自动编译验证，需手动检查：
1. **XML 合法性**：`xmllint --noout file.drawio` 检查语法
2. **ID 唯一性**：检查所有 mxCell 的 id 不重复
3. **坐标重叠检测**：检查两个非父子关系节点的矩形区域是否重叠（x, y, width, height）
4. **连线完整性**：所有 edge 的 source 和 target 均指向存在的节点 id
5. **文字溢出估算**：节点 width ≥ 文字长度估算 + 20px
6. **分组间 gap**：相邻分组框之间间距 ≥ 60px
7. **连线不穿越分组**：跨分组连线的 waypoint y 坐标在 gap 区域内

### 自检清单（draw.io XML 通用）

- [ ] xmllint 验证通过，ID 唯一
- [ ] **所有节点 width ≥ 文字估算宽度 + 20px**
- [ ] **分组间 gap ≥ 60px**（推荐 80px）
- [ ] 跨分组连线的 waypoint y 在 gap 区域内
- [ ] 反馈回路走分组框外侧
- [ ] 渐变色用 `fillColor` + `gradientColor` + `gradientDirection`（非 CSS gradient）
- [ ] 全局 shadow 与节点级 shadow 不冲突（散布文字等装饰节点不应有阴影）
- [ ] 连线数量与画图指令一致
- [ ] 中英文混合标签格式统一（全部用同一种格式）
- [ ] **渲染后视觉审查**（必须用 drawio 导出 PNG 后查看）：
  - [ ] 所有连线标签在导出的 PNG 中可读（字号 ≥ 11px）
  - [ ] 反馈回路标签清晰可辨，不被框体遮挡
  - [ ] 整图纵横比 ≤ 1:2（过长则增加 pageWidth 或压缩 pageHeight）
  - [ ] **紧凑度**：各区域间距是否过大？是否存在大面积留白？学术配图应紧凑饱满
  - [ ] 阶段间连线走向自然，无不必要的折线

### 自检清单（模式F 分层技术路线图专用）

- [ ] 左侧紫色竖排标签与右侧灰色竖排标签等高对齐
- [ ] SVG 3D 圆柱体的圆点 y 坐标与相邻 CSS 侧栏卡片垂直中心对齐（最常见错位问题）
- [ ] 侧栏卡片容器设 `height` = SVG高度，用 `justify-content: space-between` 均分
- [ ] 树状连线的父框中心 x = 水平分叉线中点，子框等间距分布
- [ ] 汇聚箭头左右两条线的起点 x 坐标分别对齐上方左右列的中心
- [ ] 论文主题横幅横跨整个中心区，两侧标签（多学科/跨模态）用 `position:absolute` 定位
- [ ] 研究内容虚线框内三栏（左侧栏+SVG中心+右侧栏）垂直居中对齐
- [ ] 两个研究内容区块之间有下箭头过渡
- [ ] 结论展望区的3个卡片等宽等高
- [ ] **紧凑但不挤压**——间距刚好能区分层次，但**不能因为追求紧凑导致元素重叠**。检查：
  - 每个框/卡片与上方元素之间至少有 4px 间隙（不能贴在一起或重叠）
  - 标题胶囊如果用 `position:absolute; top:-Npx` 悬浮，不能遮挡上方区域的内容
  - 编号圆/标签与相邻文字不重叠
