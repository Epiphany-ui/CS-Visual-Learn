---

### 📦 25. 物理进阶：动态向量场 (Vector Field)
**文件建议命名：** `template_25_vector_field.md`

```markdown
# 意图：可视化空间中的电磁场或流体场。使用 ArrowVectorField 绘制满屏的向量箭头，并让它们根据时间函数发生动态旋转与流动。
# 关键词：向量场, 电磁场, 流体, 箭头场, ArrowVectorField, np.sin, np.cos

下面是完整的 Manim 代码示例：
```python
from manim import *

class DynamicVectorField(Scene):
    def construct(self):
        # 1. 定义一个基于空间坐标 (x, y) 和时间 (t) 的二维向量场函数
        def field_func(pos):
            x, y = pos[0], pos[1]
            # 例如：一个产生旋涡和流动的非线性场
            return np.array([
                np.sin(y) - np.cos(x),
                np.cos(y) + np.sin(x),
                0
            ])

        # 2. 创建向量场对象
        vector_field = ArrowVectorField(
            field_func,
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            colors=[BLUE, YELLOW, RED] # 箭头根据长度自动应用颜色渐变
        )
        
        self.play(Create(vector_field), run_time=3)
        self.wait(1)

        # 3. 进阶：如果需要让场“动”起来，可以让原函数加上随时间偏移的值
        time_tracker = ValueTracker(0)

        def dynamic_field_func(pos):
            t = time_tracker.get_value()
            x, y = pos[0], pos[1]
            # 引入时间变量 t 让旋涡移动
            return np.array([
                np.sin(y + t) - np.cos(x - t),
                np.cos(y - t) + np.sin(x + t),
                0
            ])

        # 为向量场添加更新器，使其每帧根据新的时间重绘箭头方向
        vector_field.add_updater(lambda f: f.become(
            ArrowVectorField(
                dynamic_field_func, 
                x_range=[-7, 7, 1], y_range=[-4, 4, 1], 
                colors=[BLUE, YELLOW, RED]
            )
        ))

        # 播放时间线
        self.play(time_tracker.animate.set_value(3), run_time=4, rate_func=linear)
        
        vector_field.clear_updaters()