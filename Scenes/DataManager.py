# utils/data_manager.py
import json
import os

class DataManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.equips = {}
        self.monsters = {}
        self.jobs = {}
        self.levels = {}
        self.config = {}
        self.story = {}
        self.texts = {}
        self._initialized = True

    def load_all(self, lang=None):
        """一次性加载所有基础数据库"""
        # 项目根目录
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # 1. 加载基础配置以获取语言
        config_path = os.path.join(base_dir, "Core", "config.json")
        new_config = self._load_json(config_path)
        self.config.clear()
        self.config.update(new_config)
        
        if lang is None:
            lang = self.config.get("language", "zh")

        # 2. 核心数据路径
        battle_data_dir = os.path.join(base_dir, "Scenes", "Battle", "data")
        
        self.equips.clear()
        self.equips.update(self._load_json(os.path.join(battle_data_dir, "equips.json")))
        
        self.monsters.clear()
        self.monsters.update(self._load_json(os.path.join(battle_data_dir, "monsters.json")))
        
        self.levels.clear()
        self.levels.update(self._load_json(os.path.join(battle_data_dir, "levels.json")))
        
        # 3. 剧情数据
        self.story.clear()
        self.story.update(self._load_json(os.path.join(base_dir, "Scenes", "story.json")))
        
        # 4. 加载职业数据 (基础 + 语言包)
        base_jobs = self._load_json(os.path.join(battle_data_dir, "jobs.json"))
        lang_file = f"jobs-{lang}.json"
        lang_jobs = self._load_json(os.path.join(battle_data_dir, lang_file))
        
        # 职业基础默认配置
        job_defaults = {
            "frame_size": [16, 24],
            "cols": 4,
            "rows": 8,
            "render_size": [32, 48],
            "world_speed": 100
        }

        self.jobs.clear()
        for key, data in base_jobs.items():
            combined = job_defaults.copy()
            combined.update(data)
            if key in lang_jobs:
                combined.update(lang_jobs[key])
            if "name" not in combined:
                combined["name"] = key
            self.jobs[key] = combined

        # 5. UI 文本
        lang_dir = os.path.join(base_dir, "Language")
        self.texts.clear()
        self.texts.update(self._load_json(os.path.join(lang_dir, f"{lang}.json")))

        print(f"--- 游戏数据库初始化完成 (语言: {lang}) ---")

    def _load_json(self, path):
        try:
            if not os.path.exists(path):
                return {}
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"加载失败 {path}: {e}")
            return {}

    def get_equip(self, category, item_id):
        return self.equips.get(category, {}).get(item_id)

    def get_job(self, job_id):
        return self.jobs.get(job_id)

    def get_monster(self, monster_id):
        return self.monsters.get(monster_id)

    def get_text(self, category, key):
        return self.texts.get(category, {}).get(key, f"NO_TEXT: {category}.{key}")

# 导出全局单例
data_manager = DataManager()