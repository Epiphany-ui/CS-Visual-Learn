---

### 📦 7. 高级 Updater：跟随轨迹的拖尾粒子系统 (Particle Trails)
**文件建议命名：** `template_07_particle_trail.md`

```markdown
# 意图：创建一个沿复杂数学轨迹（如李萨如曲线）运动的质点，并利用 TracedPath 为其生成一条带有颜色渐变的平滑拖尾特效。
# 关键词：轨迹, 质点运动, 拖尾, 路径追踪, TracedPath, MoveAlongPath, ValueTracker

下面是完整的 Manim 代码示例：
```python
from manim import *

class TracedPathParticle(Scene):
    def construct(self):
        # 1. 绘制一条复杂的参数路径（李萨如曲线）
        curve = ParametricFunction(
            lambda t: np.array([
                3 * np.sin(2 * t),
                2 * np.sin(3 * t),
                0
            ]),
            t_range=[0, 2 * PI],
            color=DARK_GRAY,
            stroke_width=2
        ).set_opacity(0.3)  # 背景辅助线调暗
        
        self.add(curve)

        # 2. 创建运动质点
        dot = Dot(color=YELLOW, radius=0.15)
        # 初始移动到曲线的起点
        dot.move_to(curve.get_start())

        # 3. 核心：创建追踪拖尾 (TracedPath)
        # 该对象会自动记录 dot 的轨迹，并生成一条线
        trail = TracedPath(
            dot.get_center, 
            stroke_width=4, 
            stroke_color=YELLOW, 
            dissipating_time=0.8 # 拖尾逐渐消散的时间，产生彗星划过的效果
        )

        self.add(trail, dot)

        # 4. 播放动画：让质点沿着曲线运动
        # rate_func=linear 保证匀速运动，不卡顿
        self.play(MoveAlongPath(dot, curve), run_time=4, rate_func=linear)
        self.wait(1)