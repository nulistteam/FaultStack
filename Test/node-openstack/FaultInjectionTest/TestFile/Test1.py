__author__ = 'yichengwang'

import nose
import FaultInjection.Tools.Server_manager as Server_manager
import FaultInjection.Tools.Common as Common
import FaultInjectionTest.Tempest.Tempest as Tempest

class Test1():
    manager = None

    @classmethod
    def setupClass(cls):
        cls.manager = Server_manager.ServerManager()
        if "tempest" not in Common.CONFIG:
            raise nose.SkipTest("Tempest required to verify Nova Service")
        cls.manager.save_state()

    @classmethod
    def teardownClass(cls):
        cls.manager.load_state()

    def test_nova_compute_restart(self):
        server = self.manager.get(role='compute')
        if not server:
            raise nose.SkipTest("Compute role needed for compute service test")
        server.cmd("service openstack-nova-compute restart")
        Tempest.run(test_type="smoke", include="compute.servers")

    def test_nova_network_restart(self):
        server = self.manager.get(role='controller')
        if not server:
            raise nose.SkipTest("Compute role needed for compute service test")
        res = server.cmd("service openstack-nova-network status",
                         ignore_failures=True)
        if res.exit_code == 1:  # maybe neutron is being used
            raise nose.SkipTest("Service nova-network doesn't seem to exist")
        Tempest.run(test_type="smoke", include="network")

    def test_keystone_restart(self):
        server = self.manager.get(role='keystone')
        if not server:
            raise nose.SkipTest("Keystone role needed for keystone test")
        server.cmd("service openstack-keystone restart")
        Tempest.run(test_type="smoke", include="identity")

    def test_swift_proxy_restart(self):
        server = self.manager.get(role='swift_proxy')
        if not server:
            raise nose.SkipTest("Swift_proxy role needed for swift test")
        server.cmd("service openstack-swift-proxy restart")
        Tempest.run(test_type="smoke", include="object_storage")