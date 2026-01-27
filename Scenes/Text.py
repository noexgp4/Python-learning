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
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), border_radius=8)  # 圆角矩形

        # 绘制边框
        pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), 3, border_radius=8)  # 边框

        # 绘制按钮文字
        # 优化：如果按钮被选中（背景通常为黄色），文字应变为黑色
        display_text_color = self.text_color
        if self.selected:
            display_text_color = UIConfig.COLOR_PALETTE_BLACK
            
        text_surface = self.font.render(self.text, True, display_text_color)
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
        # 1. 确定色块填充颜色 (选中时色块用黄色)
        fill_color = UIConfig.COLOR_YELLOW
        
        # 2. 确定边框色
        # 逻辑：
        # - 如果被选中，边框为白色 (提供高对比度焦点)
        # - 如果未选中，且有进度值，边框跟随色块 (黄色)
        # - 如果未选中，且无进度值，边框为默认灰色
        if self.selected:
            border_color = UIConfig.COLOR_WHITE
        elif self.progress > 0:
            border_color = UIConfig.COLOR_YELLOW
        else:
            border_color = UIConfig.COLOR_BAR_BORDER_NORMAL
            
        border_radius = 8
        
        # 绘制背景槽
        pygame.draw.rect(screen, UIConfig.COLOR_BAR_BG, (self.x, self.y, self.width, self.height), border_radius=border_radius)
        
        # 填充进度
        fill_width = int(self.width * self.progress)
        if fill_width > 0:
            pygame.draw.rect(screen, fill_color, (self.x, self.y, fill_width, self.height), border_radius=border_radius)
        
        # 绘制边框
        pygame.draw.rect(screen, border_color, (self.x, self.y, self.width, self.height), 3, border_radius=border_radius)

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
        border_radius = 8
        
        # 绘制背景
        if self.selected:
            pygame.draw.rect(screen, UIConfig.COLOR_YELLOW, (self.x, self.y, self.width, self.height), border_radius=border_radius)
        
        # 绘制边框
        pygame.draw.rect(screen, border_color, (self.x, self.y, self.width, self.height), 3, border_radius=border_radius)
        
        # 绘制文字
        # 选中时背景为黄色，文字应为黑色；未选中时为默认设置文字颜色
        text_color = UIConfig.COLOR_PALETTE_BLACK if self.selected else UIConfig.COLOR_SETTINGS_TEXT
            
        text_surf = UIConfig.render_text(self.text, "normal", text_color)
        screen.blit(text_surf, (self.x + self.width//2 - text_surf.get_width()//2, self.y + self.height//2 - text_surf.get_height()//2))
        
        # 绘制箭头 (使用传入的图标)
        arrow_color = UIConfig.COLOR_PALETTE_BLACK if self.selected else UIConfig.COLOR_GRAY
        arrow_surf = UIConfig.render_text(self.icon, "small", arrow_color)
        screen.blit(arrow_surf, (self.x + self.width + 20, self.y + self.height//2 - arrow_surf.get_height()//2))

class Panel:
    """圆角背景面板组件"""
    def __init__(self, x, y, width, height, color=(20, 20, 20, 180), border_color=None, border_width=2, border_radius=15):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius

    def draw(self, screen):
        # 使用 Surface 以支持透明度
        panel_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, self.color, (0, 0, self.width, self.height), border_radius=self.border_radius)
        if self.border_color:
            pygame.draw.rect(panel_surf, self.border_color, (0, 0, self.width, self.height), self.border_width, border_radius=self.border_radius)
        screen.blit(panel_surf, (self.x, self.y))

class ImageComponent:
    """图片显示组件"""
    def __init__(self, x, y, image, border_color=None, border_width=2, border_radius=0):
        self.x = x
        self.y = y
        self.image = image
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius

    def draw(self, screen):
        # 绘制图片
        screen.blit(self.image, (self.x, self.y))
        # 绘制边框 (如果需要)
        if self.border_color:
            rect = self.image.get_rect(topleft=(self.x, self.y))
            pygame.draw.rect(screen, self.border_color, rect, self.border_width, border_radius=self.border_radius)

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
    COLOR_BG = COLOR_PALETTE_SCREEN_BG
    
    # 交互状态
    COLOR_HIGHLIGHT = COLOR_PALETTE_YELLOW            # 文字高亮状态
    COLOR_BORDER_HIGHLIGHT = COLOR_PALETTE_YELLOW     # 边框选中高亮 (金黄色)
    
    # --- 3. 界面模块专用名 (Per-Scene Styles) ---
    # 菜单界面
    COLOR_MENU_TITLE = COLOR_PALETTE_GOLD
    COLOR_MENU_TEXT = COLOR_PALETTE_WHITE
    
    # 设置界面
    COLOR_SETTINGS_TITLE = COLOR_PALETTE_YELLOW
    COLOR_SETTINGS_TEXT = COLOR_PALETTE_GRAY
    COLOR_SETTINGS_ACTIVE = COLOR_PALETTE_WHITE
    COLOR_SETTINGS_TIPS = COLOR_PALETTE_GRAY_LIGHT
    
    # --- 4. 控件/组件专项 (Widget Styles) ---
    COLOR_BAR_BG = (25, 25, 25)                     # 进度条槽底色 (更深)
    COLOR_BAR_BORDER_NORMAL = (100, 100, 100)       # 进度条默认边框色 (中灰色)
    COLOR_BAR_BORDER_ACTIVE = COLOR_PALETTE_YELLOW  # 进度条选中边框色 (黄色)
    COLOR_BAR_BORDER = COLOR_PALETTE_GRAY           # 逻辑保留（旧名兼容）
    COLOR_SCREEN_BG = COLOR_PALETTE_SCREEN_BG       # 屏幕全局背景色
    COLOR_PANEL_BG = (30, 30, 30, 220)              # 通用面板底色
    COLOR_BTN_BASE = (50, 50, 50)                   # 按钮默认底色
    COLOR_GRAY_LIGHT = COLOR_PALETTE_GRAY_LIGHT     # 浅灰色
    
    COLOR_DARK_BG = (20, 20, 20)


    # --- 常用图标/符号 ---
    ICON_SELECT = "< >"

    # --- 字体文件路径 ---
    FONT_PATH = r"Language\Font\fusion-pixel-10px-monospaced-zh_hans.ttf"

    # --- 预设字体模板 ---
    # 我们直接在这里生成字体对象
    try:
        TITLE_FONT = pygame.font.Font(FONT_PATH, 50)
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
        # 智能反色逻辑：如果传入的是纯黄色，且我们希望在黄色背景上显示，则这里可以根据场景由调用者决定，
        # 或者在此处做一个简单的亮度判断（目前按用户要求处理）
        
        if type == "title":
            return UIConfig.TITLE_FONT.render(text, antialias, color)
        elif type == "small":
            return UIConfig.SMALL_FONT.render(text, antialias, color)
        else:
            return UIConfig.NORMAL_FONT.render(text, antialias, color)

    @staticmethod
    def draw_center_text(screen, surface, y):
        """
        在屏幕水平居中位置绘制已生成的文字表面
        """
        x = (screen.get_width() - surface.get_width()) // 2
        screen.blit(surface, (x, y))