# 意图：绘制标准几何图形（如等边三角形、正多边形、矩形、圆环），必须使用原生几何对象，禁止使用 Polygon 手写坐标。
# 关键词：等边三角形, 正多边形, 矩形, 圆环, Triangle, RegularPolygon, Rectangle, Annulus

下面是完整的 Manim 代码示例：
```python
from manim import *

class StandardShapes(Scene):
    def construct(self):
        # 1. 创建标准等边三角形（禁止用 Polygon 算坐标）
        triangle = Triangle(color=BLUE, fill_opacity=0.3)
        
        # 2. 创建正六边形
        hexagon = RegularPolygon(n=6, color=GREEN, fill_opacity=0.3)
        
        # 3. 创建圆环
        ring = Annulus(inner_radius=0.5, outer_radius=1.0, color=RED)
        
        # 自动排版并居中
        group = VGroup(triangle, hexagon, ring).arrange(RIGHT, buff=0.8).move_to(ORIGIN)
        
        self.play(LaggedStartMap(Create, group, lag_ratio=0.2), run_time=2)
        self.wait(1)