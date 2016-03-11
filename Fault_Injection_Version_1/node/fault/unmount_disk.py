import subprocess

command = ('umount /dev/vda3')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('df | grep /dev/vda3')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    print s
    if (s == ''):
        break

print 'The /dev/vda3 has been umounted'

command = ('mount /dev/vda3')
p = subprocess.Popen(command, shell=True)

while (1):
    command = ('df | grep /dev/vda3')
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    s = p.stdout.read()
    if (s != ''):
        break

print 'The /dev/vda3 has bee mounted'
