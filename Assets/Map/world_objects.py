import pygame
import os
from Scenes.DataManager import data_manager

class WorldObject(pygame.sprite.Sprite):
    """地图物体基类，处理交互位置、绘制和基础碰撞状态"""
    def __init__(self, obj_data):
        super().__init__()
        self.x = obj_data.x
        self.y = obj_data.y
        self.width = obj_data.width
        self.height = obj_data.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.properties = obj_data.properties
        self.name = getattr(obj_data, 'name', "")
        
        self.image = None
        self.state = "idle"

    def _load_asset(self, filename):
        """通用资源加载助手"""
        if not filename: return None
        # 根据实际存放路径调整，这里兼容 Assets/Tiles 和 Assets/Characters
        search_paths = [
            "Assets/Tiles", 
            "Assets/Characters", 
            "Assets/Tiles/Characters",
            "Assets/Tiles/building",
            "Assets/Tiles/Decorative items"
        ]
        for p in search_paths:
            full_path = os.path.join(p, filename)
            if os.path.exists(full_path):
                try:
                    return pygame.image.load(full_path).convert_alpha()
                except:
                    pass
        print(f"【警告】未找到资源文件: {filename}")
        return None

    def update(self, dt):
        pass

    def draw(self, screen, camera):
        if self.image:
            # 获取在地图上的基础绘制位置
            pos = camera.apply_rect(self.rect)
            
            # 获取图片尺寸和 rect 尺寸
            img_w, img_h = self.image.get_size()
            # 注意：camera.apply_rect 返回的是屏幕上的坐标，缩放已经在 Camera 里处理了吗？
            # 查阅 Camera.py，apply_rect 只是做了减法 (offset_x, offset_y)，缩放是在 WorldScene 绘制时手动乘的。
            # 这里我们遵循 WorldScene 的绘制习惯。
            
            screen.blit(self.image, pos)

    def interact(self):
        pass

class ChestObject(WorldObject):
    def __init__(self, obj_data):
        super().__init__(obj_data)
        self.chest_id = self.properties.get("chest_id", "default_chest")
        
        # 1. 获取 JSON 数据 (包含图片路径)
        chest_data = data_manager.get_chest_data(self.chest_id) or {}
        self.item_id = self.properties.get("item_id") or chest_data.get("item_id", "none")
        self.is_opened = chest_data.get("is_opened", False)
        
        # 2. 从 JSON 读取图片名称
        sprite_closed = chest_data.get("sprite_closed", "Treasure Chest.png")
        sprite_opened = chest_data.get("sprite_opened", "openchest.png")
        
        self.images = {
            "closed": self._load_asset(sprite_closed),
            "opened": self._load_asset(sprite_opened)
        }
        
        self.state = "opened" if self.is_opened else "closed"
        self.image = self.images[self.state] or pygame.Surface((32, 32))

    def interact(self):
        if self.state == "closed":
            self.state = "opened"
            self.image = self.images["opened"]
            self.is_opened = True
            return "CHEST_OPEN", {"item_id": self.item_id, "chest_id": self.chest_id}
        return None, None

class NPCObject(WorldObject):
    """通用 NPC 类，从 npcs.json 获取数据"""
    def __init__(self, obj_data):
        super().__init__(obj_data)
        # 优先使用属性里的 npc_id 或 npc_sprite 名作为索引
        self.npc_id = self.properties.get("npc_id") or self.properties.get("npc_sprite") or "default_npc"
        
        # 获取 JSON 数据
        self.npc_data = data_manager.get_npc_data(self.npc_id) or {}
        self.display_name = self.npc_data.get("name", self.npc_id)
        self.dialogues = self.npc_data.get("dialogue", ["..."])
        
        # 加载图片
        sprite_file = self.npc_data.get("sprite")
        self.image = self._load_asset(sprite_file)
        
        # 如果没图片，画个圆头方块做占位
        if not self.image:
             self.image = pygame.Surface((32, 48), pygame.SRCALPHA)
             pygame.draw.rect(self.image, (100, 100, 250), (0, 0, 32, 48), border_radius=5)
             pygame.draw.circle(self.image, (250, 220, 200), (16, 12), 10)

    def interact(self):
        # 暂时返回对话数据，后续由 WorldScene 弹出对话框
        return "NPC_TALK", {
            "name": self.display_name,
            "dialogue": self.dialogues,
            "shop_id": self.npc_data.get("shop_id")
        }

class ShopObject(NPCObject):
    """特殊的 NPC 或 建筑，关联商店数据"""
    def __init__(self, obj_data):
        super().__init__(obj_data)
        self.shop_id = self.properties.get("shop_id") or self.npc_data.get("shop_id")
        self.shop_data = data_manager.get_shop_data(self.shop_id) or {}
        
        # 【核心】如果商店配置了图片（如房子），则覆盖 NPC 图片
        shop_sprite = self.shop_data.get("sprite")
        if shop_sprite:
            new_img = self._load_asset(shop_sprite)
            if new_img:
                self.image = new_img

    def interact(self):
        # 如果有商店 ID，优先进入商店逻辑
        return "SHOP_OPEN", {
            "shop_id": self.shop_id, 
            "shop_data": self.shop_data,
            "npc_name": self.display_name
        }

def create_world_object(obj_data):
    """工厂函数"""
    obj_type = (getattr(obj_data, 'type', None) or obj_data.properties.get('type', '')).lower()
    obj_class = (getattr(obj_data, 'class', None) or obj_data.properties.get('class', '')).lower()
    
    # 逻辑优先级：宝箱 -> 商店 -> 普NPC
    if obj_type == "chest" or obj_class == "chest":
        return ChestObject(obj_data)
    elif obj_type == "npc_shop" or obj_class == "shop" or obj_data.properties.get("shop_id"):
        return ShopObject(obj_data)
    elif obj_type == "npc" or obj_class == "npc":
        return NPCObject(obj_data)
    
    return None