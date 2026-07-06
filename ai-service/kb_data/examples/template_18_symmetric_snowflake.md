# 意图：绘制复杂的六角对称雪花图案，演示利用循环旋转（rotate）与关于点对称（about_point）实现高级几何艺术排版。
# 关键词：雪花, 晶体, 六角对称, 旋转复用, VGroup, Line, rotate, about_point, LaggedStart

下面是完整的 Manim 代码示例：
```python
from manim import *

class MathematicalSnowflake(Scene):
    def construct(self):
        # 1. 核心设计：先构建雪花的“单个标准分支”
        single_branch = VGroup()
        
        # 绘制主骨架线（从原点向上延伸）
        main_bone = Line(ORIGIN, UP * 3, stroke_width=4, color=WHITE)
        single_branch.add(main_bone)
        
        # 批量添加侧边的小冰晶分叉（利用循环和镜像坐标）
        for h in [1.0, 1.8, 2.4]:  # 分叉在主干上的不同高度
            scale_factor = (3.0 - h) / 3.0  # 越靠近顶端，分叉越短
            left_sub = Line(
                UP * h, 
                UP * h + LEFT * 0.7 * scale_factor + UP * 0.4 * scale_factor, 
                stroke_width=3, 
                color=WHITE
            )
            right_sub = Line(
                UP * h, 
                UP * h + RIGHT * 0.7 * scale_factor + UP * 0.4 * scale_factor, 
                stroke_width=3, 
                color=WHITE
            )
            single_branch.add(left_sub, right_sub)

        # 2. 🌟 矩阵灵魂：将单个分支复制并旋转6次，完美形成六角对称雪花
        # 60度 = 360 / 6
        snowflake_group = VGroup()
        for i in range(6):
            rotated_branch = single_branch.copy()
            # 关键：绕原点 (ORIGIN) 旋转对应的角度
            rotated_branch.rotate(i * 60 * DEGREES, about_point=ORIGIN)
            snowflake_group.add(rotated_branch)

        # 3. 增强视觉质感：加入一个中心冰核
        center_core = RegularPolygon(n=6, radius=0.3, color=BLUE_A, fill_opacity=0.3)
        snowflake_group.add(center_core)
        
        snowflake_group.move_to(ORIGIN).scale(1.2)

        # 4. 炫酷的逐层生长入场动画
        self.play(
            LaggedStart(
                *[Create(branch) for branch in snowflake_group], 
                lag_ratio=0.15
            ), 
            run_time=3
        )
        # 让雪花平滑自转两圈，充满动态呼吸感
        self.play(snowflake_group.animate.rotate(120 * DEGREES), run_time=3, rate_func=linear)
        self.wait(1)