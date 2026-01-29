import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, sheet_path, pos):
        super().__init__()
        # 1. 加载并切割素材 (假设每帧 64x64)
        self.sprite_sheet = pygame.image.load(sheet_path).convert_alpha()
        self.animations = {
            "down":  self._get_frames(0),
            "left":  self._get_frames(1),
            "right": self._get_frames(2),
            "up":    self._get_frames(3)
        }
        
        self.direction = "down"
        self.frame_index = 0
        self.image = self.animations[self.direction][self.frame_index]
        
        # 2. 核心：双矩形设计
        self.rect = self.image.get_rect(topleft=pos)
        # hitbox 是真正参与碰撞的（脚下那一小块），rect 负责画图
        self.hitbox = pygame.Rect(0, 0, 40, 24) 

    def _get_frames(self, row):
        """从大图中抠出一整行的动作帧"""
        frames = []
        for i in range(4): # 假设每种动作有 4 帧
            rect = pygame.Rect(i * 64, row * 64, 64, 64)
            frames.append(self.sprite_sheet.subsurface(rect))
        return frames

    def update(self, dt, move_vec):
        # 1. 更新朝向和动画
        if move_vec.length() > 0:
            # 确定主朝向
            if abs(move_vec.x) > abs(move_vec.y):
                self.direction = "right" if move_vec.x > 0 else "left"
            else:
                self.direction = "up" if move_vec.y < 0 else "down"
            
            # 播放动画
            self.frame_index += 0.1 # 控制动画速度
            if self.frame_index >= len(self.animations[self.direction]):
                self.frame_index = 0
        else:
            self.frame_index = 0 # 停下时显示第一帧（站立帧）

        self.image = self.animations[self.direction][int(self.frame_index)]
        
        # 2. 同步 Hitbox 到 Rect 的底部中心
        self.hitbox.midbottom = self.rect.midbottom