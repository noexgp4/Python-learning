import json
import os

class SkillsLibrary:
    """技能库管理器 - 负责加载和查询技能数据"""
    
    _skills_data = None
    
    @classmethod
    def load_skills(cls):
        """从 skills.json 加载技能数据"""
        if cls._skills_data is None:
            current_dir = os.path.dirname(__file__)
            skills_path = os.path.join(current_dir, 'skills.json')
            
            with open(skills_path, 'r', encoding='utf-8') as f:
                cls._skills_data = json.load(f)
        
        return cls._skills_data
    
    @classmethod
    def get_skill(cls, skill_id):
        """根据技能ID获取技能详情
        
        Args:
            skill_id: 技能ID (如 'fireball', 'heavy_slash')
            
        Returns:
            技能字典,包含 name, cost, type, power 等属性
            如果技能不存在,返回 None
        """
        skills = cls.load_skills()
        return skills.get(skill_id)
    
    @classmethod
    def get_skills_by_ids(cls, skill_ids):
        """根据技能ID列表批量获取技能详情
        
        Args:
            skill_ids: 技能ID列表 (如 ['fireball', 'arcane_blast'])
            
        Returns:
            技能字典列表
        """
        skills = cls.load_skills()
        return [skills[sid] for sid in skill_ids if sid in skills]
    
    @classmethod
    def get_all_skills(cls):
        """获取所有技能"""
        return cls.load_skills()
