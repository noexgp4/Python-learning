import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, base_color, border_color, selected_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.base_color = base_color
        self.border_color = border_color
        self.selected_color = selected_color
        self.selected = False  # 按钮是否被选中

    def draw(self, screen):
        # 绘制按钮背景
        color = self.selected_color if self.selected else self.base_color
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), border_radius=10)  # 圆角矩形

        # 绘制边框
        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), 3, border_radius=10)  # 边框

        # 绘制按钮文字
        text_surface = self.font.render(self.text, True, (255, 255, 255))  # 白色文字
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def check_click(self, mouse_pos):
        """检查鼠标是否点击了按钮"""
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            return True
        return False
