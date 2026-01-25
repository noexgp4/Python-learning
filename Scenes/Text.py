import pygame

# 初始化一下，确保字体系统能用
pygame.font.init()

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