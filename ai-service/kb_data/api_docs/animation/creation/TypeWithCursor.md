# TypeWithCursor

**合格名称：** `manim.animation.creation.TypeWithCursor`

::: currentmodule
manim.animation.creation
:::

::::: {.autoclass show-inheritance="" members="" private-members=""}
TypeWithCursor

## 描述

`TypeWithCursor` 是一个用于模拟**逐字打字效果**的动画类，常用于演示文本的实时输入过程。该动画会按照字符顺序依次显示 `Text` 或 `MarkupText` 对象中的每个字符，并在当前输入位置显示一个闪烁的光标（通常为竖线或下划线），以增强视觉真实感。

此动画适用于：
- 代码演示中的命令输入；
- 演讲或教学中的逐句展示；
- 需要强调文本逐步生成的场景。

与 `Write` 动画类似，`TypeWithCursor` 作用于文本对象，但它额外提供了光标动画和更细致的字符级控制。

---

## 参数

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `mobject` | `Text` 或 `MarkupText` | 要进行打字效果的文本对象。必须为文本类型，否则会引发错误。 |
| `run_time` | `float` | 动画的总持续时间（秒）。默认为 `2.0`。 |
| `rate_func` | `Callable[[float], float]` | 速率函数，控制字符出现的节奏。默认使用线性函数。 |
| `lag_ratio` | `float` | 字符之间的延迟比例（相对于 `run_time`）。默认 `0.05`，即每个字符的显示时间约为总时长的 5%。 |
| `cursor_char` | `str` | 光标符号，默认为 `"\|"`（竖线）。可改为 `"_"` 等。 |
| `cursor_blink_interval` | `float` | 光标闪烁间隔（秒），默认为 `0.5`。若设为 `0` 则禁用闪烁。 |
| `cursor_blink` | `bool` | 是否启用光标闪烁，默认为 `True`。 |
| `time_per_char` | `float` | 每个字符的显示时间（秒），若指定则覆盖 `run_time` 和 `lag_ratio`。 |
| `remover` | `bool` | 动画结束后是否移除 `mobject`，默认为 `False`。 |
| `suspend_mobject_updating` | `bool` | 是否暂停 `mobject` 的更新程序，默认为 `True`。 |
| `name` | `str` | 动画名称，默认为 `"TypeWithCursor"`。 |

> **注意：** 继承自 `Animation` 的其他参数（如 `use_override`）也接受。

---

## 方法

::: {.autosummary nosignatures=""}
~TypeWithCursor.begin
~TypeWithCursor.clean_up_from_scene
~TypeWithCursor.finish
~TypeWithCursor.update_submobject_list
:::

### 方法详情

- **`begin()`**  
  开始动画。  
  在该方法中，会初始化字符列表、创建光标对象，并将 `mobject` 的子对象（字符）全部隐藏，准备逐个显示。  
  *返回类型：* `None`

- **`clean_up_from_scene(scene)`**  
  动画完成后清理场景。  
  如果动画标记为 `remover`，则会移除 `mobject`；否则，光标会被移除，仅保留完整文本。  
  *参数：* `scene` – 当前场景对象。  
  *返回类型：* `None`

- **`finish()`**  
  完成动画，确保所有字符均已显示，并移除光标。  
  *返回类型：* `None`

- **`update_submobject_list()`**  
  更新子对象列表。  
  在动画开始前，调用此方法将文本拆分为单个字符（每个字符作为一个独立的 `Mobject`），用于后续逐次显示。  
  *返回类型：* `None`

---

## 属性

::: autosummary
~TypeWithCursor.run_time
:::

- **`run_time`**：动画的总时长（秒）。可通过 `set_run_time()` 修改。

---

## 示例

```python
from manim import *

class TypeWriterExample(Scene):
    def construct(self):
        text = Text("Hello, Manim!", font_size=48)
        self.play(TypeWithCursor(text, run_time=3, cursor_blink_interval=0.3))
        self.wait(1)