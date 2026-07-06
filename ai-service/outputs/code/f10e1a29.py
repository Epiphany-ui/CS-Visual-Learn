from manim import *

class BinarySearchDemo(Scene):
    def construct(self):
        # ---------- 构建二叉搜索树 ----------
        # 节点值及位置（手动布局）
        values = [8, 3, 10, 9, 13]
        pos = {
            8:  ORIGIN,
            3:  LEFT * 2 + DOWN * 1.5,
            10: RIGHT * 2 + DOWN * 1.5,
            9:  RIGHT * 1 + DOWN * 3,
            13: RIGHT * 3 + DOWN * 3,
        }

        # 创建节点（圆形 + 数字文本）
        nodes = {}
        for val in values:
            circle = Circle(radius=0.4, fill_color=BLUE, fill_opacity=0.6, stroke_color=WHITE)
            text = Text(str(val), font_size=24, color=WHITE).move_to(circle.get_center())
            node = VGroup(circle, text)                 # 每个节点是一个VGroup
            node.move_to(pos[val])
            nodes[val] = node

        # 连线（父节点 -> 子节点）
        edges = VGroup()
        # 8 -> 3
        edges.add(Line(pos[8], pos[3], color=GREY_B, stroke_width=2))
        # 8 -> 10
        edges.add(Line(pos[8], pos[10], color=GREY_B, stroke_width=2))
        # 10 -> 9
        edges.add(Line(pos[10], pos[9], color=GREY_B, stroke_width=2))
        # 10 -> 13
        edges.add(Line(pos[10], pos[13], color=GREY_B, stroke_width=2))

        # 所有节点组合（用于一次性创建）
        all_nodes = VGroup(*nodes.values())
        tree = VGroup(edges, all_nodes)

        # ---------- 动画：画出整棵树 ----------
        self.play(Create(tree), run_time=2)
        self.wait(0.8)

        # ---------- 搜索数值 13 ----------
        # 步骤1：比较根节点 8
        self.play(nodes[8][0].animate.set_color(YELLOW), run_time=0.5)
        self.wait(0.4)
        # 步骤2：比较右子节点 10
        self.play(nodes[10][0].animate.set_color(YELLOW), run_time=0.5)
        self.wait(0.4)
        # 步骤3：比较右子节点 13（找到目标）
        self.play(nodes[13][0].animate.set_color(GREEN), run_time=0.5)
        self.wait(0.4)
        # 闪烁表示找到
        self.play(Flash(nodes[13][0].get_center(), color=GREEN, line_length=1.2, flash_radius=0.8), run_time=0.6)
        self.wait(0.5)

        # 保持画面一小段时间后结束
        self.wait(1)