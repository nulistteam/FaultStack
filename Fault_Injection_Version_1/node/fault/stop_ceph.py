import subprocess

command = ('service ceph stop')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep ceph')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '-'):
        break

print 'The ceph has been shut down'

command = ('service ceph start')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep ceph')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '+'):
        break

print 'The ceph has been started'
