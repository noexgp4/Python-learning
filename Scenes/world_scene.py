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
        # 处理退出回菜单
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "MENU"
            # 增加空格键作为触发，因为空格键受输入法干扰最小
            if event.key == pygame.K_b or event.key == pygame.K_SPACE:
                return "BATTLE"
            if event.key == pygame.K_p:
                return "SAVE"
        return None

    def update(self):
        # 可以在这处理相机跟随逻辑
        pass

    def draw(self):
        self.screen.fill((0, 0, 0))
        # 绘制预渲染的地图
        self.screen.blit(self.map_surface, self.camera_offset)
