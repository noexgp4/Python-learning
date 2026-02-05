import os
import pygame
from Assets.Map.map import TiledMap
from Assets.Map.camera import Camera
from Scenes.Battle.data.loader import Player
from Scenes.Battle.data.jobs_config import JOBS
from Scenes.UI.hud import StatusHUD

class WorldScene:
    def __init__(self, screen, job_name, debug_collision=False):
        self.screen = screen
        screen_width, screen_height = screen.get_size()

        # 1. 计算路径并加载地图
        base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
        map_path = os.path.join(base_dir, "Assets", "Map", "testmap.tmx")
        self.tiled_map = TiledMap(map_path)
        print(f"【调试】加载了 {len(self.tiled_map.walls)} 个碰撞墙")

        # 2. 创建玩家
        spawn_point = self.tiled_map.get_player_spawn_point() or (0,0)
        self.player = Player(spawn_point[0], spawn_point[1], job_name)
        print(f"【调试】玩家出生点原始坐标: {spawn_point}")
        self.map_surface = self.tiled_map.make_map()
        
        # 3. 初始化 HUD (必须在玩家创建之后)
        self.hud = StatusHUD(self.player)
        
        # 4. 最后初始化相机
        self.camera = Camera(
            screen_width,
            screen_height,
            self.tiled_map.width,
            self.tiled_map.height,
            zoom=2.0
        )

        self.debug_collision = debug_collision

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(
            dt, 
            keys, 
            self.tiled_map.walls,
            self.tiled_map.width, 
            self.tiled_map.height
        )

        self.camera.update(self.player.x, self.player.y, self.player.width, self.player.height)

    def draw(self):
        # 1. 应用相机变换渲染地图
        self.camera.apply(self.screen, self.map_surface)
        
        # 2. 获取当前的相机偏移和缩放倍率
        offset_x, offset_y = self.camera.get_offset()
        zoom = getattr(self.camera, 'zoom', 2.0) 

        # 3. 绘制碰撞调试红框
        if self.debug_collision:
            for wall in self.tiled_map.walls:
                debug_rect = pygame.Rect(
                    (wall.x + offset_x) * zoom,
                    (wall.y + offset_y) * zoom,
                    wall.width * zoom,
                    wall.height * zoom
                )
                pygame.draw.rect(self.screen, (255, 0, 0), debug_rect, 1)

        # 4. 绘制玩家
        player_screen_x = (self.player.x + offset_x) * zoom
        player_screen_y = (self.player.y + offset_y) * zoom
        player_screen_w = self.player.width * zoom
        player_screen_h = self.player.height * zoom
        
        player_img = self.player.get_current_image()
        if player_img:
            draw_img = pygame.transform.scale(player_img, (int(player_screen_w), int(player_screen_h)))
            self.screen.blit(draw_img, (player_screen_x, player_screen_y))
        
        # 5. 绘制 HUD
        self.hud.draw(self.screen)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "MENU"
            if event.key == pygame.K_SPACE or event.key == pygame.K_b:
                return "BATTLE"
            if event.key == pygame.K_p:
                return "SAVE"
        return None
