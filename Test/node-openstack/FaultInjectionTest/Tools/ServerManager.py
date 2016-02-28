__author__ = 'yichengwang'

import FaultInjectionTest.Tools.Common as Common
import FaultInjectionTest.Tools.Server as Server
import FaultInjectionTest.Metaopenstack.Metaopenstack as Metaopenstack

ROLES = set(['keystone', 'swift_proxy', 'swift_data', 'controller', 'compute',
             'glance', 'cinder', 'neutron'])

class ServerManager():

    def __init__(self):
        self._servers = Server.create_servers(Common.CONFIG["servers"])

    def save_state(self, tag = ''):
        #save snapshot
        self._choose_state_restoration_action('save', tag)
        pass

    def load_state(self):
        #load snapshot
        self._choose_state_restoration_action('load', tag)
        self.connect()
        pass

    def servers(self, role=None, roles=None):
        if role:
            assert role in ROLES
            assert not roles  # cannot use both
        if roles:
            roles = set(roles)
            assert roles.issubset(ROLES)

        for server in self._servers:
            if not role and not roles:
                # no conditions, return any
                yield server
            elif role in server.roles \
                    or (roles and roles.issubset(server.roles)):
                yield server

    def get(self, role = None, roles = None):
        try:
            return self.servers(role, roles).next()
        except StopIteration:
            return None

    def get_all(self, role=None, roles=None):
        """Same as `get`, but returns a list of all the matching servers."""
        return list(self.servers(role, roles))

    def connect(self):
        for server in self._servers:
            server.connect()

    def disconnect(self):
        for server in self._servers:
            server.disconnect()

    def _choose_state_restoration_action(self, action, tag):
        assert action in ['save', 'load']
        man_type = Common.CONFIG['management']['type']

        if man_type == 'metaopenstack':
            if action == 'save':
                Metaopenstack.create_snapshots(tag)
            else:
                Metaopenstack.restore_snapshots(tag)
        else:
            raise Exception("This type of server management, '%s', is not supported, choose: metaopenstack" %(man_type))