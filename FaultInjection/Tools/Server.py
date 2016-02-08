__author__ = 'yichengwang'

import paramiko
import logging
import subprocess
import socket
import FaultInjection.Tools.Common as Common

LOG = logging.getLogger(__name__)

def create_servers(configs):
    servers = []
    for config in configs:
        servers.append(Server(**config))
    return servers

class ServerException(Exception):
    """Raised when there was a problem executing an SSH command on a server.
    """
    def __init__(self, command, message=None, **kwargs):
        new_msg = str(command)
        if message:
            new_msg += message
        super(ServerException, self).__init__(new_msg, **kwargs)


class LocalServer(object):
    name = 'localhost'

    def cmd(self, command, ignore_failures=False, log_cmd=True,
            log_output=True, collect_stdout=True, **kwargs):
        """Execute shell command on localhost.
        Wrapper around subprocess' `Popen` and `communicate` for logging and
        clarity. It should have more or less the same options as when using
        `Server.cmd`.
        :param command: any shell command
        :param ignore_failures: if True, return CommandResult which will
            contain the exit code; if False, raise ServerException
        :param log_cmd: log info message with format "[localhost] command"
        :param log_output: if there is some output, log info message with
            format "[localhost stdout] the_output" and
            "[localhost stderr] the_error_output"
        :param collect_stdout: if True, the stdout of the command will be saved
            into a string in the returned result (and logged if log_output is
            enabled). If False, it will get printed directly on stdout in
            real-time and not logged or returned.
        :param kwargs: append to `subprocess.Popen`
        :raises: ServerException if ignore_failures is False and the command
            returns a non-zero value
        :returns: `CommandResult`
        """
        if log_cmd:
            LOG.info("[%s] %s", self.name, command)

        if collect_stdout:
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, **kwargs)
        else:
            p = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE,
                                 *kwargs)
        stdout, stderr = p.communicate()
        result = CommandResult(self.name, command)
        result.parse_subprocess_results(stdout, stderr, p.returncode)
        if log_output and result.out:
            LOG.info("[%s stdout] %s", self.name, result.out)
        if log_output and result.err:
            LOG.info("[%s stderr] %s", self.name, result.err)
        if result.exit_code != 0 and not ignore_failures:
            raise ServerException(result)
        return result

    def file_exists(self, filename):
        if self.cmd("[ -f %s ]" % filename,
                    ignore_failures=True, log_cmd=False).exit_code == 0:
            return True
        else:
            return False

class Server(LocalServer):

    def __init__(self, hostname=None, ip=None, username="root", password=None,
                 roles=None, extra_disks=None, **kwargs):
        if not (hostname or ip):
            raise Exception("Either hostname or IP address required")
        self.hostname = hostname
        if not ip:
            self.ip = socket.gethostbyname(self.hostname)
        else:
            self.ip = ip
        self.name = self._decide_on_name()
        self.roles = roles or set()
        self.disks = extra_disks
        if "root_password" in kwargs and not password:
            username = "root"
            password = kwargs["root_password"]
        self._username = username
        self._password = password

        self._ssh = SSH(self.name)
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.load_system_host_keys()
        self.connect()

class SSH(paramiko.SSHClient):
    """Wrapper around paramiko for better error handling and logging.
    Do not create it directly - it is used by the `Server` object.
    """
    def __init__(self, name):
        super(SSH, self).__init__()
        self.name = name

    def __call__(self, command, ignore_failures,
                 log_cmd, log_output, **kwargs):
        """Similar to exec_command, but checks for errors.
        If an error occurs, it logs the command, stdout and stderr.
        :param command: any bash command
        :param ignore_failures: don't raise an exception if an error occurs
        :param log_output: always log output, both stdout and stderr
        :param log_cmd: log the command and the name of server where it is run
        :raises: ServerException
        """
        if log_cmd:
            LOG.info("[%s] %s", self.name, command)
        _, stdout, stderr = self.exec_command(command, **kwargs)
        result = CommandResult(self.name, command)
        result.parse_paramiko_results(stdout, stderr)

        if log_output and result.out:
            LOG.info("[%s stdout] %s", self.name, result.out)
        if log_output and result.err:
            LOG.info("[%s stderr] %s", self.name, result.err)
        if result.exit_code != 0 and not ignore_failures:
            raise ServerException(result)
        return result

class CommandResult(object):
    """Wrapper around SSH command result, for easier usage of `Server.cmd()`
    """
    def __init__(self, server_name, command):
        self._server_name = server_name
        self._out = []
        self._err = []
        self._exit_code = None
        self._command = command

    def parse_paramiko_results(self, stdout, stderr):
        self._exit_code = stdout.channel.recv_exit_status()
        self._out = [line.strip('\n') for line in stdout.readlines()]
        self._err = [line.strip('\n') for line in stderr.readlines()]

    def parse_subprocess_results(self, stdout, stderr, exit_code):
        self._exit_code = exit_code
        if stdout:
            self._out = stdout.strip().split('\n')
        if stderr:
            self._err = stderr.strip().split('\n')

    @property
    def out(self):
        return self._out

    @property
    def err(self):
        return self._err

    @property
    def exit_code(self):
        return self._exit_code

    def __repr__(self):
        return ("[%s] %s\nstdout: %s\nstderr: %s\nexit code: %d"
                % (self._server_name, self._command,
                   self.out, self.err, self.exit_code))

    def __str__(self):
        return ("[%s] %s\nstdout: %s\nstderr: %s\nexit code: %d"
                % (self._server_name, self._command,
                   '\n'.join(self.out), '\n'.join(self.err), self.exit_code))