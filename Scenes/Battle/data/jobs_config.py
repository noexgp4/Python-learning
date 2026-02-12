import json
import os

from Scenes.DataManager import data_manager

# 使用 DataManager 统一加载
# DataManager.jobs 已经在 load_all 中完成了与默认值的合并
JOBS = data_manager.jobs

def load_jobs_config(lang=None):
    """手动重新加载职业配置"""
    data_manager.load_all(lang)
    global JOBS
    JOBS = data_manager.jobs
    return JOBS
