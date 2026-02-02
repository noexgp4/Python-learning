import pygame,os
from .skills_library import SKILLS_LIB
from .jobs_config import JOBS
from Assets.Map.map import TiledMap

class Player:
    # 初始化玩家

    def __init__(self, x, y, job_name):
        self.x = float(x)
        self.y = float(y)

        self.job = JOBS[job_name]
        self.job_data = JOBS[job_name]
        self.world_speed = self.job_data["world_speed"]

        self.width = 32
        self.height = 32

    def update(self, dt, keys, walls, map_w, map_h):
        dx = dy = 0
        speed = self.world_speed

        # Shift 加速
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            speed *= 2

        distance = speed * dt

# 1. 获取输入方向
        move_x = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        move_y = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])

        # 归一化移动向量（防止斜着走变快）
        if move_x != 0 or move_y != 0:
            vec = pygame.Vector2(move_x, move_y).normalize()
            dx = vec.x * distance
            dy = vec.y * distance

        # 2. X 轴移动与碰撞
        self.x += dx
        self.x = max(0, min(map_w - self.width, self.x)) # 边界限制
        
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for wall in walls:
            if player_rect.colliderect(wall):
                if dx > 0: self.x = wall.left - self.width
                if dx < 0: self.x = wall.right
                break

        # 3. Y 轴移动与碰撞
        self.y += dy
        self.y = max(0, min(map_h - self.height, self.y)) # 边界限制
        
        # 重新同步位置用于 Y 轴判定
        player_rect.topleft = (self.x, self.y)
        for wall in walls:
            if player_rect.colliderect(wall):
                if dy > 0: self.y = wall.top - self.height
                if dy < 0: self.y = wall.bottom
                break

class Actor:
    def __init__(self, key, config_dict):
        data = config_dict[key]
        self.name = data["name"]
        
        # 装载数值
        s = data["stats"]
        self.hp = self.max_hp = s["hp"]
        self.mp = self.max_mp = s["mp"]
        self.atk = s["atk"]
        self.armor = s["def"]
        
        # 【核心】装载技能数据
        self.skills = []
        for s_id in data["skills"]:
            if s_id in SKILLS_LIB:
                # 复制一份，防止动态修改影响全局库
                skill_info = SKILLS_LIB[s_id].copy()
                self.skills.append(skill_info)