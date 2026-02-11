import pygame,os
from .skills_library import SKILLS_LIB
from .jobs_config import JOBS
from Assets.Map.map import TiledMap


class Player:
    # 初始化玩家

    def __init__(self, x, y, job_name, hp=None, mp=None, level=1, exp=0):
        self.x = float(x)
        self.y = float(y)

        self.job = JOBS[job_name]
        self.job_data = JOBS[job_name]
        self.world_speed = self.job_data["world_speed"]

        self.width = self.job_data["frame_size"][0]
        self.height = self.job_data["frame_size"][1]

        self.animations = self._cut_spritesheet()

        # 动画状态
        self.direction = "down"
        self.frame_index = 0
        self.anim_timer = 0
        self.anim_speed = 0.15 # 秒/帧
        self.is_moving = False  
        self.is_running = False # 新增：加速状态

        # 属性状态
        self.max_hp = self.job_data.get("hp", 100)
        self.max_mp = self.job_data.get("mp", 50)
        self.hp = hp if hp is not None else self.max_hp
        self.mp = mp if mp is not None else self.max_mp
        self.level = level
        self.exp = exp

    def _cut_spritesheet(self):
        """
        从角色雪碧图中切割出所有动画帧。
        返回字典：{'down': [img1, img2, ...], 'left': [...], ...}
        """
        data = self.job_data
        path = data["sprite_path"]
        
        # 确保路径正确（相对于当前文件）
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_dir, "..", "..", "..", path)
        
        if not os.path.exists(full_path):
            print(f"[Error] Sprite not found: {full_path}")
            return {}

        try:
            sheet = pygame.image.load(full_path).convert_alpha()
        except pygame.error as e:
            print(f"[Error] Failed to load sprite: {e}")
            return {}

        fw, fh = data["frame_size"]
        cols = data["cols"]
        rows = data["rows"]
        
        animations = {
            "down": [], "left": [], "right": [], "up": [],
            "run_down": [], "run_left": [], "run_right": [], "run_up": []
        }

        # 方向映射表
        row_to_key = {
            0: "down", 1: "left", 2: "right", 3: "up",
            4: "run_down", 5: "run_left", 6: "run_right", 7: "run_up"
        }

        for r in range(rows):
            for c in range(cols):
                rect = pygame.Rect(c * fw, r * fh, fw, fh)
                frame = sheet.subsurface(rect)
                
                # 缩放至渲染尺寸
                frame = pygame.transform.scale(frame, (self.width, self.height))
                
                anim_key = row_to_key.get(r, "down")
                animations[anim_key].append(frame)
                
        return animations

    def update(self, dt, keys, walls, map_w, map_h):
        dx = dy = 0
        speed = self.world_speed

        # Shift 加速
        self.is_running = (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])
        if self.is_running:
            speed *= 2
            self.anim_speed = 0.1 # 加速时动作也变快
        else:
            self.anim_speed = 0.15

        distance = speed * dt

# 1. 获取输入方向
        move_x = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        move_y = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])

        # 归一化移动向量（防止斜着走变快）
        self.is_moving = move_x != 0 or move_y != 0
        if self.is_moving:
            vec = pygame.Vector2(move_x, move_y).normalize()
            dx = vec.x * distance
            dy = vec.y * distance
            
            # 更新方向
            if abs(move_x) > abs(move_y):
                self.direction = "right" if move_x > 0 else "left"
            else:
                self.direction = "down" if move_y > 0 else "up"
        
        # 更新动画帧
        if self.is_moving:
            self.anim_timer += dt
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.animations.get(self.direction, [0]))
        else:
            self.frame_index = 0 # 停止移动时回到第一帧

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

    def get_rect(self):
        """返回玩家的逻辑碰撞矩形 (用于地图传送等检测)"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_current_image(self):
        """返回当前应该渲染的图像帧"""
        anim_key = self.direction
        if self.is_running and self.is_moving:
            anim_key = f"run_{self.direction}"
            
        anim = self.animations.get(anim_key, [])
        if not anim:
            # 如果没有加速动画，回退到普通动画
            anim = self.animations.get(self.direction, [])
            
        if not anim:
            return None
        return anim[self.frame_index % len(anim)]


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