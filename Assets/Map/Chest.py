import pygame

class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y, item_id, status="closed"):
        super().__init__()
        # 1. 加载对应的图片或序列帧
        self.images = {
            "closed": pygame.image.load("Assets/Tiles/Treasure Chest.png").convert_alpha(),
            "opened": pygame.image.load("Assets/Tiles/openchest.png").convert_alpha()
        }
        self.state = status # 从存档读取，默认为关闭
        self.image = self.images[self.state]
        
        # 2. 设置位置（直接使用 Tiled 传过来的 x, y）
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # 3. 存储逻辑属性
        self.item_id = item_id

    def open(self):
        """切换图片状态"""
        self.state = "opened"
        self.image = self.images["opened"]