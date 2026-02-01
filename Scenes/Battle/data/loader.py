import pygame,os
from .skills_library import SKILLS_LIB
from .jobs_config import JOBS

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

    def update(self, dt, keys):
        dx = dy = 0
        speed = self.world_speed

        # Shift 加速
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            speed *= 2

        distance = speed * dt

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= distance
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += distance
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= distance
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += distance

        return dx, dy

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