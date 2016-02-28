__author__ = 'yichengwang'

import logging
import exceptions
import FaultInjectionTest.Tools.Common as Common
import FaultInjectionTest.Tools.Server as Server

LOG = logging.getLogger(__name__)

def run(include=None, test_type=None, test_dir="api",
        regexp=None):

    tempest_dir = Common.CONFIG.get("tempest", None) #get the file position of tempest
    if not tempest_dir:
        raise Exception("Tempest directory not provided in config")

    if not regexp:
        regexp = "tempest\%s\%s. --%s" % (test_dir, include, test_type)
    cmd = ("cd %s && ./run-tempest.sh %s" % (tempest_dir, regexp))

    localhost = Server.LocalServer() #set to the local host
    result = localhost.cmd(cmd)
    if result.exit_code == 0:
        return result
    else:
        raise exceptions.AssertionError("Some of the Tempest tests failed,"
                                        " system is not functional")


