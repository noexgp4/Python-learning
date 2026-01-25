from Scenes.text import Button, Label, UIConfig, SelectBox, ProgressBar

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.components = []  # 存储所有可绘制对象

    def add_component(self, component):
        self.components.append(component)
        return component

    def clear(self):
        """清空当前所有UI元素"""
        self.components = []

    def draw(self):
        # 绘制所有组件
        for component in self.components:
            component.draw(self.screen)

    def check_click(self, mouse_pos):
        """检查按钮点击 (仅针对具有 check_click 方法的组件)"""
        for component in self.components:
            if hasattr(component, "check_click"):
                if component.check_click(mouse_pos):
                    return component
        return None
