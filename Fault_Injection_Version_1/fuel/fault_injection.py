import paramiko
import json

MAIN_CONFIG_FILE = "fault_injection.json"

def get_config(filename = MAIN_CONFIG_FILE):
    with open(filename) as f:
        config = json.load(f)
    return config

CONFIG = get_config()

for i in range(0, len(CONFIG['servers'])):

    ip = CONFIG['servers'][i]['ip']
    username = CONFIG['servers'][i]['username']
    password = CONFIG['servers'][i]['password']
    test_file = CONFIG['servers'][i]['test_file']
    test_content = CONFIG['servers'][i]['test_content']

    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username = username, password=password)
    command = ('python %s' % (test_file))
    stdin, stdout, stderr = ssh.exec_command(command)
    stdin.write(test_content)
    ssh.close()

