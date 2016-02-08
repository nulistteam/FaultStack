__author__ = 'yichengwang'

import os
import json

PROJ_DIR = os.path.join(os.path.dirname(__file__), "..")
CONFIG_DIR = os.path.join(PROJ_DIR, "Config")

MAIN_CONFIG_FILE = os.environ.get("MAIN_CONFIG_FILE", "config.json")

def get_config(filename = MAIN_CONFIG_FILE):
    with open(os.path.join(CONFIG_DIR, filename)) as f:
        config = json.load(f)
    return config

CONFIG = get_config()