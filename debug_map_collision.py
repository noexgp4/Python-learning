import pytmx
import os
import sys

# 设置默认编码为utf-8
sys.stdout.reconfigure(encoding='utf-8')

map_path = r"e:\Python learning\Python-learning\Python-learning\Assets\Map\testmap.tmx"
print(f"正在加载地图: {map_path}")

try:
    import pygame
    pygame.init()
    pygame.display.set_mode((1,1), pygame.NOFRAME)
    tmx_data = pytmx.load_pygame(map_path, pixelalpha=True)
except Exception as e:
    print(f"地图加载失败: {e}")
    exit()

print("-" * 30)
print("1. 检查图块集定义 - 自定义碰撞形状与 Wall 属性")
count_defs = 0
for gid, props in tmx_data.tile_properties.items():
    has_coll = 'objects' in props and len(props['objects']) > 0
    
    # 检查 Wall 属性
    is_wall_attr = False
    type_val = props.get('type') or props.get('class')
    wall_val = props.get('Wall')
    if type_val == 'Wall' or wall_val == True or str(wall_val).lower() == 'true':
        is_wall_attr = True
        
    if has_coll or is_wall_attr:
        count_defs += 1
        info = []
        if has_coll: info.append(f"含 {len(props['objects'])} 个碰撞体")
        if is_wall_attr: info.append("含 Wall 属性")
        # print(f"  GID={gid}: {', '.join(info)}")

print(f"  共发现 {count_defs} 个带有碰撞信息（形状或属性）的图块定义")

print("-" * 30)
print("2. 检查所有图层实例")
total_walls = 0

for layer in tmx_data.visible_layers:
    print(f"\n>> 扫描图层: [{type(layer).__name__}] '{layer.name}'")
    
    # === 情况 A: 图块层 (TiledTileLayer) ===
    if isinstance(layer, pytmx.TiledTileLayer):
        print("   (这是一个图块层)")
        layer_walls = 0
        for x, y, gid in layer:
            if gid == 0: continue
            
            props = tmx_data.get_tile_properties_by_gid(gid)
            if not props: continue
            
            has_shape = 'objects' in props and props['objects']
            
            is_wall_attr = False
            type_val = props.get('type') or props.get('class')
            if type_val == 'Wall': is_wall_attr = True
            elif props.get('Wall') == True or str(props.get('Wall')).lower() == 'true': is_wall_attr = True
            
            if has_shape or is_wall_attr:
                layer_walls += 1
                total_walls += 1
                if layer_walls <= 3: # 仅打印前3个
                    details = []
                    if has_shape: details.append("形状")
                    if is_wall_attr: details.append("属性")
                    print(f"   -> ({x},{y}) GID={gid} 有碰撞: {', '.join(details)}")
        
        if layer_walls == 0:
            print("   (未发现任何带碰撞的图块)")
        else:
            print(f"   (共发现 {layer_walls} 个碰撞图块)")

    # === 情况 B: 对象层 (TiledObjectGroup) ===
    elif isinstance(layer, pytmx.TiledObjectGroup):
        print("   (这是一个对象层)")
        layer_walls = 0
        for obj in layer:
            # 1. 检查直接画在对象层里的矩形（且位于 Collision 层）
            if layer.name == "Collision":
                print(f"   -> 发现直接碰撞对象: {obj.name} ({obj.x}, {obj.y})")
                layer_walls += 1
                total_walls += 1
            
            # 2. 检查对象是否是使用了带碰撞的图块 (Tile Object)
            elif hasattr(obj, 'gid') and obj.gid:
                # 注意：这里我们用简单的方式，不处理 flag 位，通常 pytmx 会处理
                props = tmx_data.get_tile_properties_by_gid(obj.gid)
                if props and 'objects' in props and props['objects']:
                    layer_walls += 1
                    total_walls += 1
                    print(f"   -> 发现图块对象碰撞: GID={obj.gid} ({obj.x}, {obj.y})")
        
        if layer_walls == 0 and layer.name != "Collision":
             print("   (未发现带碰撞的图块对象)")

print("-" * 30)
print(f"地图总计有效碰撞体数: {total_walls}")

pygame.quit()
