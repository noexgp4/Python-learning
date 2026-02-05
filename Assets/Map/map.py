import pygame
import pytmx

class TiledMap:
    def __init__(self, filename):
        # 1. 加载地图数据
        # pixelalpha=True 确保支持透明度
        self.tmx_data = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight

        # 2. 初始化列表
        self.walls = [] 
        self.portals = [] # 存储传送门对象
        
        # 遍历所有图层（包括隐藏图层，因为传送门等触发器通常不需要显示）
        for layer in self.tmx_data.layers:
            # 策略 A: 瓦片图层 (Tile Layers)
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    if gid == 0: continue
                    # 1. 检查瓷砖是否有自定义碰撞形状
                    self._add_tile_collision(x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight, gid)
                    
                    # 2. 检查瓷砖是否带有 'Wall' 自定义属性
                    props = self.tmx_data.get_tile_properties_by_gid(gid)
                    if props:
                        is_wall = False
                        tile_type = props.get('type') or props.get('class')
                        if tile_type == 'Wall':
                            is_wall = True
                        elif props.get('Wall') == True or str(props.get('Wall')).lower() == 'true':
                            is_wall = True
                        
                        if is_wall:
                            self.walls.append(pygame.Rect(
                                x * self.tmx_data.tilewidth,
                                y * self.tmx_data.tileheight,
                                self.tmx_data.tilewidth,
                                self.tmx_data.tileheight
                            ))
            
            # 策略 B: 对象图层 (Object Groups)
            elif isinstance(layer, pytmx.TiledObjectGroup):
                # 尝试多种方式获取图层类型
                layer_class = getattr(layer, 'class', None) or layer.properties.get('class')
                layer_type = getattr(layer, 'type', None) or layer.properties.get('type')
                actual_layer_type = layer_class or layer_type
                
                # print(f"【调试】扫描对象层: '{layer.name}', Class: {layer_class}, Type: {layer_type}")
                
                for obj in layer:
                    # 尝试多种方式获取对象类型
                    obj_class = getattr(obj, 'class', None) or obj.properties.get('class')
                    obj_type = getattr(obj, 'type', None) or obj.properties.get('type')
                    actual_obj_type = obj_class or obj_type
                    
                    is_portal = False
                    if actual_obj_type and str(actual_obj_type).lower() == 'portal':
                        is_portal = True
                    elif actual_layer_type and str(actual_layer_type).lower() == 'portal':
                        is_portal = True
                        
                    if is_portal:
                        # 关键：将图层的所有自定义属性同步给该对象，确保护送 target_map 等属性
                        for key, value in layer.properties.items():
                            if key not in obj.properties:
                                obj.properties[key] = value
                        
                        self.portals.append(obj)
                        print(f"【地图】成功识别传送门: {getattr(obj, 'name', '未命名')} @ ({obj.x}, {obj.y}) [类型:{actual_obj_type}, 图层类型:{actual_layer_type}]")
                        continue 

                    # 1. 专门的 "Collision" 层中的几何形状
                    if layer.name == "Collision":
                        self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                    
                    # 2. 其他对象层中带 GID 的图块对象
                    elif hasattr(obj, 'gid') and obj.gid:
                        self._add_tile_collision(obj.x, obj.y, obj.gid)

    def _add_tile_collision(self, base_x, base_y, gid):
        """辅助方法：解析瓷砖编辑器 (Tile Editor) 中定义的碰撞形状"""
        props = self.tmx_data.get_tile_properties_by_gid(gid)
        if not props: return
        
        # 兼容处理：pytmx 不同版本对碰撞数据的存储键名不同
        # 旧版可能用 'objects'，新版通常用 'colliders' (TiledObjectGroup)
        coll_objs = []
        if 'colliders' in props:
            coll_objs = props['colliders']
        elif 'objects' in props:
            coll_objs = props['objects']
            
        for coll_obj in coll_objs:
            # 记录相对于地图全局的碰撞矩形
            self.walls.append(pygame.Rect(
                base_x + coll_obj.x,
                base_y + coll_obj.y,
                coll_obj.width,
                coll_obj.height
            ))

    def get_player_spawn_point(self):
        for obj_group in self.tmx_data.objectgroups:
            if obj_group.name == "PlayerSpawn":
                for obj in obj_group:
                    # pytmx 已处理 Y 轴偏移
                    return (obj.x, obj.y)
        return (0, 0) # 默认回退

    def make_map(self):
        """预渲染整个地图到一张 Surface，提高性能"""
        temp_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # 用一种适合你游戏的底色填充，防止黑边，这里用草地绿示例，可改
        temp_surface.fill((100, 150, 80)) 
        self.render(temp_surface)
        return temp_surface

    def render(self, surface):
        """渲染逻辑"""
        for layer in self.tmx_data.visible_layers:
            # 1. 渲染瓦片图层
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    if gid:
                        try:
                            tile = self.tmx_data.get_tile_image_by_gid(gid)
                            if tile:
                                draw_x = x * self.tmx_data.tilewidth
                                draw_y = y * self.tmx_data.tileheight
                                surface.blit(tile, (draw_x, draw_y))
                        except Exception:
                            pass
            
            # 2. 渲染对象图层中的图形对象（如果是图片对象）
            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if hasattr(obj, 'gid') and obj.gid:
                        try:
                            tile = self.tmx_data.get_tile_image_by_gid(obj.gid)
                            if tile:
                                # 注意：pytmx 已将 GID 物体坐标转换为左上角，直接绘制即可
                                surface.blit(tile, (obj.x, obj.y))
                        except Exception:
                            pass