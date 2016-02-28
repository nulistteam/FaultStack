__author__ = 'yichengwang'

import os
import json


PROJ_DIR = os.path.join(os.path.dirname(__file__), "..")
CONFIG_DIR = os.path.join(PROJ_DIR, "config")
listfile = os.listdir(CONFIG_DIR)
MAIN_CONFIG_FILE = None
for file in listfile:
    if file[-5:] == '.json':
        MAIN_CONFIG_FILE = file
        break
MAIN_CONFIG_FILE = os.path.join(CONFIG_DIR, MAIN_CONFIG_FILE)

def get_config(filename = MAIN_CONFIG_FILE):
     with open(os.path.join(CONFIG_DIR, filename)) as f:
         config = json.load(f)
     return config

CONFIG = get_config()
print CONFIG