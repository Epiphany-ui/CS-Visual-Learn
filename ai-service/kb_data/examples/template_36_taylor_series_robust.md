# 意图：使用标准的非递归方式展示泰勒级数展开。通过阶乘累加函数构建多项式，避免使用任何递归闭包。
# 关键词：泰勒级数, 泰勒展开, sin(x), 多项式逼近, math.factorial

下面是完整的 Manim 代码示例：
```python
from manim import *
import math

class RobustTaylorSeries(Scene):
    def construct(self):
        axes = Axes(x_range=[-4, 4], y_range=[-2, 2], axis_config={"include_numbers": False})
        sin_graph = axes.plot(lambda x: np.sin(x), color=BLUE, stroke_width=4)
        
        # 定义非递归的泰勒级数计算函数
        def taylor_sin(x, n):
            res = 0
            for i in range(n + 1):
                res += ((-1)**i * x**(2*i+1)) / math.factorial(2*i+1)
            return res

        # 初始逼近
        curr_graph = axes.plot(lambda x: taylor_sin(x, 0), color=GREEN, stroke_width=4)
        self.add(axes, sin_graph, curr_graph)

        # 动态逼近阶数 1, 3, 5
        for n in [1, 3, 5]:
            next_graph = axes.plot(lambda x: taylor_sin(x, n), color=GREEN, stroke_width=4)
            self.play(Transform(curr_graph, next_graph), run_time=1)
            self.wait(0.5)
        self.wait(2)