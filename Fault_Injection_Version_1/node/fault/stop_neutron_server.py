import subprocess

command = ('service neutron-server stop')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep neutron-server')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '-'):
        break

print 'The neutron-server has been shut down'

command = ('service neutron-server start')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep neutron-server')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '+'):
        break

print 'The neutron-server has bee started'
