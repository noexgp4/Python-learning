import os
import pygame
from Assets.Map.map import TiledMap
from Assets.Map.camera import Camera
from Scenes.Battle.data.loader import Player
from Scenes.Battle.data.jobs_config import JOBS

class WorldScene:
    def __init__(self, screen, job_name, debug_collision=False):
        self.screen = screen
        screen_width, screen_height = screen.get_size()

        # 1. 先计算路径
        base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
        map_path = os.path.join(base_dir, "Assets", "Map", "testmap.tmx")

        # 2. 再加载地图（此时 map_path 已经有值了）
        self.tiled_map = TiledMap(map_path)
        # --- 添加这行打印 ---
        print(f"【调试】加载了 {len(self.tiled_map.walls)} 个碰撞墙")

        # 3. 再创建玩家
        spawn_point = self.tiled_map.get_player_spawn_point() or (0,0)
        self.player = Player(spawn_point[0], spawn_point[1], job_name)
        print(f"【调试】玩家出生点原始坐标: {spawn_point}")
        self.map_surface = self.tiled_map.make_map()
        
        # 4. 最后初始化相机
        self.camera = Camera(
            screen_width,
            screen_height,
            self.tiled_map.width,
            self.tiled_map.height,
            zoom=2.0
        )

        # 玩家（速度来自职业表）
        self.debug_collision = debug_collision  # 控制是否显示碰撞调试线

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.player.update(
            dt, 
            keys, 
            self.tiled_map.walls,  # <--- 关键点：数据在这里传递
            self.tiled_map.width, 
            self.tiled_map.height
        )

        self.camera.update(self.player.x, self.player.y, self.player.width, self.player.height)

    def draw(self):
        # 1. 应用相机变换渲染地图
        self.camera.apply(self.screen, self.map_surface)
        
        # 2. 获取当前的相机偏移和缩放倍率
        offset_x, offset_y = self.camera.get_offset()
        # 注意：这里要确保能拿到 Camera 类里的 zoom 属性
        zoom = getattr(self.camera, 'zoom', 2.0) 

        # 3. 根据开关状态绘制碰撞调试红框
        if self.debug_collision:
            for wall in self.tiled_map.walls:
                # 正确公式：(原始坐标 + 偏移) * 缩放
                debug_rect = pygame.Rect(
                    (wall.x + offset_x) * zoom,
                    (wall.y + offset_y) * zoom,
                    wall.width * zoom,
                    wall.height * zoom
                )
                pygame.draw.rect(self.screen, (255, 0, 0), debug_rect, 1)

        # 4. 绘制玩家 (同样应用缩放和偏移)
        player_screen_x = (self.player.x + offset_x) * zoom
        player_screen_y = (self.player.y + offset_y) * zoom
        player_screen_w = self.player.width * zoom
        player_screen_h = self.player.height * zoom
        
        # 绘制玩家逻辑矩形（绿色，用于对比）
        pygame.draw.rect(self.screen, (0, 255, 0), (player_screen_x, player_screen_y, player_screen_w, player_screen_h), 1)
        
        # 绘制玩家中心点
        center_x = player_screen_x + player_screen_w / 2
        center_y = player_screen_y + player_screen_h / 2
        pygame.draw.circle(self.screen, (255, 0, 0), (int(center_x), int(center_y)), int(8 * zoom))

    def handle_input(self, event):
        # 不再需要处理按键监听碰撞调试切换了
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "MENU"
            if event.key == pygame.K_SPACE or event.key == pygame.K_b:
                return "BATTLE"
            if event.key == pygame.K_p:
                return "SAVE"
        return None
