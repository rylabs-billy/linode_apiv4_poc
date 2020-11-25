#!/bin/bash
#
# sudo apt install jq -y

# create linode and check status
create_linode () {
  linode_id=$(curl -sH "Content-Type: application/json" \
      -H "Authorization: Bearer $TOKEN" \
      -X POST -d '{
        "backups_enabled": true,
        "swap_size": 512,
        "image": "linode/debian9",
        "root_pass": "aComplexP@ssword",
        "authorized_keys": [
          "SSH_KEY"
        ],
        "booted": true,
        "label": "shell_example",
        "type": "g6-nanode-1",
        "region": "ap-southeast"
      }' \
      https://api.linode.com/v4/linode/instances | jq -r .id)

  while true; do
    linode_status=$(curl -sH "Authorization: Bearer $TOKEN" https://api.linode.com/v4/linode/instances/$linode_id | jq -r .status)
    sleep 1
    if [[ $linode_status == "running" ]]; then
      break
    fi
  done

  echo "Linode is $linode_status."
}

# resize disk and check status
resize_disk () {
  disk_id=$(curl -sH "Authorization: Bearer $TOKEN" https://api.linode.com/v4/linode/instances/$linode_id/disks/ | jq -r .data[0].id)

  curl -sH "Content-Type: application/json" \
      -H "Authorization: Bearer $TOKEN" \
      -X POST -d '{
        "size": 15000
      }' \
      https://api.linode.com/v4/linode/instances/$linode_id/disks/$disk_id/resize

  while true; do
    disk_status=$(curl -sH "Authorization: Bearer $TOKEN" https://api.linode.com/v4/linode/instances/$linode_id/disks/$disk_id | jq -r .status)
    sleep 1
    if [[ $disk_status == "ready" ]]; then
      break
    fi
  done

  echo "Disk is $disk_status."
}

# main
create_linode
sleep 10
resize_disk
