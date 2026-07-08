# Blink

**合格名称：** `manim.animation.indication.Blink`

::: currentmodule
manim.animation.indication
:::

::::: {.autoclass show-inheritance="" members="" private-members=""}
Blink

## 描述

`Blink` 是一个用于**强调**的动画类，使目标 `Mobject` 产生一次或多次“闪烁”效果 – 通常表现为快速缩放（放大再恢复）并伴随透明度或颜色的短暂变化，以吸引观众注意力。

该动画常用于：
- 高亮显示场景中的关键元素；
- 模拟按钮点击或状态变化；
- 在演示中引导观众视线。

`Blink` 是 `Indication` 动画家族的一员，与 `Flash`、`Wiggle` 等类似，但更专注于快速、明显的视觉跳动。

---

## 参数

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `mobject` | `Mobject` | 要执行闪烁动画的对象。 |
| `run_time` | `float` | 动画的总持续时间（秒）。默认为 `0.5`。 |
| `rate_func` | `Callable[[float], float]` | 速率函数，控制闪烁的节奏。默认使用 `rate_functions.ease_in_out_sine`。 |
| `blink_ratio` | `float` | 闪烁过程中“放大”阶段占 `run_time` 的比例（剩余时间为恢复阶段）。默认为 `0.5`。 |
| `n_blinks` | `int` | 闪烁次数。默认为 `1`。若大于 `1`，动画会重复进行多次放大-恢复循环。 |
| `scale_factor` | `float` | 放大倍率。对象在峰值时会放大到原始大小的 `scale_factor` 倍。默认为 `1.2`。 |
| `color_shift` | `str` 或 `Color` | 闪烁时颜色的变化目标色。若为 `None` 则不改变颜色。默认为 `None`。 |
| `remover` | `bool` | 动画结束后是否移除 `mobject`，默认为 `False`。 |
| `suspend_mobject_updating` | `bool` | 是否暂停 `mobject` 的更新程序，默认为 `True`。 |
| `name` | `str` | 动画名称，默认为 `"Blink"`。 |

> **注意：** 其他继承自 `Animation` 的参数（如 `lag_ratio`）也接受，但可能不影响 `Blink` 的行为。

---

## 方法

::: {.autosummary nosignatures=""}
~Blink.begin
~Blink.interpolate
~Blink.finish
:::

### 方法详情

- **`begin()`**  
  开始动画。  
  初始化内部状态，记录对象的原始属性（缩放和颜色）。  
  *返回类型：* `None`

- **`interpolate(alpha)`**  
  根据进度 `alpha` 更新对象的状态。  
  将总体进度拆分为多个闪烁周期，并应用缩放和颜色变化。  
  *参数：* `alpha` – 0 到 1 的浮点数。  
  *返回类型：* `None`

- **`finish()`**  
  完成动画，确保对象恢复到原始大小和颜色（如果 `color_shift` 已应用，则恢复）。  
  *返回类型：* `None`

---

## 属性

::: autosummary
~Blink.run_time
:::

- **`run_time`**：动画的总时长（秒）。可通过 `set_run_time()` 修改。

---

## 示例

```python
from manim import *

class BlinkExample(Scene):
    def construct(self):
        circle = Circle(color=BLUE, fill_opacity=0.5)
        self.play(Create(circle))
        self.play(Blink(circle, n_blinks=3, scale_factor=1.5, run_time=2))
        self.wait(1)
