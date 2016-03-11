import subprocess

command = ('service nova-api stop')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep nova-api')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '-'):
        break

print 'The nova-api has been shut down'

command = ('service nova-api start')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep nova-api')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '+'):
        break

print 'The node-api has bee started'
