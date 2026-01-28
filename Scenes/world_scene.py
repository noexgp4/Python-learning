import pygame
from Assets.Map.map import TiledMap

class WorldScene:
    def __init__(self, screen):
        self.screen = screen
        # 加载测试地图
        self.tiled_map = TiledMap("Assets/Map/testmap.tmx")
        self.map_surface = self.tiled_map.make_map()
        self.camera_offset = pygame.Vector2(0, 0)

    def handle_input(self, event):
        # 暂时只处理简单的退出回菜单，或者预留给玩家移动
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "MENU"
        return None

    def update(self):
        # 可以在这处理相机跟随逻辑
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        # 绘制预渲染的地图
        self.screen.blit(self.map_surface, self.camera_offset)
