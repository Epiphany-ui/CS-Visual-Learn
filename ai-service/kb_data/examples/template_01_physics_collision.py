# 意图：模拟两个方块在完全弹性碰撞下的物理运动，利用 ValueTracker 和 add_updater 实现基于时间的物理引擎级别的实时坐标更新。
# 关键词：物理, 碰撞, 动量守恒, 速度, ValueTracker, add_updater, Square, 实时计算

from manim import *

class ElasticCollision(Scene):
    def construct(self):
        # 1. 创建两个方块（左侧质量大/速度快，右侧质量小/静止或慢速）
        box_left = Square(side_length=1.5, color=BLUE, fill_opacity=0.8).move_to(LEFT * 4)
        box_right = Square(side_length=1.0, color=RED, fill_opacity=0.8).move_to(RIGHT * 1)

        # 添加质量标签
        label_left = MathTex("m_1").move_to(box_left.get_center())
        label_right = MathTex("m_2").move_to(box_right.get_center())

        # 将标签与方块绑定，使其跟随移动
        box_left.add(label_left)
        box_right.add(label_right)

        # 2. 初始化物理参数：质量和初始速度
        m1, m2 = 3.0, 1.0
        v1, v2 = 2.0, -0.5  # v1向右，v2向左

        # 使用列表存储速度，以便在 updater 中修改它（利用闭包的引用特性）
        velocities = [v1, v2]

        # 3. 创建时间追踪器 dt
        time_tracker = ValueTracker(0)

        # 4. 定义物理更新逻辑
        def update_physics(mob, dt):
            # 获取两个方块的中心 x 坐标
            x1 = box_left.get_x()
            x2 = box_right.get_x()

            # 检测碰撞 (考虑方块边长的一半)
            distance = x2 - x1
            min_distance = (1.5 / 2) + (1.0 / 2)

            if distance <= min_distance:
                # 发生碰撞，计算完全弹性碰撞后的新速度
                u1, u2 = velocities[0], velocities[1]
                v1_new = ((m1 - m2) * u1 + 2 * m2 * u2) / (m1 + m2)
                v2_new = ((m2 - m1) * u2 + 2 * m1 * u1) / (m1 + m2)

                velocities[0] = v1_new
                velocities[1] = v2_new

                # 强制推开微小距离以防止粘连Bug
                box_left.set_x(x2 - min_distance - 0.01)

            # 根据当前速度更新位移
            box_left.shift(RIGHT * velocities[0] * dt)
            box_right.shift(RIGHT * velocities[1] * dt)

        # 5. 绑定更新器并执行动画
        self.add(box_left, box_right)

        # 将 updater 绑定到场景或某个虚拟物体上，这里我们直接绑定到 box_left 顺带更新两者
        box_left.add_updater(update_physics)

        # 播放时间线，持续运行 4 秒的物理模拟
        self.wait(4)

        # 移除 updater 结束模拟
        box_left.remove_updater(update_physics)