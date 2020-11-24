#!/usr/bin/env python3
#
# pip install linode_api4

import time
from linode_api4 import LinodeClient, Disk

# create linode and check status
client = LinodeClient(TOKEN)

new_linode = client.linode.instance_create('g6-nanode-1',
                                                     'ap-southeast',
                                                     image='linode/debian9',
                                                     authorized_keys=SSH_KEY,
                                                     root_pass='aComplexP@ssword',
                                                     label='api_python_test4',
                                                     booted=True)
                                                   
status = None
while status != 'running':
    status = new_linode.status
    time.sleep(1)

print(f'Linode is {status}.')
time.sleep(10)

# check status of disk operations, such as when resizing
linode_id = new_linode.id
disks = [str(i).split()[1] for i in new_linode.disks]
disk_id = disks[0]

linode_disk = Disk(client, disk_id, parent_id=linode_id, json=None)

status = None
if linode_disk.resize(15000) == True:
    while status != 'ready':
        status = linode_disk.status
        time.sleep(1)

print(f'Disk is {status}.')



