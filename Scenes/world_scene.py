import os
import pygame
from Assets.Map.map import TiledMap
from Assets.Map.camera import Camera
from Scenes.Battle.data.loader import Player
from Scenes.Battle.data.jobs_config import JOBS

class WorldScene:
    def __init__(self, screen, job_name):
        self.screen = screen
        screen_width, screen_height = screen.get_size()

        # 地图
        base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
        map_path = os.path.join(base_dir, "Assets", "Map", "testmap.tmx")

        self.tiled_map = TiledMap(map_path)
        self.map_surface = self.tiled_map.make_map()

        # 玩家出生点
        spawn_point = self.tiled_map.get_player_spawn_point() or (0,0)
        self.player = Player(spawn_point[0], spawn_point[1], job_name)

        # 相机
        self.camera = Camera(
            screen_width,
            screen_height,
            self.tiled_map.width,
            self.tiled_map.height,
            zoom=2.0
        )

        # 玩家（速度来自职业表）
    def update(self, dt):
        keys = pygame.key.get_pressed()
        dx, dy = self.player.update(dt, keys)

        # 边界限制
        self.player.x = max(0, min(self.tiled_map.width - self.player.width, self.player.x + dx))
        self.player.y = max(0, min(self.tiled_map.height - self.player.height, self.player.y + dy))

        self.camera.update(self.player.x, self.player.y, self.player.width, self.player.height)

    def draw(self):
        self.camera.apply(self.screen, self.map_surface)
        offset_x, offset_y = self.camera.get_offset()
        pygame.draw.circle(
            self.screen, (255,0,0),
            (int(self.player.x + self.player.width/2 + offset_x),
             int(self.player.y + self.player.height/2 + offset_y)),
            8
        )
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "MENU"
            if event.key == pygame.K_SPACE or event.key == pygame.K_b:
                return "BATTLE"
            if event.key == pygame.K_p:
                return "SAVE"
        return None
