---

### 📦 模板 3：坐标系绘制与函数微积分面积
这个模板专门对付物理和高数需求。教会大模型使用现代化的 `Axes` 而不是已经被废弃的 `GraphScene`。

```markdown
# 意图：构建二维直角坐标系，绘制正弦曲线，并填充曲线下方的微积分面积
# 关键词：坐标系, 函数, 曲线, 面积, 积分, Axes, plot, get_area

下面是完整的 Manim 代码示例：
```python
from manim import *

class CalculusAreaGraph(Scene):
    def construct(self):
        # 1. 创建直角坐标系
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 1],
            axis_config={"color": BLUE},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        # 2. 绘制数学函数曲线 (如 np.sin)
        graph = axes.plot(lambda x: np.sin(x), color=YELLOW)
        
        # 3. 获取曲线下方的积分面积 (x=2 到 x=8)
        area = axes.get_area(graph, x_range=(2, 8), color=OPACITY, opacity=0.5)

        # 4. 依次播放动画
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(graph), run_time=2)
        self.play(FadeIn(area), run_time=1)
        self.wait(1)