In the fault_injection.json file is the configuration file for the fault_injection and metaopenstack.
There are two things I will explain, the other things are the basic configuration.
The test_file is the place where the fault_injection is put on the node client.
The test_content is the type of the fault that will inject.
1.stop nova
2.stop cinder
3.stop glance
4.stop ceilometer
5.stop neutron
6.stop rsyslog
7.umount disk
8.stop NIC
9.stop ceph
0.stop networking
a.stop udev
b.stop database mongodb
