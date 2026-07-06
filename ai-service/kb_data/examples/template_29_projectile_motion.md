---

#### 📦 29. 经典力学：平抛/斜抛运动的抛物线轨迹
**文件建议命名：** `template_29_projectile_motion.md`

```markdown
# 意图：展示物理学中的斜抛运动。一个小球带着初始仰角和速度射出，在重力作用下划过一条完美的抛物线，并留下实时拖尾。
# 关键词：斜抛运动, 抛物线, 重力加速度, 运动学, TracedPath, shift, ValueTracker

下面是完整的 Manim 代码示例：
```python
from manim import *
import numpy as np

class ProjectileMotion(Scene):
    def construct(self):
        # 1. 初始化地面和发射质点
        ground = Line(LEFT * 6 + DOWN * 3, RIGHT * 6 + DOWN * 3, color=GREEN)
        ball = Dot(color=YELLOW, radius=0.2).move_to(LEFT * 5 + DOWN * 2.8)
        
        # 2. 挂载动态彩色拖尾
        trail = TracedPath(ball.get_center, stroke_color=ORANGE, stroke_width=4, dissipating_time=1.5)
        self.add(ground, trail, ball)

        # 3. 初始化斜抛物理参数
        self.v_x = 2.5       # 水平分速度 (恒定)
        self.v_y = 5.5       # 竖直分速度 (受重力影响)
        gravity = -9.8       # 重力加速度

        # 4. 物理刷新器（严禁在内部调 .animate！）
        def update_projectile(mob, dt):
            # 速度更新：v_y = v_y + g * dt
            self.v_y += gravity * dt
            # 位移更新
            mob.shift(np.array([self.v_x * dt, self.v_y * dt, 0]))
            
            # 边界碰撞检测：如果掉落到地面以下，停止运动
            if mob.get_y() <= -2.8:
                mob.set_y(-2.8)
                mob.clear_updaters()

        # 5. 绑定更新器并执行
        ball.add_updater(update_projectile)
        
        # 持续观察 2.5 秒的抛物线飞行
        self.wait(2.5)
        ball.clear_updaters()
        self.wait(1)