__author__ = 'yichengwang'

import subprocess
import time

while (1):
    print 'what kind fault do you want to inject?'
    print '1.Stop the nova api service'
    print '2.Stop the cinder api service'
    print '3.Stop the glance api service'
    print '4.Stop the ceilometer api service'
    print '5.Stop the neutron server'
    print '6.Stop the rsyslog service'
    print '7.Stop NIC'
    print '8.umount the disk'
    print '9.Stop the ceph'
    print '0.Stop the networking'
    print 'a.Stop the udev'
    print 'b.Stop database'
    index = raw_input()
    if index >= '0' and index <= '9':
        break
    if index == 'a' or index == 'b':
        break;

command = ('service rsyslog start')
p = subprocess.Popen(command, shell=True)

time.sleep(5)

if index == '1':
    command = ('python fault/stop_nova_api.py')
    p = subprocess.Popen(command, shell=True)
if index == '2':
    command = ('python fault/stop_cinder_api.py')
    p = subprocess.Popen(command, shell=True)
if index == '3':
    command = ('python fault/stop_glance_api.py')
    p = subprocess.Popen(command, shell=True)
if index == '4':
    command = ('python fault/stop_ceilometer_api.py')
    p = subprocess.Popen(command, shell=True)
if index == '5':
    command = ('python fault/stop_neutron_server.py')
    p = subprocess.Popen(command, shell=True)
if index == '6':
    command = ('python fault/stop_rsyslog.py')
    p = subprocess.Popen(command, shell=True)
if index == '7':
    command = ('python fault/umount_disk.py')
    p = subprocess.Popen(command, shell=True)
if index == '8':
    command = ('python fault/stop_NIC.py')
    p = subprocess.Popen(command, shell=True)
if index == '9':
    command = ('python fault/stop_ceph.py')
    p = subprocess.Popen(command, shell=True)
if index == '0':
    command = ('python fault/stop_networking.py')
    p = subprocess.Popen(command, shell=True)
if index == 'a':
    command = ('python fault/stop_udev.py')
    p = subprocess.Popen(command, shell=True)
if index == 'b':
    command = ('python fault/stop_database_mongodb.py')
    p = subprocess.Popen(command, shell=True)

time.sleep(60)
command = ('service rsyslog stop')
p = subprocess.Popen(command, shell=True)
