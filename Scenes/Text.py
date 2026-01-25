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

class Label:
    def __init__(self, x, y, text, type="normal", color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.text = text
        self.type = type
        self.color = color

    def draw(self, screen):
        surface = UIConfig.render_text(self.text, self.type, self.color)
        screen.blit(surface, (self.x, self.y))

class ProgressBar:
    def __init__(self, x, y, width, height, progress, is_selected=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.progress = progress
        self.selected = is_selected

    def draw(self, screen):
        # 边框颜色
        border_color = UIConfig.COLOR_BORDER_HIGHLIGHT if self.selected else UIConfig.COLOR_BAR_BORDER
        
        # 绘制背景槽
        pygame.draw.rect(screen, UIConfig.COLOR_BAR_BG, (self.x, self.y, self.width, self.height))
        
        # 绘制边框
        pygame.draw.rect(screen, border_color, (self.x, self.y, self.width, self.height), 3)
        
        # 填充进度
        fill_width = int(self.width * self.progress)
        pygame.draw.rect(screen, UIConfig.COLOR_HIGHLIGHT_BG, (self.x, self.y, fill_width, self.height))

class SelectBox:
    def __init__(self, x, y, width, height, text, is_selected=False, icon=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.selected = is_selected
        self.icon = icon if icon else UIConfig.ICON_SELECT

    def draw(self, screen):
        # 边框颜色
        border_color = UIConfig.COLOR_BORDER_HIGHLIGHT if self.selected else UIConfig.COLOR_BAR_BORDER
        
        # 绘制背景
        pygame.draw.rect(screen, border_color, (self.x, self.y, self.width, self.height), 3)
        if self.selected:
            pygame.draw.rect(screen, UIConfig.COLOR_HIGHLIGHT_BG, (self.x, self.y, self.width, self.height))
        
        # 绘制文字
        text_color = UIConfig.COLOR_SETTINGS_ACTIVE if self.selected else UIConfig.COLOR_SETTINGS_TEXT
        text_surf = UIConfig.render_text(self.text, "normal", text_color)
        screen.blit(text_surf, (self.x + self.width//2 - text_surf.get_width()//2, self.y + self.height//2 - text_surf.get_height()//2))
        
        # 绘制箭头 (使用传入的图标)
        arrow_surf = UIConfig.render_text(self.icon, "small", UIConfig.COLOR_GRAY)
        screen.blit(arrow_surf, (self.x + self.width + 20, self.y + self.height//2 - arrow_surf.get_height()//2))

class UIConfig:
    # --- 1. 基础色板 (Base Palette) ---
    COLOR_PALETTE_WHITE = (255, 255, 255)
    COLOR_PALETTE_BLACK = (0, 0, 0)
    COLOR_PALETTE_GOLD = (255, 215, 0)
    COLOR_PALETTE_YELLOW = (255, 255, 0)
    COLOR_PALETTE_BLUE = (0, 120, 215)
    COLOR_PALETTE_GRAY = (150, 150, 150)
    COLOR_PALETTE_GRAY_LIGHT = (200, 200, 200)
    COLOR_PALETTE_GRAY_DARK = (60, 60, 60)
    COLOR_PALETTE_GRAY_MID = (100, 100, 100)
    COLOR_PALETTE_SCREEN_BG = (40, 40, 40)

    # --- 2. 核心功能映射 (Core Functional Colors) ---
    # 使用基础色板中的名字，禁止直接写 tuple
    COLOR_WHITE = COLOR_PALETTE_WHITE
    COLOR_YELLOW = COLOR_PALETTE_YELLOW
    COLOR_GRAY = COLOR_PALETTE_GRAY
    COLOR_BLUE = COLOR_PALETTE_BLUE
    COLOR_BG = COLOR_PALETTE_BLUE
    
    # 交互状态
    COLOR_HIGHLIGHT = COLOR_PALETTE_YELLOW            # 文字高亮状态
    COLOR_HIGHLIGHT_BG = COLOR_PALETTE_BLUE           # 容器填充高亮
    COLOR_BORDER_HIGHLIGHT = COLOR_PALETTE_BLUE       # 边框选中高亮
    
    # --- 3. 界面模块专用名 (Per-Scene Styles) ---
    # 菜单界面
    COLOR_MENU_TITLE = COLOR_PALETTE_GOLD
    COLOR_MENU_TEXT = COLOR_PALETTE_WHITE
    
    # 设置界面
    COLOR_SETTINGS_TITLE = COLOR_PALETTE_BLUE
    COLOR_SETTINGS_TEXT = COLOR_PALETTE_GRAY
    COLOR_SETTINGS_ACTIVE = COLOR_PALETTE_WHITE
    COLOR_SETTINGS_TIPS = COLOR_PALETTE_GRAY_LIGHT
    
    # --- 4. 控件/组件专项 (Widget Styles) ---
    COLOR_BAR_BG = COLOR_PALETTE_GRAY_DARK          # 进度条槽底色
    COLOR_BAR_BORDER = COLOR_PALETTE_GRAY           # 默认边框色
    COLOR_SCREEN_BG = COLOR_PALETTE_SCREEN_BG       # 屏幕全局背景色
    COLOR_BTN_BASE = COLOR_PALETTE_GRAY_MID         # 按钮默认底色
    
    COLOR_DARK_BG = (30, 30, 30) # 仅供极少数底层特殊用途


    # --- 常用图标/符号 ---
    ICON_SELECT = "< >"

    # --- 字体文件路径 ---
    FONT_PATH = r"Language\Font\fusion-pixel-10px-monospaced-zh_hans.ttf"

    # --- 预设字体模板 ---
    # 我们直接在这里生成字体对象
    try:
        TITLE_FONT = pygame.font.Font(FONT_PATH, 40)
        NORMAL_FONT = pygame.font.Font(FONT_PATH, 32)
        SMALL_FONT = pygame.font.Font(FONT_PATH, 20)
    except:
        # 如果文件没找到，自动降级到系统字体
        TITLE_FONT = pygame.font.SysFont("SimHei", 40)
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