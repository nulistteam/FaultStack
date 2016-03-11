import subprocess

command = ('service rsyslog stop')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep rsyslog')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '-'):
        break

print 'The rsyslog has been shut down'

command = ('service rsyslog start')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep rsyslog')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '+'):
        break

print 'The rsyslog has bee started'
