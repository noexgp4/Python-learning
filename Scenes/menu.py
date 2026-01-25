import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ["开始冒险", "加载存档", "游戏设置", "退出游戏"]
        self.selected_index = 0
        self.sfx_callback = None  # 用于播放音效的回调函数
        
        # 1. 加载并处理背景图
        try:
            # 加载图片
            # 修复后
            original_bg = pygame.image.load("Assets/Image/background.png").convert()
            # 缩放到屏幕尺寸 (800x600)
            self.bg_image = pygame.transform.scale(original_bg, (800, 600))
        except:
            # 如果没找到图片，创建一个深蓝色的表面作为备用
            print("警告：未找到 background.png,将使用默认背景")
            self.bg_image = pygame.Surface((800, 600))
            self.bg_image.fill((20, 20, 40))

        # 字体
        self.font = pygame.font.SysFont("SimHei", 40)
        self.title_font = pygame.font.SysFont("SimHei", 80)

    def draw(self):
        # 2. 先绘制背景
        self.screen.blit(self.bg_image, (0, 0))
        
        # 3. 可以在背景上加一层半透明的黑色蒙版，让文字更清晰
        # 创建一个覆盖全屏的黑色表面，透明度设为 128 (0-255)
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100)) 
        self.screen.blit(overlay, (0, 0))

        # 4. 绘制标题（加一个简单的阴影效果）
        title_text = "像素勇者"
        shadow = self.title_font.render(title_text, True, (0, 0, 0))
        title = self.title_font.render(title_text, True, (255, 215, 0))
        
        # 先画阴影（偏移 4 像素），再画主体
        self.screen.blit(shadow, (400 - title.get_width()//2 + 4, 104))
        self.screen.blit(title, (400 - title.get_width()//2, 100))
        
        # 5. 循环绘制选项
        for i, text in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            display_text = f"> {text}" if i == self.selected_index else text
            
            option_surf = self.font.render(display_text, True, color)
            x = 400 - option_surf.get_width()//2
            y = 300 + i * 60
            self.screen.blit(option_surf, (x, y))

    def set_sfx_callback(self, callback):
        """设置音效回调函数"""
        self.sfx_callback = callback

    def play_button_sound(self):
        """播放按钮音效"""
        if self.sfx_callback:
            self.sfx_callback("button")

    def update_selection(self, direction):
        self.selected_index = (self.selected_index + direction) % len(self.options)
        self.play_button_sound()  # 自动播放按钮音效