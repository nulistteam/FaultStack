import subprocess

command = ('service mongodb stop')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep mongodb')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    print s
    if (s[3] == '-'):
        break

print 'The mongodb has been stopped'

command = ('service mongodb start')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep mongodb')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    print s
    if (s[3] == '+'):
        break

print 'The mongodb has bee started'
