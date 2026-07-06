---

### 📦 9. 向量加法与平行四边形法则 (Vector Addition)
**文件建议命名：** `template_09_vector_addition.md`

```markdown
# 意图：通过几何图形（平行四边形法则）演示两个向量相加的过程，绘制虚线辅助线并平移向量。
# 关键词：向量加法, 平行四边形法则, 辅助线, Vector, DashedLine, Arrow, put_start_and_end_on

下面是完整的 Manim 代码示例：
```python
from manim import *

class VectorAddition(Scene):
    def construct(self):
        # 1. 设置底层网格并定义坐标点
        plane = NumberPlane()
        self.add(plane)

        coord_v = np.array([3, 1, 0])
        coord_w = np.array([-1, 2, 0])
        coord_sum = coord_v + coord_w

        # 2. 创建初始向量 v 和 w
        vec_v = Arrow(ORIGIN, coord_v, buff=0, color=YELLOW)
        vec_w = Arrow(ORIGIN, coord_w, buff=0, color=BLUE)
        
        label_v = MathTex(r"\vec{v}", color=YELLOW).next_to(vec_v.get_end(), RIGHT)
        label_w = MathTex(r"\vec{w}", color=BLUE).next_to(vec_w.get_end(), LEFT)

        self.play(GrowArrow(vec_v), GrowArrow(vec_w), Write(label_v), Write(label_w))

        # 3. 演示平移 w 到 v 的尾部 (平行四边形的一条边)
        vec_w_copy = vec_w.copy().set_opacity(0.5)
        self.play(vec_w_copy.animate.shift(coord_v), run_time=1.5)

        # 绘制平移轨迹辅助线
        dashed_line_1 = DashedLine(coord_w, coord_sum, color=YELLOW_A)
        dashed_line_2 = DashedLine(coord_v, coord_sum, color=BLUE_A)
        self.play(Create(dashed_line_1), Create(dashed_line_2))

        # 4. 绘制结果向量 v + w
        vec_sum = Arrow(ORIGIN, coord_sum, buff=0, color=GREEN)
        label_sum = MathTex(r"\vec{v} + \vec{w}", color=GREEN).next_to(vec_sum.get_end(), UP)

        self.play(GrowArrow(vec_sum), Write(label_sum))
        self.wait(2)