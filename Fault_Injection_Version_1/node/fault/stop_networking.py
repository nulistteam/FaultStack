import subprocess

command = ('service networking stop')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep networking')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '-'):
        break

print 'The networking has been shut down'

command = ('service networking start')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep networking')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '+'):
        break

print 'The networking has bee started'
