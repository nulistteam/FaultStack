__author__ = 'yichengwang'

import logging
import time
import itertools
import socket
from novaclient import client
from novaclient import exceptions

import FaultInjection.Tools.Server as Server
import FaultInjection.Tools.Common as Common

LOG = logging.getLogger(__name__)
SNAPSHOT_TIMEOUT = 5 * 60

def create_snapshots(tag = ""):
    nova = _get_nova_client()
    vms, ssh_servers = _find_vms(nova)

    snapshots = list()
    for vm_id, ssh in zip(vms, ssh_servers):
        vm = nova.servers.get(vm_id)
        snapshot_name = _get_snapshot_name(vm.name, tag)
        s = _find_snapshot(nova, snapshot_name)
        if s:
            LOG.warning("Snapshot '%s' already exist, re-using it"
                        % snapshot_name)
            snapshots.append(s)
        else:
            # let things settle a bit
            time.sleep(3)
            # sync the file system first
            ssh.cmd("sync")
            LOG.info("Creating snapshot '%s'" % snapshot_name)
            s = vm.create_image(snapshot_name)
            snapshots.append(s)

    for snapshot_id in snapshots:
        snapshot = nova.images.get(snapshot_id)


def restore_snapshots(tag=''):
    """Restore snapshots of servers - find them by name."""
    nova = _get_nova_client()
    vms, _ = _find_vms(nova)
    for vm_id in vms:
        vm = nova.servers.get(vm_id)
        snapshot_name = _get_snapshot_name(vm.name, tag)
        s = nova.images.find(name=snapshot_name)
        # use findall and check if there is only one, check if s.server.id is
        # the same as the vm.id, check if status is active
        LOG.info("Rebuilding VM '%s' with image '%s'" % (vm.name, s.name))
        vm.rebuild(s)

    for vm_id in vms:
        vm = nova.servers.get(vm_id)
    # create new ssh connections
    # TODO(mkollaro) wait until ssh works, not just an arbitrary sleep
    time.sleep(3 * 60)

def delete_snapshots(tag=''):
    nova = _get_nova_client()
    vms, _ = _find_vms(nova)
    for vm_id in vms:
        try:
            vm = nova.servers.get(vm_id)
            snapshot_name = _get_snapshot_name(vm.name, tag)
            s = nova.images.find(name=snapshot_name)
            LOG.info("Deleting snapshot '%s'", s.name)
            s.delete()
        except exceptions.NotFound:
            LOG.warning("Could not find snapshot '%s'", s.name)

def _find_snapshot(novaclient, snapshot_name):
    try:
        snapshot = novaclient.images.find(name=snapshot_name)
        return snapshot
    except exceptions.NotFound:
        return None

def _get_nova_client():
    user = Common.CONFIG["management"]["user"]
    tenant = Common.CONFIG["management"]["tenant"]
    auth_url = Common.CONFIG["management"]["auth_url"]
    password = Common.CONFIG["management"]["password"]
    nova = client.Client("1.1", user, password, tenant, auth_url, service_type="compute")
    return nova

def _get_snapshot_name(vm_name, tag):
    basename = Common.CONFIG['management'].get('snapshot_prefix',
                                               'destroystack-snapshot')
    if tag:
        tag = '_' + tag
    name = "%s_%s%s" % (basename, vm_name, tag)
    return name

def _find_vms(novaclient):
    vms = list()
    ssh_servers = list()
    for server in Common.CONFIG["servers"]:
        if "id" in server:
            vm = novaclient.servers.get(server["id"])
        else:
            ip = server.get("ip", None);
            if not ip:
                ip = socket.gethostbyname(server["hostname"])
            vm = _find_vm_by_ip(novaclient, ip)

        if vm is None:
            raise exceptions.NotFound("Couldn't find server:\n %s" % server)
        ssh = Server.Server(**server)
        vms.append(vm)
        ssh_servers.append(ssh)
    return vms,ssh_servers

def _find_vm_by_ip(novaclient, ip):
    all_vms = novaclient.servers.list()
    found = False
    result = None
    for vm in all_vms:
        ip_list = getattr(vm, "networks", dict()).values()
        all_ips = list(itertools.chain.from_iterable(ip_list))
        if ip in all_ips:
            if found is True:
                msg = ("Found two VMs with the IP '%s'. This means it is"
                       " possible for more VMs to have the same IP in your"
                       " setup. To uniquely identify VMs, please provide the"
                       " 'id' field in the configuration for each server")
                raise exceptions.NoUniqueMatch(msg)
            found = True
            result = vm
    return result
