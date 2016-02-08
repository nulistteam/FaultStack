__author__ = 'yichengwang'

import logging
import exceptions
import FaultInjection.Tools.Common as Common
import FaultInjection.Tools.Server as server_tools

LOG = logging.getLogger(__name__)

def run(include=None, exclude=None, test_type=None, test_dir="api",
        regexp=None, concurrency=4):

    if exclude:
        raise NotImplementedError("The `exclude` param is not implemented")
    tempest_dir = Common.CONFIG.get("tempest", None) #get the file position of tempest
    if not tempest_dir:
        raise Exception("Tempest directory not provided in config")

    if not regexp:
        regexp = "(^tempest\.%s\.%s.*%s.*)" % (test_dir, include, test_type)
    cmd = ("cd %s && tox -eall '%s' --"
           " --concurrency=%s" % (tempest_dir, regexp, concurrency))

    localhost = server_tools.LocalServer() #set to the local host
    result = localhost.cmd(cmd, ignore_failures=True)
    if result.exit_code == 0:
        return result
    else:
        raise exceptions.AssertionError("Some of the Tempest tests failed,"
                                        " system is not functional")


