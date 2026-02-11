# UI/hud.py
import pygame
import os
from Scenes.Battle.data.level_config import get_required_exp

class StatusHUD:
    def __init__(self, player):
        self.player = player
        # 基础设置
        self.pos = (20, 20)  # 在屏幕左上角的偏移
        self.width = 200     # 条的总长度
        self.height = 12     # 条的高度 (略微减小高度以容纳三条)
        
        # 颜色定义
        self.COLOR_BG = (50, 50, 50)     # 底色（深灰）
        self.COLOR_HP = (210, 50, 50)    # 血条（红）
        self.COLOR_MP = (50, 120, 255)   # 蓝条（蓝）
        self.COLOR_EXP = (240, 200, 50)  # 经验条（金/黄）
        self.COLOR_TEXT = (255, 255, 255) # 文字（白）

        # 字体加载
        font_name = "fusion-pixel-10px-monospaced-zh_hans.ttf"
        if os.path.exists(font_name):
            self.font = pygame.font.Font(font_name, 18)
            self.small_font = pygame.font.Font(font_name, 14)
        else:
            self.font = pygame.font.SysFont("SimHei", 18) # 兜底使用系统黑体
            self.small_font = pygame.font.SysFont("SimHei", 14)

    def draw(self, screen):
        # 1. 绘制职业名称和等级
        level_text = f"Lv.{self.player.level}"
        name_text = f"{self.player.job['name']}"
        name_surf = self.font.render(f"{name_text} {level_text}", True, self.COLOR_TEXT)
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
        mp_bg_rect = pygame.Rect(self.pos[0], self.pos[1] + 42, self.width, self.height)
        pygame.draw.rect(screen, self.COLOR_BG, mp_bg_rect)
        
        # 绘制 MP 进度
        mp_fill_rect = pygame.Rect(self.pos[0], self.pos[1] + 42, self.width * mp_ratio, self.height)
        pygame.draw.rect(screen, self.COLOR_MP, mp_fill_rect)

        # 4. 计算 EXP 比例
        req_exp = get_required_exp(self.player.level)
        exp_ratio = min(1.0, self.player.exp / req_exp) if req_exp > 0 else 0
        
        # 绘制 EXP 底槽
        exp_bg_rect = pygame.Rect(self.pos[0], self.pos[1] + 59, self.width, self.height // 2)
        pygame.draw.rect(screen, self.COLOR_BG, exp_bg_rect)
        
        # 绘制 EXP 进度
        exp_fill_rect = pygame.Rect(self.pos[0], self.pos[1] + 59, self.width * exp_ratio, self.height // 2)
        pygame.draw.rect(screen, self.COLOR_EXP, exp_fill_rect)

        # 绘制数值文本 (可选，更清晰)
        hp_text = self.small_font.render(f"{int(self.player.hp)}/{int(self.player.max_hp)}", True, self.COLOR_TEXT)
        screen.blit(hp_text, (self.pos[0] + self.width + 10, self.pos[1] + 23))
