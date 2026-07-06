
---

### 📦 模板 2：高阶公式推导与局部颜色高亮
这个模板是解决大模型“公式渲染失败”的杀手锏。它教会大模型如何使用 `MathTex` 并根据子字符串独立上色。

```markdown
# 意图：展示数学公式，为公式中的特定变量设置不同颜色，并进行等式推导动画
# 关键词：公式, 数学, 颜色, 推导, MathTex, set_color_by_tex, TransformMatchingTex, VGroup

下面是完整的 Manim 代码示例：
```python
from manim import *

class MathFormulaDerivation(Scene):
    def construct(self):
        # 1. 创建初始公式，双斜杠转义LaTeX符号
        eq1 = MathTex("a^2", "+", "b^2", "=", "c^2")
        
        # 为公式中的特定部分染色（必须和上面的字符串切分匹配）
        eq1.set_color_by_tex("a^2", RED)
        eq1.set_color_by_tex("b^2", BLUE)
        eq1.set_color_by_tex("c^2", YELLOW)

        # 2. 创建推导后的目标公式
        eq2 = MathTex("c^2", "-", "a^2", "=", "b^2")
        eq2.set_color_by_tex("a^2", RED)
        eq2.set_color_by_tex("b^2", BLUE)
        eq2.set_color_by_tex("c^2", YELLOW)
        
        # 将新公式往下平移
        eq2.next_to(eq1, DOWN, buff=1)

        # 3. 动画序列
        self.play(Write(eq1))
        self.wait(1)
        # TransformMatchingTex 可以根据相同的字符串实现聪明的字母飞行动画
        self.play(TransformMatchingTex(eq1.copy(), eq2), run_time=2)
        self.wait(1)