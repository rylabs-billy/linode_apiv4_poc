#!/usr/bin/env python3
'''
Demontrates deploying a linode with the python apiv4 library.
Standard images fill the allocable disk space by default. Private
images deploy at exact size, so an extra disk resize is needed to
fill the allocable space for the plan type.
'''

import time, os, sys, dotenv
from linode_api4 import LinodeClient, Disk

# load environment variabls
dotenv.load_dotenv()
TOKEN = os.environ.get('token')
ROOT_PASS = os.environ.get('root_pass')
SSH_KEY = os.environ.get('ssh_key')
IMAGE = os.environ.get('image')

def create_linode():
    '''Deploy a Linode instance'''
    client = LinodeClient(TOKEN)

    # set boot and status parameters based on whether the image is standard or private
    if 'private' in IMAGE:
        print(f'Deploying private image: {IMAGE}\n')
        boot = False
        wait_status = 'offline'
        resize = True
    else:
        print(f'Deploying standard image: {IMAGE}\n')
        boot = True
        wait_status = 'running'
        resize = False

    # spawn instance    
    instance = client.linode.instance_create('g6-standard-4',
                                             'us-east',
                                             image=IMAGE,
                                             authorized_keys=SSH_KEY,
                                             root_pass=ROOT_PASS,
                                             label=sys.argv[1],
                                             swap_size=512,
                                             booted=boot,
                                             tags=["example"])
                                
    # let user know when instance is ready
    print("Waiting for instance to become available.", end="", flush=True)
    while instance.status != wait_status:
        time.sleep(1)
        print(".", end="", flush=True)
    print()

    # resize the disk before rebooting (only if using private image)
    if resize == True:
        resize_disk(client, instance)
        
        # boot the linode after resizing
        boot_linode(instance) 

    return instance

def resize_disk(client, instance):
    '''Resize the Linode's boot disk to remaining allocable space'''
    disk_id = str(instance.disks[0]).split()[1]
    disk_size = instance.specs.disk - 512
    
    linode_disk = Disk(client, disk_id, parent_id=instance.id, json=None)
    
    # make sure disk is ready
    print("waiting for disks.", end="", flush=True)
    while linode_disk.status != 'ready':
            time.sleep(1)
            print(".", end="", flush=True)
    print()

    # resize disk when ready   
    linode_disk.resize(disk_size)
    print("resizing disks.", end="", flush=True)
    while linode_disk.status != 'ready':
        time.sleep(1)
        print(".", end="", flush=True)
    print()

def boot_linode(instance):
    '''Boot the Linode'''
    instance.boot()

    print("booting.", end="", flush=True)
    while instance.status != 'running':
        time.sleep(1)
        print(".", end="", flush=True)
    print()  
        
#    print(f"""
#    linode {instance.id} created successfully! ssh should become available
#    shortly at root@{instance.ipv4[0]}""")

def main():
    linode = create_linode()
    print(f"""
    linode {linode.id} created successfully! ssh should become available
    shortly at root@{linode.ipv4[0]}""")

# main
if __name__ == '__main__':
    main()



