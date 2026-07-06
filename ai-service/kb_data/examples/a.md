# Manim 核心动画设计指南

## 1. 颜色规范
如果标准颜色（如 RED, BLUE, GREEN）无法满足需求，或者需要特殊颜色（如棕色 BROWN），禁止自作聪明替换，必须使用自定义十六进制 Hex 颜色代码：
- 棕色：Circle(color="#8B4513")

## 2. 动画组合禁忌
绝对禁止在同一个 `self.play()` 中对【同一个物体】同时使用具有重叠效果的入场动画（例如 `Create` 和 `FadeIn`、`GrowFromCenter` 和 `Write`）。

### 正确的动画组合示例（前后顺序）：
```python
# 先画出圆的轮廓，再将圆填充颜色并淡入
circle = Circle(color="#8B4513", stroke_width=4)
self.play(Create(circle))
self.play(circle.animate.set_fill("#8B4513", opacity=0.5))
```
正确的并发动画示例（不同物体）：
```Python
# 圆和文字同时出现是允许的
self.play(Create(circle), Write(text))
```

---

### ✨ 优化后的正确代码

如果按照上面的规范，这段代码应该被改写成这样，视觉效果才会真正惊艳：

```python
from manim import *

class BrownCircle(Scene):
    def construct(self):
        # 1. 使用 Hex 代码定义真正的棕色，并加入渐变和填充质感
        brown_circle = Circle(
            radius=2,
            color="#8B4513",       # 真正的棕色
            stroke_width=5,        # 轮廓线条加粗
            fill_color="#A0522D",  # 稍浅一点的棕色填充
            fill_opacity=0.6       # 设置半透明，非常有质感
        )
        brown_circle.shift(LEFT * 1.5)

        # 2. 优雅的入场：先画出轮廓，再渐变展示出中间的填充色
        # 创建文字
        title = Text("棕色的圆", font_size=40, color=WHITE).next_to(brown_circle, RIGHT, buff=1)
        
        # 3. 播放动画：线画圆，同时写字，最后整体展示
        self.play(
            Create(brown_circle, run_time=1.5), 
            Write(title, run_time=1.5)
        )
        # 轮廓画完后，平滑地把不透明度从 0 变成 0.6
        self.play(brown_circle.animate.set_fill(opacity=0.6), run_time=1)
        self.wait(1)