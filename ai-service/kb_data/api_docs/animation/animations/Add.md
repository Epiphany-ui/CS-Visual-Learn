# Add

**合格名称：** `manim.animation.animation.Add`

::: currentmodule
manim.animation.animation
:::

::::: {.autoclass show-inheritance="" members="" private-members=""}
Add

## 描述

`Add` 是一个基础的动画类，用于在场景中**立即**添加一个或多个 Mobject（图形对象）。与 `FadeIn`、`Write` 等带有过渡效果的动画不同，`Add` 不进行任何插值或视觉渐变 – 对象会直接在动画开始时出现在场景中，其最终状态即为初始状态。

该动画常用于：
- 静态元素的瞬时出现，无需入场效果；
- 构建复杂场景时的临时展示；
- 作为其他动画的辅助或基础组件。

---

## 参数

| 参数 | 类型 | 说明 |
| :--- | :--- | :--- |
| `mobject` | `Mobject` | 要添加到场景中的图形对象。这是必填参数。 |
| `run_time` | `float` | 动画的持续时间（秒）。默认为 `0`，即对象立即出现；若设为正数，则动画会持续该时长，但对象始终可见（无变化），相当于在开始瞬间添加后保持显示。 |
| `rate_func` | `Callable[[float], float]` | 速率函数，定义动画进度曲线。由于 `Add` 无插值过程，此参数不会影响视觉结果，但会保留在父类中。 |
| `lag_ratio` | `float` | 当 `mobject` 为 `VGroup` 时，子对象出现的时间延迟比例。例如设为 `0.5`，则子对象会在动画前半部分依次出现，但由于无过渡，实际效果仅为时间点的错开。 |
| `remover` | `bool` | 若为 `True`，动画结束后会从场景中移除该对象（默认为 `False`）。 |
| `suspend_mobject_updating` | `bool` | 是否在动画期间暂停 `mobject` 的更新程序（默认为 `True`）。 |
| `name` | `str` | 动画的名称，用于调试和日志显示。默认为 `"Add"`。 |

> **注意：** 其他继承自 `Animation` 的关键字参数（如 `use_override`）亦被接受。

---

## 方法

::: {.autosummary nosignatures=""}
~Add.begin
~Add.clean_up_from_scene
~Add.finish
~Add.interpolate
~Add.update_mobjects
:::

### 方法详情

- **`begin()`**  
  开始动画。  
  此方法在动画播放时被调用，核心操作为将 `self.mobject` 添加至场景（调用 `scene.add`）。  
  *返回类型：* `None`

- **`clean_up_from_scene(scene)`**  
  动画完成后清理场景。  
  如果动画被标记为 `remover`，则在此处移除 `mobject`。  
  *参数：* `scene` – 当前场景对象。  
  *返回类型：* `None`

- **`finish()`**  
  完成动画，通常在结束时调用。  
  *返回类型：* `None`

- **`interpolate(alpha)`**  
  设置动画进度。由于 `Add` 无需插值，此方法为空实现（或只调用基类方法）。  
  *参数：* `alpha` – 0 到 1 的浮点数，表示完成比例。  
  *返回类型：* `None`

- **`update_mobjects(dt)`**  
  更新内部 mobject 状态（例如起始 mobject）。对 `Add` 而言，此方法无额外作用。  
  *参数：* `dt` – 时间增量。  
  *返回类型：* `None`

---

## 属性

::: autosummary
~Add.run_time
:::

- **`run_time`**：动画的持续时间（秒）。可通过 `set_run_time()` 修改。

---

## 示例

```python
from manim import *

class AddExample(Scene):
    def construct(self):
        dot = Dot(color=RED)
        square = Square(color=BLUE)

        # 立即添加红色圆点
        self.play(Add(dot))

        # 延迟 1 秒后添加蓝色正方形（但无过渡）
        self.play(Add(square, run_time=1))