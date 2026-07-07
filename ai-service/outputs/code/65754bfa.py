import numpy as np
from manim import *

class CNNVisualization(Scene):
    def construct(self):
        # -------------------------------------------------------------------
        # 参数设置
        # -------------------------------------------------------------------
        input_size = 8
        kernel_size = 3
        stride = 1
        output_size = (input_size - kernel_size) // stride + 1  # =6

        cell_size = 0.4
        spacing = 0.02

        # -------------------------------------------------------------------
        # 生成输入图像 (0~1 灰度)
        # -------------------------------------------------------------------
        input_image = np.zeros((input_size, input_size))
        center = ((input_size - 1) / 2, (input_size - 1) / 2)
        for i in range(input_size):
            for j in range(input_size):
                dist = np.sqrt((i - center[0])**2 + (j - center[1])**2)
                input_image[i, j] = 1.0 if dist < 2.5 else 0.2

        # -------------------------------------------------------------------
        # 定义卷积核（这里使用平均核）
        # -------------------------------------------------------------------
        kernel = np.ones((kernel_size, kernel_size)) / (kernel_size * kernel_size)

        # -------------------------------------------------------------------
        # 预计算卷积结果并归一化到 [0,1]
        # -------------------------------------------------------------------
        conv_result = np.zeros((output_size, output_size))
        for i in range(output_size):
            for j in range(output_size):
                region = input_image[i:i+kernel_size, j:j+kernel_size]
                conv_result[i, j] = np.sum(region * kernel)

        conv_min = conv_result.min()
        conv_max = conv_result.max()
        if conv_max - conv_min < 1e-12:
            conv_norm = np.zeros_like(conv_result)
        else:
            conv_norm = (conv_result - conv_min) / (conv_max - conv_min)

        # -------------------------------------------------------------------
        # 辅助函数：计算某个格子左上角在网格坐标系中的位置
        # -------------------------------------------------------------------
        def cell_top_left(row, col):
            x = col * (cell_size + spacing)
            y = -row * (cell_size + spacing)
            return np.array([x, y, 0])

        # -------------------------------------------------------------------
        # 创建输入图像网格
        # -------------------------------------------------------------------
        input_grid = VGroup()
        input_cells = [[None] * input_size for _ in range(input_size)]

        for i in range(input_size):
            for j in range(input_size):
                top_left = cell_top_left(i, j)
                center_pos = top_left + np.array([cell_size / 2, -cell_size / 2, 0])
                val = input_image[i, j]
                col = interpolate_color(BLACK, WHITE, val)
                cell = Square(
                    side_length=cell_size,
                    fill_opacity=1,
                    fill_color=col,
                    stroke_width=0.5,
                    stroke_color=WHITE
                )
                cell.move_to(center_pos)
                input_grid.add(cell)
                input_cells[i][j] = cell

        input_grid.move_to(np.array([-4.0, 0, 0]))

        # -------------------------------------------------------------------
        # 创建卷积核网格
        # -------------------------------------------------------------------
        kernel_grid = VGroup()
        for i in range(kernel_size):
            for j in range(kernel_size):
                top_left = cell_top_left(i, j)
                center_pos = top_left + np.array([cell_size / 2, -cell_size / 2, 0])
                cell = Square(
                    side_length=cell_size,
                    fill_opacity=0.35,
                    fill_color=YELLOW,
                    stroke_width=2.0,
                    stroke_color=YELLOW
                )
                cell.move_to(center_pos)
                kernel_grid.add(cell)

        # -------------------------------------------------------------------
        # 创建特征图网格
        # -------------------------------------------------------------------
        output_grid = VGroup()
        output_cells = [[None] * output_size for _ in range(output_size)]

        for i in range(output_size):
            for j in range(output_size):
                top_left = cell_top_left(i, j)
                center_pos = top_left + np.array([cell_size / 2, -cell_size / 2, 0])
                cell = Square(
                    side_length=cell_size,
                    fill_opacity=0,
                    fill_color=WHITE,
                    stroke_width=0.5,
                    stroke_color=WHITE
                )
                cell.move_to(center_pos)
                output_grid.add(cell)
                output_cells[i][j] = cell

        output_grid.move_to(np.array([4.0, 0, 0]))

        # -------------------------------------------------------------------
        # 文字标签
        # -------------------------------------------------------------------
        input_label = Text("Input Image", font_size=24).next_to(input_grid, UP)
        output_label = Text("Feature Map", font_size=24).next_to(output_grid, UP)
        kernel_label = Text("Kernel", font_size=24)

        # 将文字也添加到场景，并为 kernel_label 添加跟随更新器
        kernel_label.next_to(kernel_grid, UP)
        kernel_label.add_updater(lambda m, dt: m.next_to(kernel_grid, UP))

        # -------------------------------------------------------------------
        # 尺寸说明
        # -------------------------------------------------------------------
        size_label_input = Text("8×8 pixels", font_size=18).next_to(input_grid, DOWN)
        size_label_output = Text("6×6 pixels", font_size=18).next_to(output_grid, DOWN)

        # -------------------------------------------------------------------
        # 将静态元素添加到场景
        # -------------------------------------------------------------------
        self.add(input_grid, input_label, size_label_input,
                 output_grid, output_label, size_label_output,
                 kernel_grid, kernel_label)

        # -------------------------------------------------------------------
        # 进度追踪器（0 → 36，对应 6×6 个步）
        # -------------------------------------------------------------------
        progress_tracker = ValueTracker(0)

        # 记录已经填充到哪个步数
        last_filled = [-1]

        # -------------------------------------------------------------------
        # 更新函数：移动卷积核 + 填充特征图
        # -------------------------------------------------------------------
        def update_display(mob, dt):
            progress = progress_tracker.get_value()

            # 当前步数（截断到 0 … 35）
            current_step = int(progress)
            if current_step >= output_size * output_size:
                current_step = output_size * output_size - 1
            if current_step < 0:
                current_step = 0

            # 确定卷积核的左上角应该对齐到输入图像的哪个格子
            row = current_step // output_size
            col = current_step % output_size

            target_cell = input_cells[row][col]
            target_ul = target_cell.get_center() + np.array([-cell_size / 2, cell_size / 2, 0])
            kernel_grid.move_to(target_ul, aligned_edge=UL)

            # 填充特征图中新的格子（从上次结束后的下一个到当前步）
            start = last_filled[0] + 1
            end = current_step
            for s in range(start, end + 1):
                if s < 0:
                    continue
                r = s // output_size
                c = s % output_size
                cell = output_cells[r][c]
                val = conv_norm[r, c]
                cell.set_fill(color=interpolate_color(BLACK, WHITE, val), opacity=1)

            last_filled[0] = current_step

        # 创建哑元 VMobject 承载更新器
        dummy = VMobject()
        dummy.add_updater(update_display)
        self.add(dummy)

        # -------------------------------------------------------------------
        # 播放动画
        # -------------------------------------------------------------------
        self.play(
            progress_tracker.animate.set_value(output_size * output_size),
            run_time=18,
            rate_func=linear
        )
        self.wait(2)