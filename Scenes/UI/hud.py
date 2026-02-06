# UI/hud.py
import pygame
import os

class StatusHUD:
    def __init__(self, player):
        self.player = player
        # 基础设置
        self.pos = (20, 20)  # 在屏幕左上角的偏移
        self.width = 200     # 条的总长度
        self.height = 15     # 条的高度
        
        # 颜色定义
        self.COLOR_BG = (7, 59, 50)
        self.COLOR_BG = (50, 50, 50)     # 底色（深灰）
        self.COLOR_HP = (200, 50, 50)    # 血条（红）
        self.COLOR_MP = (50, 100, 200)   # 蓝条（蓝）
        self.COLOR_TEXT = (255, 255, 255) # 文字（白）

        # 字体加载
        font_name = "fusion-pixel-10px-monospaced-zh_hans.ttf"
        if os.path.exists(font_name):
            self.font = pygame.font.Font(font_name, 18)
        else:
            self.font = pygame.font.SysFont("SimHei", 18) # 兜底使用系统黑体
    def draw(self, screen):
        # 1. 绘制职业名称
        name_surf = self.font.render(f"{self.player.job['name']}", True, self.COLOR_TEXT)
        screen.blit(name_surf, (self.pos[0], self.pos[1]))

        # 2. 计算 HP 比例
        hp_ratio = self.player.hp / self.player.max_hp if self.player.max_hp > 0 else 0
        
        # 绘制 HP 底槽
        hp_bg_rect = pygame.Rect(self.pos[0], self.pos[1] + 25, self.width, self.height)
        pygame.draw.rect(screen, self.COLOR_BG, hp_bg_rect)
        
        # 绘制 HP 进度
        hp_fill_rect = pygame.Rect(self.pos[0], self.pos[1] + 25, self.width * hp_ratio, self.height)
        pygame.draw.rect(screen, self.COLOR_HP, hp_fill_rect)

        # 3. 计算 MP 比例
        mp_ratio = self.player.mp / self.player.max_mp if self.player.max_mp > 0 else 0
        
        # 绘制 MP 底槽
        mp_bg_rect = pygame.Rect(self.pos[0], self.pos[1] + 45, self.width, self.height)
        pygame.draw.rect(screen, self.COLOR_BG, mp_bg_rect)
        
        # 绘制 MP 进度
        mp_fill_rect = pygame.Rect(self.pos[0], self.pos[1] + 45, self.width * mp_ratio, self.height)
        pygame.draw.rect(screen, self.COLOR_MP, mp_fill_rect)