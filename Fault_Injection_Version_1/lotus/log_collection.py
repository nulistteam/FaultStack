__author__ = 'yichengwang'

import os
import subprocess

HYPERVISOR_LOG_FILE = ['fuel_ceilometer.log', 'fuel_controller_0.log', 'fuel_controller_1.log', 'fuel_master.log']

HOME = os.environ.get('HOME')

listfile = os.listdir(HOME)
HYPERVISOR_LOG_DIR_NAME = 'HYPERVISOR_LOG'


LOG_DIR = None
LOG_DIR_NAME = '/var/log/rsyslog/hypervisor/'

HYPERVISOR_LOG_DIR = '/var/log/libvirt/'

for logfile in HYPERVISOR_LOG_FILE:
    command = ('cp /var/log/libvirt/qemu/%s %s' %(logfile, LOG_DIR_NAME))
    p = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE)
