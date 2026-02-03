import pytmx
import sys

sys.stdout.reconfigure(encoding='utf-8')
map_path = r"e:\Python learning\Python-learning\Python-learning\Assets\Map\testmap.tmx"

print("--- 深度诊断 GID 3 (对应 tile id 2) ---")
try:
    import pygame
    pygame.init()
    pygame.display.set_mode((1,1), pygame.NOFRAME)
    tmx = pytmx.load_pygame(map_path, pixelalpha=True)
    
    # Building tileset starts at GID 1. Tile id 2 => GID 3.
    target_gid = 3
    print(f"尝试获取 GID {target_gid} 的属性...")
    
    props = tmx.get_tile_properties_by_gid(target_gid)
    if props:
        print(f"GID {target_gid} 属性字典 keys: {list(props.keys())}")
        if 'objects' in props:
            print(f"GID {target_gid} 包含 'objects': {props['objects']}")
            print(f"objects 数量: {len(props['objects'])}")
        else:
            print(f"错误: GID {target_gid} 的属性中不包含 'objects' 键！")
            
        print(f"完整属性: {props}")
    else:
        print(f"警告: GID {target_gid} 返回了 None (无属性)")
        
    print("\n--- 遍历 tile_properties 寻找碰撞信息 ---")
    found_any = False
    for gid, p in tmx.tile_properties.items():
        if 'objects' in p and p['objects']:
            print(f"GID {gid} 有碰撞对象: {len(p['objects'])} 个")
            found_any = True
    
    if not found_any:
        print("整个 tile_properties 中没有发现任何 'objects' 数据！")

except Exception as e:
    print(e)
pygame.quit()
