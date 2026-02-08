import os
import pygame
from Assets.Map.map import TiledMap
from Assets.Map.camera import Camera
from Scenes.Battle.data.loader import Player
from Scenes.Battle.data.jobs_config import JOBS
from Scenes.UI.hud import StatusHUD

class WorldScene:
    def __init__(self, screen, manager, job_name, map_name="testmap.tmx", spawn_pos=None, debug_collision=False):
        self.screen = screen
        self.manager = manager
        self.job_name = job_name
        self.map_name = map_name
        screen_width, screen_height = screen.get_size()

        # 1. 计算路径并加载地图
        base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
        map_path = os.path.join(base_dir, "Assets", "Map", map_name)
        self.tiled_map = TiledMap(map_path)
        print(f"【地图】加载了 {map_name}, 包含 {len(self.tiled_map.walls)} 个碰撞墙, {len(self.tiled_map.portals)} 个传送点")

        # 2. 确定出生点
        if spawn_pos:
            actual_spawn = spawn_pos
        else:
            actual_spawn = self.tiled_map.get_player_spawn_point() or (0,0)
        
        self.player = Player(actual_spawn[0], actual_spawn[1], job_name)
        self.map_surface = self.tiled_map.make_map()
        
        # 3. 初始化 HUD
        self.hud = StatusHUD(self.player)
        
        # 4. 初始化相机
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

        # 检测传送门碰撞
        player_rect = self.player.get_rect()
        for portal in self.tiled_map.portals:
            portal_rect = pygame.Rect(portal.x, portal.y, portal.width, portal.height)
            if player_rect.colliderect(portal_rect):
                # 返回传送指令和数据，交给 main.py 处理加载页
                teleport_data = self._get_teleport_info(portal)
                if teleport_data:
                    return "TELEPORT", teleport_data
                break

        self.camera.update(self.player.x, self.player.y, self.player.width, self.player.height)
        return None, None

    def _get_teleport_info(self, portal):
        """仅提取传送信息，不执行切换"""
        properties = portal.properties
        target_map = (properties.get("target_map") or 
                      properties.get("targetMap") or 
                      properties.get("destination"))
        
        target_portal_name = (properties.get("target_portal") or 
                             properties.get("targetPortal"))

        if not target_map:
            return None

        # 预计算落脚点，确保加载完后位置正确
        base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
        target_map_path = os.path.join(base_dir, "Assets", "Map", target_map)
        
        spawn_pos = (0, 0)
        try:
            temp_map = TiledMap(target_map_path)
            if target_portal_name:
                p = temp_map.get_object_by_name(target_portal_name)
                if p:
                    spawn_pos = (p.x, p.y + p.height + 10) # 增加一些位移防止循环触发
                else:
                    spawn_pos = temp_map.get_player_spawn_point()
            else:
                spawn_pos = temp_map.get_player_spawn_point()
        except:
            pass

        return {
            "map": target_map,
            "pos": spawn_pos
        }

    def draw(self, screen=None):
        if screen is None:
            screen = self.screen
            
        # 1. 应用相机变换渲染地图
        self.camera.apply(screen, self.map_surface)
        
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
                pygame.draw.rect(screen, (255, 0, 0), debug_rect, 1)

        # 4. 绘制玩家
        player_screen_x = (self.player.x + offset_x) * zoom
        player_screen_y = (self.player.y + offset_y) * zoom
        player_screen_w = self.player.width * zoom
        player_screen_h = self.player.height * zoom
        
        player_img = self.player.get_current_image()
        if player_img:
            draw_img = pygame.transform.scale(player_img, (int(player_screen_w), int(player_screen_h)))
            screen.blit(draw_img, (player_screen_x, player_screen_y))
        
        # 5. 绘制 HUD
        self.hud.draw(screen)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "MENU"
            if event.key == pygame.K_SPACE or event.key == pygame.K_b:
                return "BATTLE"
            if event.key == pygame.K_p:
                return "SAVE"
        return None
