__author__ = 'yichengwang'


import paramiko

ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect('10.0.20.5', 8000, 'root', 'r00tme')
ssh.exec_command('mkdir yes')

import FaultInjectionTest.Tools.ServerManager as ServerManager

s = ServerManager.ServerManager()
#s.connect()

a = s.get_all(role="compute")
print a



# y = s.servers(role="a")
#
# ROLES = set(["1", "2", "3"])
#
# def r(role=None, roles=None):
#     if role:
#         assert role in ROLES
#         assert not roles  # cannot use both
#     if roles:
#         roles = set(roles)
#         assert roles.issubset(ROLES)
#
# r(role="4")