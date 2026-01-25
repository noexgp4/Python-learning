class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []  # 存储按钮对象
        self.texts = []  # 存储文本对象

    def add_button(self, button):
        self.buttons.append(button)

    def add_text(self, text):
        self.texts.append(text)

    def draw(self):
        # 绘制所有按钮
        for button in self.buttons:
            button.draw(self.screen)

        # 绘制所有文本
        for text in self.texts:
            text.draw(self.screen)

    def check_click(self, mouse_pos):
        """检查按钮点击"""
        for button in self.buttons:
            if button.check_click(mouse_pos):
                return button
        return None
