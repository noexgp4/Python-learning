import os
import pygame
from Assets.Map.map import TiledMap
from Assets.Map.camera import Camera

class WorldScene:
    def __init__(self, screen):
        self.screen = screen
        screen_width, screen_height = screen.get_size()
        
        # 加载测试地图（使用模块相对路径以避免工作目录依赖）
        base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
        map_path = os.path.join(base_dir, "Assets", "Map", "testmap.tmx")
        self.tiled_map = TiledMap(map_path)
        self.map_surface = self.tiled_map.make_map()
        
        # 初始化相机系统（zoom=2.0 表示放大2倍）
        self.camera = Camera(
            screen_width, 
            screen_height,
            self.tiled_map.width,
            self.tiled_map.height,
            zoom=2.0  # 初始缩放为2倍放大
        )
        
        # 玩家位置（从地图的出生点初始化）
        spawn_point = self.tiled_map.get_player_spawn_point()
        if spawn_point:
            self.player_x, self.player_y = spawn_point
        else:
            self.player_x, self.player_y = 0, 0
        
        self.player_width = 32
        self.player_height = 32
        self.player_speed = 4  # 玩家移动速度

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
            # 缩放控制（Z/X键）
            if event.key == pygame.K_z:
                # Z键放大
                self.camera.set_zoom(self.camera.zoom + 0.5)
            if event.key == pygame.K_x:
                # X键缩小
                self.camera.set_zoom(max(0.5, self.camera.zoom - 0.5))
        
        # 方向键控制玩家移动
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player_y = max(0, self.player_y - self.player_speed)
        if keys[pygame.K_DOWN]:
            self.player_y = min(self.tiled_map.height - self.player_height, self.player_y + self.player_speed)
        if keys[pygame.K_LEFT]:
            self.player_x = max(0, self.player_x - self.player_speed)
        if keys[pygame.K_RIGHT]:
            self.player_x = min(self.tiled_map.width - self.player_width, self.player_x + self.player_speed)
        
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
