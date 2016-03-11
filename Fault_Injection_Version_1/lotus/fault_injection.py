import paramiko
import json

MAIN_CONFIG_FILE = "fault_injection.json"

def get_config(filename = MAIN_CONFIG_FILE):
    with open(filename) as f:
        config = json.load(f)
    return config

CONFIG = get_config()

ip = CONFIG['node']['ip']
username = CONFIG['node']['username']
password = CONFIG['node']['password']
test_file = CONFIG['node']['test_file']

ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, username = username, password=password)
command = ('python %s' % (test_file))
stdin, stdout, stderr = ssh.exec_command(command)
ssh.close()
