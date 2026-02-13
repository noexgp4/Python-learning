import os
import pygame
import random
import pytmx
from Assets.Map.map import TiledMap
from Assets.Map.camera import Camera
from Scenes.Battle.data.loader import Player
from Scenes.Battle.data.jobs_config import JOBS
from Scenes.UI.hud import StatusHUD
from Scenes.DataManager import data_manager
from Scenes.text import UIConfig, Panel, Label

class WorldScene:
    def __init__(self, screen, manager, job_name, map_name="testmap.tmx", spawn_pos=None, debug_collision=False, initial_stats=None):
        self.screen = screen
        self.manager = manager
        self.job_name = job_name
        self.map_name = map_name
        screen_width, screen_height = screen.get_size()
        
        # 提取初始属性
        istats = initial_stats or {}
        hp = istats.get("hp")
        mp = istats.get("mp")
        level = istats.get("level", 1)
        exp = istats.get("exp", 0)

        # 1. 计算路径并加载地图
        base_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
        map_path = os.path.join(base_dir, "Assets", "Map", map_name)
        self.tiled_map = TiledMap(map_path)
        print(f"【地图】加载了 {map_name}, 包含 {len(self.tiled_map.walls)} 个碰撞墙, {len(self.tiled_map.portals)} 个传送点, {len(self.tiled_map.world_objects)} 个可交互物体")
        
        # 2. 确定出生点
        if spawn_pos:
            actual_spawn = spawn_pos
        else:
            actual_spawn = self.tiled_map.get_player_spawn_point() or (0,0)
        
        self.player = Player(actual_spawn[0], actual_spawn[1], job_name, hp=hp, mp=mp, level=level, exp=exp)

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
        self.movement_accumulator = 0 # 遇怪步数累加器
        self.teleport_cooldown = 1.0  # 初始 1 秒传送冷却，防止循环传送
        
        # 掉落提示框状态
        self.showing_loot = False
        self.loot_item_name = ""

    def update(self, dt):
        # 1. 保存移动前的坐标
        old_x, old_y = self.player.x, self.player.y

        keys = pygame.key.get_pressed()
        self.player.update(
            dt, 
            keys, 
            self.tiled_map.walls,
            self.tiled_map.width, 
            self.tiled_map.height
        )

        # 2. 计算移动距离
        dx = self.player.x - old_x
        dy = self.player.y - old_y
        distance = (dx**2 + dy**2)**0.5
        
        if distance > 0:
            self.movement_accumulator += distance
            
            # 每移动 32 像素(约一格)检查一次遇怪
            if self.movement_accumulator >= 32:
                self.movement_accumulator = 0
                player_rect = self.player.get_rect()
                
                # 检查所有遇怪区域
                for area in self.tiled_map.encounter_areas:
                    if player_rect.colliderect(area["rect"]):
                        # 触发几率(例如 15%)
                        if random.random() < 0.15:
                            print(f"【遭遇】触发随机战斗！区域群组: {area['enemy_group']}")
                            return "BATTLE", {"enemy_group": area["enemy_group"]}

        # 3. 检测传送门碰撞
        # 增加一个简单的冷却判定，防止加载后瞬间再次触发
        if getattr(self, "teleport_cooldown", 0) > 0:
            self.teleport_cooldown -= dt
        else:
            player_rect = self.player.get_rect()
            for portal in self.tiled_map.portals:
                portal_rect = pygame.Rect(portal.x, portal.y, portal.width, portal.height)
                if player_rect.colliderect(portal_rect):
                    teleport_data = self._get_teleport_info(portal)
                    if teleport_data:
                        # 核心修复：记录“踏入传送门之前”的坐标作为记忆点，并额外往后推一点
                        # 这里我们将 old_x, old_y 传回，它是移动前的坐标
                        teleport_data["safe_pos"] = (old_x, old_y)
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
            "pos": spawn_pos,
            "is_return": properties.get("is_return") or properties.get("isReturn") or False
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
        
        # 5. 绘制可交互物体 (宝箱、NPC等)
        for obj in self.tiled_map.world_objects:
            obj_screen_x = (obj.rect.x + offset_x) * zoom
            obj_screen_y = (obj.rect.y + offset_y) * zoom
            
            if obj.image:
                img_w, img_h = obj.image.get_size()
                rect_h = obj.rect.height
                
                # 如果图片比占位符高（如房子、高大的NPC），向上偏移以保持底部对齐
                if img_h > rect_h:
                    obj_screen_y -= (img_h - rect_h) * zoom
                
                scaled_img = pygame.transform.scale(obj.image, (int(img_w * zoom), int(img_h * zoom)))
                screen.blit(scaled_img, (obj_screen_x, obj_screen_y))
            elif self.debug_collision:
                # 调试模式下为没有图片的物体画个框
                pygame.draw.rect(screen, (0, 255, 255), (obj_screen_x, obj_screen_y, obj.rect.width * zoom, obj.rect.height * zoom), 1)

        # 6. 绘制 HUD
        self.hud.draw(screen)

        # 7. 绘制获得物品对话框
        if self.showing_loot:
            self._draw_loot_dialog(screen)

    def _draw_loot_dialog(self, screen):
        dw, dh = 400, 150
        dx = (screen.get_width() - dw) // 2
        dy = (screen.get_height() - dh) // 2
        
        # 背景遮罩
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))
        
        # 对话框
        Panel(dx, dy, dw, dh, (30, 30, 30, 255), UIConfig.COLOR_YELLOW, 2, 12).draw(screen)
        
        msg = f"获得物品: {self.loot_item_name}"
        tw = UIConfig.NORMAL_FONT.size(msg)[0]
        Label(dx + (dw - tw) // 2, dy + 40, msg, "normal", UIConfig.COLOR_WHITE).draw(screen)
        
        hint = "[Enter / Space] 确认"
        hw = UIConfig.SMALL_FONT.size(hint)[0]
        Label(dx + (dw - hw) // 2, dy + dh - 40, hint, "small", UIConfig.COLOR_GRAY).draw(screen)

    def handle_events(self, event):
        if self.showing_loot:
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_e]:
                self.showing_loot = False
            return None, None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "MENU"
            if event.key == pygame.K_b:
                return "CHARACTER_MENU", "INVENTORY"
            if event.key == pygame.K_i:
                return "CHARACTER_MENU", "STATS"
            if event.key == pygame.K_k:
                return "CHARACTER_MENU", "SKILLS"
            if event.key == pygame.K_p:
                return "SAVE"
            
            # 交互处理 (宝箱、商店、NPC)
            if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_e]:
                player_rect = self.player.get_rect()
                interact_rect = player_rect.inflate(20, 20)
                
                for obj in self.tiled_map.world_objects:
                    if interact_rect.colliderect(obj.rect):
                        res, data = obj.interact()
                        if res == "CHEST_OPEN":
                            item_id = data.get("item_id")
                            item_name = self._get_item_display_name(item_id)
                            self.showing_loot = True
                            self.loot_item_name = item_name
                            return "CHEST_OPEN", data
                        elif res == "SHOP_OPEN":
                            print(f"【系统】打开商店: {data.get('shop_id')}")
                            return "SHOP_OPEN", data
                        elif res == "NPC_TALK":
                            name = data.get("name")
                            dialogue = data.get("dialogue", ["..."])[0] # 取第一句
                            self.showing_loot = True
                            self.loot_item_name = f"{name}: {dialogue}"
                            print(f"【对话】{name}: {dialogue}")
        return None, None

    def _get_item_display_name(self, item_id):
        # 遍历装备库查找名称
        for cat in ["weapons", "armors"]:
            item = data_manager.equips.get(cat, {}).get(item_id)
            if item:
                return item.get("name", item_id)
        return item_id
