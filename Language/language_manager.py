import json
import os

class LanguageManager:
    def __init__(self, language="en"):
        self.language = language
        self.texts = {}
        self.load_language()

    def load_language(self):
        """根据语言从 DataManager 加载对应的文本"""
        from Scenes.DataManager import data_manager
        # 确保 DataManager 加载了正确的语言
        if data_manager.config.get("language") != self.language:
             data_manager.load_all(self.language)
        self.texts = data_manager.texts

    def get_text(self, category, key):
        """根据类别和键获取文本"""
        return self.texts.get(category, {}).get(key, f"未找到 {category} - {key} 的文本")

    def change_language(self, new_language):
        """切换语言"""
        self.language = new_language
        self.load_language()
