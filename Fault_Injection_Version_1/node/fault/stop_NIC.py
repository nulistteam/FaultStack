import subprocess

command = ('ifdown eth0')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('if link show eth0')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s.find('UP') == -1):
        break

print 'The NIC has been shut down'

command = ('ifup eth0')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('if link show eth0')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s.find('UP') != -1):
        break

print 'The NIC has been started'
