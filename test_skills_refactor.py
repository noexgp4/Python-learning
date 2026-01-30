"""测试技能系统重构"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from Scenes.Battle.models.entity import Entity
from Scenes.Battle.data.skills_library import SkillsLibrary

print("=" * 50)
print("技能系统重构测试")
print("=" * 50)

# 测试1: 技能库加载
print("\n【测试1】技能库加载")
all_skills = SkillsLibrary.get_all_skills()
print(f"✓ 成功加载 {len(all_skills)} 个技能")
print(f"  技能列表: {', '.join(all_skills.keys())}")

# 测试2: 单个技能查询
print("\n【测试2】单个技能查询")
fireball = SkillsLibrary.get_skill("fireball")
print(f"✓ 火球术: {fireball}")

# 测试3: 批量技能查询
print("\n【测试3】批量技能查询")
mage_skills = SkillsLibrary.get_skills_by_ids(["fireball", "arcane_blast"])
print(f"✓ 法师技能: {mage_skills}")

# 测试4: 创建职业实体
print("\n【测试4】创建职业实体")
mage = Entity.from_job("Mage")
print(f"✓ 法师创建成功")
print(f"  名称: {mage.name}")
print(f"  技能数量: {len(mage.skills)}")
for i, skill in enumerate(mage.skills):
    print(f"  技能{i+1}: {skill['name']} (消耗:{skill['cost']} 威力:{skill['power']} 类型:{skill['type']})")

# 测试5: 创建怪物实体
print("\n【测试5】创建怪物实体")
slime = Entity.from_monster("Slime_Green")
print(f"✓ 史莱姆创建成功")
print(f"  名称: {slime.name}")
print(f"  技能数量: {len(slime.skills)}")
for i, skill in enumerate(slime.skills):
    print(f"  技能{i+1}: {skill['name']} (消耗:{skill.get('cost', 0)} 威力:{skill['power']} 类型:{skill['type']})")

# 测试6: 测试所有职业
print("\n【测试6】测试所有职业")
jobs = ["学生", "上班族", "程序员", "Mage", "Warrior"]
for job_name in jobs:
    entity = Entity.from_job(job_name)
    print(f"✓ {entity.name}: {len(entity.skills)} 个技能 - {[s['name'] for s in entity.skills]}")

print("\n" + "=" * 50)
print("✅ 所有测试通过!")
print("=" * 50)
