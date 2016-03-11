import subprocess

command = ('service cinder-api stop')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep cinder-api')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '-'):
        break

print 'The cinder-api has been shut down'

command = ('service cinder-api start')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep cinder-api')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '+'):
        break

print 'The cinder_api has bee started'
