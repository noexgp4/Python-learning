import os
import pygame
from Assets.Map.map import TiledMap
from Core.camera import Camera

class WorldScene:
    def __init__(self, screen):
        self.screen = screen
        screen_width, screen_height = screen.get_size()
        
        # 加载测试地图（使用模块相对路径以避免工作目录依赖）
        base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
        map_path = os.path.join(base_dir, "Assets", "Map", "testmap.tmx")
        self.tiled_map = TiledMap(map_path)
        self.map_surface = self.tiled_map.make_map()
        
        # 初始化相机系统
        self.camera = Camera(
            screen_width, 
            screen_height,
            self.tiled_map.width,
            self.tiled_map.height
        )
        
        # 玩家位置（从地图的出生点初始化）
        spawn_point = self.tiled_map.get_player_spawn_point()
        if spawn_point:
            self.player_x, self.player_y = spawn_point
        else:
            self.player_x, self.player_y = 0, 0
        
        self.player_width = 32
        self.player_height = 32

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
        # 更新相机位置，跟随玩家
        self.camera.update(self.player_x, self.player_y, self.player_width, self.player_height)

    def draw(self):
        # 使用相机应用效果，绘制地图的可见部分
        self.camera.apply(self.screen, self.map_surface)
        
        # 绘制玩家（需要应用相机偏移）
        offset_x, offset_y = self.camera.get_offset()
        pygame.draw.circle(
            self.screen,
            (255, 0, 0),
            (int(self.player_x + self.player_width // 2 + offset_x),
             int(self.player_y + self.player_height // 2 + offset_y)),
            8
        )
