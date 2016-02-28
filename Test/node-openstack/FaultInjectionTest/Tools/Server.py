__author__ = 'yichengwang'

import paramiko
import subprocess
import socket

def create_servers(configs):
    servers = []
    for config in configs:
        servers.append(Server(**config))
    return servers

class LocalServer():
    def cmd(self, command):
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        p.wait()
        return p.stdout.read()

class Server():

    def __init__(self, hostname=None, ip=None, username="root", password=None,
                 roles=None, extra_disks=None, **kwargs):
        if not (hostname or ip):
            raise Exception("Either hostname or IP address required")
        self.hostname = hostname
        if not ip:
            self.ip = socket.gethostbyname(self.hostname)
        else:
            self.ip = ip
        self.roles = roles or set()
        self.disks = extra_disks
        if "root_password" in kwargs and not password:
            username = "root"
            password = kwargs["root_password"]
        self._username = username
        self._password = password

        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connect()

    def connect(self):
        self._ssh.connect(self.ip, username=self._username,
                          password=self._password)

    def disconnect(self):
        self._ssh.close()

    def __del__(self):
        self.disconnect()

    def cmd(self, command):
        self._ssh.exec_command(command)