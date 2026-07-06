---

### 📦 23. 图论算法：二叉树与搜索路径 (Binary Tree)
**文件建议命名：** `template_23_binary_tree_search.md`

```markdown
# 意图：利用 Graph 对象和 tree 布局绘制一棵完美的二叉树，并动态高亮从根节点到叶子节点的搜索路径（如二分查找）。
# 关键词：二叉树, 树, 搜索, 路径高亮, Graph, layout="tree", edges

下面是完整的 Manim 代码示例：
```python
from manim import *

class BinaryTreeSearch(Scene):
    def construct(self):
        # 1. 定义二叉树的节点和父子关系边
        vertices = [10, 5, 15, 2, 7, 12, 20]
        edges = [(10, 5), (10, 15), (5, 2), (5, 7), (15, 12), (15, 20)]

        # 2. 创建 Graph，指定为 tree 布局，并设定 10 为根节点
        tree = Graph(
            vertices, 
            edges, 
            layout="tree", 
            root_vertex=10,
            vertex_config={"radius": 0.4, "color": BLUE, "fill_opacity": 1},
            edge_config={"color": WHITE, "stroke_width": 2},
            labels={v: Text(str(v), font_size=24) for v in vertices}
        )
        
        # 将整棵树向上移动一点
        tree.move_to(UP * 0.5)
        self.play(Create(tree), run_time=2)
        self.wait(1)

        # 3. 模拟寻找节点 7 的动画过程：10 -> 5 -> 7
        search_path = [10, 5, 7]
        
        # 创建一个空心圆圈作为追踪高亮框
        highlighter = Circle(radius=0.5, color=YELLOW, stroke_width=5)
        
        # 移动到根节点并显现
        highlighter.move_to(tree.vertices[search_path[0]].get_center())
        self.play(Create(highlighter))
        self.wait(0.5)

        # 遍历搜索路径
        for i in range(1, len(search_path)):
            current_node = search_path[i-1]
            next_node = search_path[i]
            
            # 高亮走过的连线
            self.play(tree.edges[(current_node, next_node)].animate.set_color(YELLOW), run_time=0.5)
            
            # 追踪框跳跃到下一个节点
            self.play(highlighter.animate.move_to(tree.vertices[next_node].get_center()), run_time=0.5)
            
            # 高亮当前节点
            self.play(tree.vertices[next_node].animate.set_color(ORANGE), run_time=0.5)
            self.wait(0.5)