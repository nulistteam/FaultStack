import subprocess

command = ('service glance-api stop')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep glance-api')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '-'):
        break

print 'The glance-api has been shut down'

command = ('service glance-api start')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep glance-api')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '+'):
        break

print 'The glance-api has bee started'
