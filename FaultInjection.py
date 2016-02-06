__author__ = 'yichengwang'

import nose
import Tempest
from nose.tools import with_setup
import Server_manager
import  Requirement

class FaultInjection():
    manager = None
    requirement = None

    def setup(self):
        self.manager = Server_manager.ServerManager()
        self.requirement = Requirement.requirements()
        self.manager.save_state()

    def teardown(self):
        self.manager.load_state()

    def fun1Start(self):
        print "Test1 Start"

    def fun1End(self):
        self.manager.load_state()
        print "Test1 End"

    def fun2Start(self):
        print "Test2 Start"

    def fun2End(self):
        self.manager.load_state()
        print "Test2 End"

    def fun3Start(self):
        print "Test3 Start"

    def fun3End(self):
        self.manager.load_state()
        print "Test3 End"

    @with_setup(fun1Start, fun1End)
    def testfun1(self):
        require = self.requirement.get()
        if not require:
            raise nose.SkipTest('The requirement is not satisfied')
        server = self.manager.get(role = 'compute')
        if not server:
            raise nose.SkipTest('Compute role needed for compute service test')
        self.manager.save_state()
        server.cmd()
        Tempest.run()

    @with_setup(fun2Start, fun2End)
    def testfun2(self):
        require = self.requirement.get()
        if not require:
            raise nose.SkipTest('The requirement is not satisfied')
        server = self.manager.get(role = 'controller')
        if not server:
            raise nose.SkipTest('Controller role needed for compute service test')
        self.manager.save_state()
        server.cmd()
        Tempest.run()

    @with_setup(fun3Start, fun3End)
    def testfun3(self):
        require = self.requirement.get()
        if not require:
            raise nose.SkipTest('The requirement is not satisfied')
        server = self.manager.get(role = 'keystone')
        if not server:
            raise nose.SkipTest('Keystone role needed for compute service test')
        self.manager.save_state()
        server.cmd()
        Tempest.run()

