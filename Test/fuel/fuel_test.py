__author__ = 'yichengwang'

import paramiko
import Test.tools.common as common

ssh = paramiko.SSHClient()

nodes = common.CONFIG['nodes']

for node in nodes:
    ip = node['hostname']
    username = node['username']
    ssh.connect(ip, username=username, look_for_keys=True)
    ssh.exec_command('sudo reboot')
    ssh.close()

for node in nodes:
    if node['role'] == 'controller':
        ip = node['hostname']
        username = node['username']
        test_file_dir = node['test_file_dir']
        test_file = node['test_file']
        ssh.connect(ip, username=username, look_for_keys=True)
        ssh.exec_command('cd %s && python %s', test_file_dir, test_file)
        ssh.close()