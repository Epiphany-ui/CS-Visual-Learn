
---

### 📦 6. 计算机科学：图论与网络拓扑可视化 (Graph Theory)
**文件建议命名：** `template_06_graph_network.md`

```markdown
# 意图：使用 Manim 专门的 Graph 对象可视化网络拓扑结构。演示如何自定义节点、连线样式，以及如何动态改变节点的布局（Layout）。
# 关键词：图论, 节点, 边, 网络拓扑, 布局变换, Graph, layout, change_layout

下面是完整的 Manim 代码示例：
```python
from manim import *

class GraphNetworkTopology(Scene):
    def construct(self):
        # 1. 定义图的顶点和边
        vertices = [1, 2, 3, 4, 5, 6]
        edges = [(1, 2), (1, 3), (2, 4), (3, 4), (4, 5), (5, 6), (6, 1)]

        # 2. 创建 Graph 对象，初始使用 spring (弹簧模型) 布局
        g = Graph(
            vertices, 
            edges, 
            layout="spring",
            layout_scale=3,
            vertex_config={"radius": 0.3, "color": TEAL, "fill_opacity": 1},
            edge_config={"color": GRAY, "stroke_width": 2}
        )

        # 为节点添加文本标签
        labels = {v: Text(str(v), font_size=24) for v in vertices}
        # 将标签强行覆盖到顶点上
        g_with_labels = Graph(
            vertices, edges, layout="spring", layout_scale=3,
            labels=labels
        )

        self.play(Create(g_with_labels), run_time=2)
        self.wait(1)

        # 3. 核心功能：平滑变换图的拓扑布局
        # 将布局从杂乱的弹簧模型变换为规整的圆形布局 (circular)
        self.play(g_with_labels.animate.change_layout("circular"), run_time=2)
        self.wait(1)

        # 再次变换为树状结构布局 (tree)，指定 1 为根节点
        self.play(g_with_labels.animate.change_layout("tree", root_vertex=1), run_time=2)
        self.wait(1)