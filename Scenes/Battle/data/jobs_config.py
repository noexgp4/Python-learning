import json
import os

# 1. 基础配置（作为所有职业的默认值）
BASE_CONFIG = {
    "frame_size": (16, 24),
    "cols": 4,
    "rows": 8,
    "render_size": (32, 48)
}

# 全局变量，供其他模块引用
JOBS = {}

def get_current_language():
    """尝试从 Core/config.json 读取当前语言设置"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "..", "..", "..", "Core", "config.json")
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get("language", "zh")
        except:
            pass
    return "zh"

def load_jobs_config(lang=None):
    """根据语言加载职业配置
    
    Args:
        lang: 语言代码 ('zh' 或 'en')，如果为 None 则从配置文件读取
    """
    global JOBS
    if lang is None:
        lang = get_current_language()
        
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 路径定义
    data_path = os.path.join(current_dir, "jobs.json")
    lang_file = f"jobs-{lang}.json"
    lang_path = os.path.join(current_dir, lang_file)
    
    # 临时字典用于合并
    temp_jobs = {}
    
    # 1. 加载基础数值数据
    if os.path.exists(data_path):
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                base_data = json.load(f)
                for key, data in base_data.items():
                    temp_jobs[key] = {**BASE_CONFIG, **data}
        except Exception as e:
            print(f"[Error] Failed to load jobs.json: {e}")

    # 2. 加载语言包数据
    if os.path.exists(lang_path):
        try:
            with open(lang_path, 'r', encoding='utf-8') as f:
                translation_data = json.load(f)
                for key, trans in translation_data.items():
                    if key in temp_jobs:
                        temp_jobs[key].update(trans)
        except Exception as e:
            print(f"[Error] Failed to load {lang_file}: {e}")
    else:
        print(f"[Warning] Translation file {lang_file} not found. Using default names.")

    # 3. 兜底逻辑：确保 'name' 字段存在
    for key, job in temp_jobs.items():
        if "name" not in job:
            job["name"] = key

    # 更新全局变量的内容，而不是重新赋值引用，确保已导入此变量的模块也能看到变化
    JOBS.clear()
    JOBS.update(temp_jobs)
    return JOBS

# 初始加载
load_jobs_config()
