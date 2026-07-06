---

### 📦 3. 文字与公式的高级形变与渐变排版 (Typography & Morphing)
**文件建议命名：** `template_03_text_morphing.md`

```markdown
# 意图：展示文字的平滑变大、颜色渐变，以及多行数学公式的动态推导对齐（TransformMatchingTex 的高级用法）。
# 关键词：文字, 放大, 颜色渐变, 公式推导, TransformMatchingTex, scale, set_color_by_gradient

下面是完整的 Manim 代码示例：
```python
from manim import *

class TextAndFormulaMorphing(Scene):
    def construct(self):
        # 1. 高级文字形变与色彩渲染
        title = Text("Manim 动力学", font_size=48, weight=BOLD)
        self.play(Write(title))
        
        # 平滑放大并应用彩虹渐变色
        self.play(
            title.animate.scale(1.5).set_color_by_gradient(RED, YELLOW, GREEN, BLUE),
            run_time=1.5
        )
        # 将标题移至顶部
        self.play(title.animate.to_edge(UP))

        # 2. 复杂公式的智能匹配形变
        # 初始展开公式
        eq_start = MathTex("(a+b)^2", "=", "a^2", "+", "2ab", "+", "b^2")
        eq_start.set_color_by_tex("a", RED).set_color_by_tex("b", BLUE)
        
        # 目标合并公式（注意符号的字符串切分必须与上文对应，才能触发智能飞行轨迹）
        eq_end = MathTex("(a+b)^2", "-", "2ab", "=", "a^2", "+", "b^2")
        eq_end.set_color_by_tex("a", RED).set_color_by_tex("b", BLUE)

        # 渲染初始公式
        self.play(FadeIn(eq_start, shift=UP))
        self.wait(1)

        # 3. 执行智能公式变换：2ab 会平滑飞过等号并变成 -2ab
        self.play(TransformMatchingTex(eq_start, eq_end), run_time=2)
        
        # 4. 整体外发光/高亮强调
        box = SurroundingRectangle(eq_end, color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait(1)
