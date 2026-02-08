import pygame
import pytmx

class TiledMap:
    def __init__(self, filename):
        # 1. 加载地图数据
        self.tmx_data = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight

        # 2. 初始化列表与查找表
        self.walls = [] 
        self.portals = [] 
        self.objects_by_name = {} # 新增：按名字索引所有对象
        
        for layer in self.tmx_data.layers:
            # 策略 A: 瓦片图层 (Tile Layers)
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    if gid == 0: continue
                    self._add_tile_collision(x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight, gid)
                    
                    props = self.tmx_data.get_tile_properties_by_gid(gid)
                    if props:
                        is_wall = False
                        if props.get('Wall') == True or str(props.get('Wall')).lower() == 'true' or props.get('type') == 'Wall' or props.get('class') == 'Wall':
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
                # 预提取图层类别和图层名称
                layer_class = (getattr(layer, 'class', None) or layer.properties.get('class') or layer.properties.get('type', '')).lower()
                layer_name = layer.name
                
                for obj in layer:
                    # 【核心修复】如果对象本身没有名字，则使用它所属图层的名字
                    # 这样用户在 Tiled 里给图层起名也能作为传送点的落脚点
                    obj_name = getattr(obj, 'name', None) or layer_name
                    if obj_name:
                        self.objects_by_name[obj_name] = obj

                    # 提取对象类别
                    obj_class = (getattr(obj, 'class', None) or obj.properties.get('class') or getattr(obj, 'type', None) or obj.properties.get('type', '')).lower()
                    
                    is_portal = (obj_class == 'portal' or layer_class == 'portal')
                        
                    if is_portal:
                        # 属性同步：确保护送自定义属性
                        for key, value in layer.properties.items():
                            if key not in obj.properties:
                                obj.properties[key] = value
                        self.portals.append(obj)
                        continue 

                    # 碰撞判定
                    if layer_name == "Collision":
                        self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                    elif hasattr(obj, 'gid') and obj.gid:
                        self._add_tile_collision(obj.x, obj.y, obj.gid)

    def get_object_by_name(self, name):
        """按名称检索任意对象"""
        return self.objects_by_name.get(name)

    def _add_tile_collision(self, base_x, base_y, gid):
        """辅助方法：解析瓷砖编辑器 (Tile Editor) 中定义的碰撞形状"""
        props = self.tmx_data.get_tile_properties_by_gid(gid)
        if not props: return
        
        coll_objs = props.get('colliders') or props.get('objects') or []
        for coll_obj in coll_objs:
            self.walls.append(pygame.Rect(
                base_x + coll_obj.x,
                base_y + coll_obj.y,
                coll_obj.width,
                coll_obj.height
            ))

    def get_player_spawn_point(self):
        """优先获取 PlayerSpawn 对象，否则尝试按图层查找"""
        spawn_obj = self.get_object_by_name("PlayerSpawn")
        if spawn_obj:
            return (spawn_obj.x, spawn_obj.y)
            
        for obj_group in self.tmx_data.objectgroups:
            if obj_group.name == "PlayerSpawn":
                for obj in obj_group:
                    return (obj.x, obj.y)
        return (0, 0)

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