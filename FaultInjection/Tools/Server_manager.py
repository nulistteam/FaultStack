__author__ = 'yichengwang'

import logging
import Common
import FaultInjection.state_save.metaopenstack as metaopenstack
import FaultInjection.Tools.Server as server_tools

LOG = logging.getLogger(__name__)

class ServerManager():

    def __init__(self):
        self.servers = server_tools.create_servers(Common.CONFIG['server'])

    def save_state(self, tag = ''):
        #save snapshot
        self._choose_state_restoration_action('save', tag)
        pass

    def load_state(self):
        #load snapshot
        self._choose_state_restoration_action('load', tag)
        self.connect()
        pass

    def get(self, role = None, roles = None):
        try:
            return self.servers(role, roles).next()
        except StopIteration:
            return None

    def connect(self):
        for server in self._servers:
            server.connect()

    def _choose_state_restoration_action(self, action, tag):
        assert action in ['save', 'load']
        man_type = Common.CONFIG['management']['type']

        if man_type == 'metaopenstack':
            if action == 'save':
                metaopenstack.save_snapshot(tag)
            else:
                metaopenstack.load_snapshot(tag)
        elif man_type == 'none':
            LOG.info('State save and load has been turned off')
        else:
            raise Exception("This type of server management, '%s', is not supported, choose: metaopenstack" %(man_type))