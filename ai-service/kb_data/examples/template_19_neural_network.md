# 意图：绘制一个标准的全连接神经网络（FCNN），包含输入层、隐藏层和输出层，并用连线（神经元突触）将它们层层相连。展示 VGroup 的高级嵌套与遍历。
# 关键词：神经网络, 机器学习, 深度学习, 节点, 连线, VGroup, Line, FCNN

下面是完整的 Manim 代码示例：
```python
from manim import *

class NeuralNetwork(Scene):
    def construct(self):
        # 1. 定义每一层的神经元数量
        layer_sizes = [3, 5, 4, 2]  # 输入层3，隐层5和4，输出层2
        
        layers = VGroup()
        for size in layer_sizes:
            # 创建单层的所有神经元节点
            layer = VGroup(*[Circle(radius=0.15, color=BLUE, fill_opacity=0.8) for _ in range(size)])
            layer.arrange(DOWN, buff=0.5)
            layers.add(layer)
        
        # 将所有层横向排版
        layers.arrange(RIGHT, buff=2)
        
        # 2. 绘制层与层之间的全连接连线
        edges = VGroup()
        for i in range(len(layers) - 1):
            current_layer = layers[i]
            next_layer = layers[i + 1]
            for node1 in current_layer:
                for node2 in next_layer:
                    # 使用较暗的颜色和极细的线条表示权重连接
                    edge = Line(node1.get_center(), node2.get_center(), stroke_width=1, color=GRAY)
                    edges.add(edge)
        
        # 3. 添加标签（使用 Text 规避 LaTeX 环境依赖）
        label_in = Text("输入层", font_size=24).next_to(layers[0], UP, buff=0.5)
        label_out = Text("输出层", font_size=24).next_to(layers[-1], UP, buff=0.5)
        
        # 4. 炫酷的入场动画：先画线，再画节点
        self.play(LaggedStartMap(Create, edges, lag_ratio=0.01), run_time=3)
        self.play(LaggedStartMap(FadeIn, layers, lag_ratio=0.2), run_time=2)
        self.play(Write(label_in), Write(label_out))
        self.wait(2)