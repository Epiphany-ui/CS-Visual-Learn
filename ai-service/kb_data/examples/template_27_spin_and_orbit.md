---

#### 📦 27. 刚体动力学：自转与公转的复合运动
**文件建议命名：** `template_27_spin_and_orbit.md`

```markdown
# 意图：展示天体物理中的复合运动——一个正方形在围绕中心点进行“公转”的同时，自身还在进行高速“自转”。
# 关键词：自转, 公转, 复合运动, 组合动画, Rotate, square

下面是完整的 Manim 代码示例：
```python
from manim import *

class SpinAndOrbit(Scene):
    def construct(self):
        # 1. 创建中心天体（太阳）和运动天体（方块行星）
        sun = Dot(color=YELLOW, radius=0.4)
        planet = Square(side_length=0.6, color=ORANGE, fill_opacity=0.8)
        
        # 初始平移行星到公转轨道半径
        planet.move_to(RIGHT * 3)
        self.add(sun, planet)

        # 2. 核心功能：在同一个 self.play 中并发执行公转与自转
        # Rotate 默认绕自身中心旋转（自转）
        # Rotate 指定 about_point 绕外部点旋转（公转）
        self.play(
            Rotate(planet, angle=2 * TAU, about_point=ORIGIN, rate_func=linear),  # 公转 2 圈
            Rotate(planet, angle=8 * TAU, rate_func=linear),                     # 自身高速自转 8 圈
            run_time=6
        )
        self.wait(1)