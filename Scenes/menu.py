import pygame

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ["开始冒险", "加载存档", "游戏设置", "退出游戏"]
        self.selected_index = 0
        self.sfx_callback = None  # 用于播放音效的回调函数
        
        # 1. 加载并处理背景图
        try:
            # 加载图片（建议使用 1920x1080 或其他 16:9 比例的高分辨率图）
            original_bg = pygame.image.load("Assets/Image/background.png").convert()
            self.original_bg = original_bg  # 保存原始图片以供缩放
        except:
            # 如果没找到图片，创建一个深蓝色的表面作为备用
            print("警告：未找到 background.png，将使用默认背景")
            self.original_bg = None
            screen_width, screen_height = self.screen.get_size()
            self.bg_image = pygame.Surface((screen_width, screen_height))
            self.bg_image.fill((20, 20, 40))

        # 字体
        self.font = pygame.font.SysFont("SimHei", 40)
        self.title_font = pygame.font.SysFont("SimHei", 80)

    def draw(self):
        # 2. 先绘制背景（保持宽高比，不变形）
        screen_width, screen_height = self.screen.get_size()
        
        if self.original_bg:
            # 按宽高比缩放，保持不变形
            scaled_bg = self._scale_to_fit(self.original_bg, screen_width, screen_height)
            # 居中显示
            x_offset = (screen_width - scaled_bg.get_width()) // 2
            y_offset = (screen_height - scaled_bg.get_height()) // 2
            self.screen.blit(scaled_bg, (x_offset, y_offset))
        else:
            # 使用默认背景
            self.screen.fill((20, 20, 40))
        
        # 3. 可以在背景上加一层半透明的黑色蒙版，让文字更清晰
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100)) 
        self.screen.blit(overlay, (0, 0))

        # 4. 绘制标题（加一个简单的阴影效果）
        title_text = "像素勇者"
        shadow = self.title_font.render(title_text, True, (0, 0, 0))
        title = self.title_font.render(title_text, True, (255, 215, 0))
        
        # 先画阴影（偏移 4 像素），再画主体
        title_x = screen_width // 2 - title.get_width() // 2
        title_y = int(screen_height * 0.1)
        self.screen.blit(shadow, (title_x + 4, title_y + 4))
        self.screen.blit(title, (title_x, title_y))
        
        # 5. 循环绘制选项
        for i, text in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            display_text = f"> {text}" if i == self.selected_index else text
            
            option_surf = self.font.render(display_text, True, color)
            x = screen_width // 2 - option_surf.get_width() // 2
            y = int(screen_height * 0.35) + i * 60
            self.screen.blit(option_surf, (x, y))
    
    def _scale_to_fit(self, image, target_width, target_height):
        """按宽高比缩放图片，不失真"""
        img_width, img_height = image.get_size()
        img_ratio = img_width / img_height
        target_ratio = target_width / target_height
        
        if img_ratio > target_ratio:
            # 图片相对较宽，按高度缩放
            new_height = target_height
            new_width = int(new_height * img_ratio)
        else:
            # 图片相对较高，按宽度缩放
            new_width = target_width
            new_height = int(new_width / img_ratio)
        
        return pygame.transform.scale(image, (new_width, new_height))

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