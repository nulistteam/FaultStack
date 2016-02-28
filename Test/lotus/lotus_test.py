__author__ = 'yichengwang'

import paramiko
import Test.tools.common as common

ssh = paramiko.SSHClient()

ip = common.CONFIG['ip']
username = common.CONFIG['username']
password = common.CONFIG['password']
test_file_dir = common.CONFIG['test_file_dir']
test_file = common.CONFIG['test_file']

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(ip, 22, username, password)

ssh.exec_command('cd %s && python %', test_file_dir, test_file)

ssh.close()