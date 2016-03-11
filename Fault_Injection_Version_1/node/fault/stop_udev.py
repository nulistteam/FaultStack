import subprocess

command = ('service udev stop')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep udev')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '-'):
        break

print 'The udev has been shut down'

command = ('service udev start')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('service --status-all | grep udev')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s[3] == '+'):
        break

print 'The udev has bee started'
