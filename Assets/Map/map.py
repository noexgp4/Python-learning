import pygame
import pytmx

class TiledMap:
    def __init__(self, filename):
        # pixelalpha=True 确保支持透明度
        self.tmx_data = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight

    def get_player_spawn_point(self):
        """获取PlayerSpawn图层中的玩家出生点坐标
        
        Returns:
            tuple: (x, y) 玩家出生点的像素坐标，如果找不到返回 None
        """
        for obj_group in self.tmx_data.objectgroups:
            if obj_group.name == "PlayerSpawn":
                # PlayerSpawn 图层中应该有一个对象表示出生点
                for obj in obj_group:
                    # 返回该对象的坐标
                    return (obj.x, obj.y)
        return None

    def render(self, surface):
        # 遍历所有图层
        for layer in self.tmx_data.visible_layers:
            # 渲染瓦片图层（TiledTileLayer）
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    if gid:  # 只绘制有效的瓦片（gid != 0）
                        try:
                            tile = self.tmx_data.get_tile_image_by_gid(gid)
                            if tile:
                                # 计算位置：格子坐标 * 瓦片像素大小
                                draw_x = x * self.tmx_data.tilewidth
                                draw_y = y * self.tmx_data.tileheight
                                surface.blit(tile, (draw_x, draw_y))
                        except Exception as e:
                            # 资源缺失时跳过，避免程序崩溃
                            pass
            
            # 渲染对象图层中的图形对象（gid > 0 的对象）
            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    # 只渲染有gid的对象（图形对象）
                    if hasattr(obj, 'gid') and obj.gid:
                        try:
                            tile = self.tmx_data.get_tile_image_by_gid(obj.gid)
                            if tile:
                                surface.blit(tile, (obj.x, obj.y))
                        except Exception as e:
                            # 资源缺失时跳过
                            pass

    def make_map(self):
        """预渲染整个地图到一张 Surface，提高性能"""
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # 用绿色填充作为背景（表示草地），防止空位显示黑块
        temp_surface.fill((100, 150, 80))  # 草地绿色
        self.render(temp_surface)
        return temp_surface