#!/usr/bin/env python3
#
# pip3 install linode_api4

import time
from linode_api4 import LinodeClient, Disk

# create linode and check status
def create_linode():
    client = LinodeClient(TOKEN)

    new_linode = client.linode.instance_create('g6-nanode-1',
                                               'ap-southeast',
                                                image='linode/debian9',
                                                authorized_keys=SSH_KEY,
                                                root_pass='aComplexP@ssword',
                                                label='python_example',
                                                booted=True)
                                                   
    status = None
    while status != 'running':
        status = new_linode.status
        time.sleep(1)

    print(f'Linode is {status}.')
    return new_linode, client

# resize disk and check status
def resize_linode(new_linode, client):
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

def main():
    linode, client = create_linode()
    time.sleep(10)
    resize_linode(linode, client)

# main
if __name__ == '__main__':
    main()



