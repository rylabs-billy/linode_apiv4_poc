# Linode APIv4 PoC

Python and shell script examples to demonstrate checking for the `status` in API responses. Instances can return [responses](https://www.linode.com/docs/api/linode-instances/#linode-create__responses) with a status of:
- `running`
- `offline`
- `booting`
- `rebooting`
- `shutting_down`
- `provisioning`
- `deleting`
- `migrating`
- `rebuilding`
- `cloning`
- `restoring`
- `stopped`

Disk updates can return [responses](https://www.linode.com/docs/api/linode-instances/#disk-update__responses) with a status of:
- `ready`
- `not ready`
- `deleting`

## Requirements
These examples use `jq` for filtering JSON, and the offical [python library](https://github.com/Linode/linode_api4-python) for the Linode APIv4.
```
apt install jq -y
pip3 install linode_api4
```

## Documentation
- [Linode API](https://www.linode.com/docs/api/)
- [linode_api4](https://linode-api4.readthedocs.io/en/latest/index.html)
