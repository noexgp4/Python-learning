import pygame

# 初始化一下，确保字体系统能用
pygame.font.init()

class Button:
    def __init__(self, x, y, width, height, text, font, base_color, border_color, selected_color, text_color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.base_color = base_color
        self.border_color = border_color
        self.selected_color = selected_color
        self.text_color = text_color
        self.selected = False  # 按钮是否被选中

    def draw(self, screen):
        # 绘制按钮背景
        color = self.selected_color if self.selected else self.base_color
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), border_radius=10)  # 圆角矩形

        # 绘制边框
        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), 3, border_radius=10)  # 边框

        # 绘制按钮文字
        text_surface = self.font.render(self.text, True, self.text_color)  # 白色文字
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def check_click(self, mouse_pos):
        """检查鼠标是否点击了按钮"""
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            return True
        return False
    
class UIConfig:
    # --- 颜色定义 (RGB) ---
    COLOR_WHITE = (255, 255, 255)
    COLOR_YELLOW = (255, 255, 0)
    COLOR_GRAY = (150, 150, 150)
    COLOR_BG = (30, 30, 30)

    # --- 字体文件路径 ---
    FONT_PATH = r"Language\Font\fusion-pixel-10px-monospaced-zh_hans.ttf"

    # --- 预设字体模板 ---
    # 我们直接在这里生成字体对象
    try:
        TITLE_FONT = pygame.font.Font(FONT_PATH, 60)
        NORMAL_FONT = pygame.font.Font(FONT_PATH, 32)
        SMALL_FONT = pygame.font.Font(FONT_PATH, 20)
    except:
        # 如果文件没找到，自动降级到系统字体
        TITLE_FONT = pygame.font.SysFont("SimHei", 60)
        NORMAL_FONT = pygame.font.SysFont("SimHei", 32)
        SMALL_FONT = pygame.font.SysFont("SimHei", 20)

    # --- 辅助方法：快速生成文字表面 ---
    @staticmethod
    def render_text(text, type="normal", color=COLOR_WHITE, antialias=False):
        """
        一个万能的文字生成器
        type: "title", "normal", "small"
        """
        if type == "title":
            return UIConfig.TITLE_FONT.render(text, antialias, color)
        elif type == "small":
            return UIConfig.SMALL_FONT.render(text, antialias, color)
        else:
            return UIConfig.NORMAL_FONT.render(text, antialias, color)