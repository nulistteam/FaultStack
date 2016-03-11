import time
import subprocess

import json

MAIN_CONFIG_FILE = "hypervisor.json"

def get_config(filename = MAIN_CONFIG_FILE):
    with open(filename) as f:
        config = json.load(f)
    return config

CONFIG = get_config()

for i in range(0, len(CONFIG['VM'])):

    command = ('virsh shutdown %s' % (CONFIG['VM'][i]['node']))
    p = subprocess.Popen(command, shell=True)

    time.sleep(60)
    while (1):
        command = ('virsh domstate %s' % (CONFIG['VM'][i]['node']))
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        s = p.stdout.read()
        if (s[0] == 's'):
            break
        command = ('virsh shutdown %s' % (CONFIG['VM'][i]['node']))
        p = subprocess.Popen(command, shell=True)
        time.sleep(10)

    print 'The node has been shut down'

    command = ('virsh start %s' % (CONFIG['VM'][i]['node']))
    p = subprocess.Popen(command, shell=True)
    time.sleep(60)
    while (1):
        command = ('virsh domstate %s' % (CONFIG['VM'][i]['node']))
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        s = p.stdout.read()
        if (s[0] == 'r'):
            break

    print 'The node has bee started'

command = ('python log_collection.py')
p = subprocess.Popen(command, shell=True)
