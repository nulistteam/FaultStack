import subprocess

command = ('service ceilometer-api stop')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep ceilometer-api')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '-'):
        break

print 'The ceilometer-api has been shut down'

command = ('service ceilometer-api start')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep ceilometer-api')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '+'):
        break

print 'The ceilometer_api has bee started'
