"""Compatibility shim for ``Scenes.data``.

This module attempts to load the data modules that currently live under
``Scenes/Battle/data`` by loading them directly from their file paths.
Loading by file avoids importing the ``Scenes.Battle`` package during
initialization and prevents circular import problems.
"""
import importlib.util
import os
import sys


def _load_module_from_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE_DIR = os.path.dirname(__file__)
_battle_data_dir = os.path.normpath(os.path.join(BASE_DIR, "..", "Battle", "data"))

JOBS_DATA = {}
MONSTERS_DATA = {}
SkillsLibrary = None

try:
    jobs_path = os.path.join(_battle_data_dir, "jobs_config.py")
    if os.path.exists(jobs_path):
        mod = _load_module_from_path("_scenes_jobs_config", jobs_path)
        JOBS_DATA = getattr(mod, "JOBS_DATA", {})

    monsters_path = os.path.join(_battle_data_dir, "monsters_config.py")
    if os.path.exists(monsters_path):
        mod = _load_module_from_path("_scenes_monsters_config", monsters_path)
        MONSTERS_DATA = getattr(mod, "MONSTERS_DATA", {})

    skills_path = os.path.join(_battle_data_dir, "skills_library.py")
    if os.path.exists(skills_path):
        mod = _load_module_from_path("_scenes_skills_library", skills_path)
        SkillsLibrary = getattr(mod, "SkillsLibrary", None)
except Exception:
    # If anything fails here, leave the defaults and allow importing code
    # to handle missing data (will raise clearer errors later).
    pass

__all__ = ["JOBS_DATA", "MONSTERS_DATA", "SkillsLibrary"]
