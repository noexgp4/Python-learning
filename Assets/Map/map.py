import pygame
import pytmx

class TiledMap:
    def __init__(self, filename):
        # pixelalpha=True 确保支持透明度
        self.tmx_data = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight

    def render(self, surface):
        # 遍历所有图层
        for layer in self.tmx_data.visible_layers:
            # 只有是瓦片图层（TiledTileLayer）时才绘制
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
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

    def make_map(self):
        """预渲染整个地图到一张 Surface，提高性能"""
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.render(temp_surface)
        return temp_surface