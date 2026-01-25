import json
import os

class LanguageManager:
    def __init__(self, language="en"):
        self.language = language
        self.texts = {}
        self.load_language()

    def load_language(self):
        """根据语言加载对应的文本文件"""
        # 使用相对于当前脚本的文件路径，确保在不同目录下运行都能找到文件
        file_path = os.path.join(os.path.dirname(__file__), f"{self.language}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                self.texts = json.load(f)
        else:
            print(f"语言文件 {self.language}.json 不存在，使用默认英文文本。")
            self.language = "en"
            self.load_language()

    def get_text(self, category, key):
        """根据类别和键获取文本"""
        return self.texts.get(category, {}).get(key, f"未找到 {category} - {key} 的文本")

    def change_language(self, new_language):
        """切换语言"""
        self.language = new_language
        self.load_language()
