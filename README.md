# Linode APIv4 PoC

Python and shell script examples of deploying Linodes via the APIv4 from private images and standard (Linode provided) images. With private images, the disk doesn't automatically resize to fill the plan's allocable space, so a manual resize is invoked before booting. In this case, it checks for `status` in API [responses](https://www.linode.com/docs/api/linode-instances/#linode-create__responses) before executing the next steps.

## Requirements
Install `jq` for filtering JSON with the shell script.
```
apt install jq -y
```
Install the [python library](https://github.com/Linode/linode_api4-python) and `python-dotenv` from `requirements.txt`.
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Usage
```
linodedeploy.{py,sh} <linode label>
```

## Documentation
- [Linode API](https://www.linode.com/docs/api/)
- [linode_api4](https://linode-api4.readthedocs.io/en/latest/index.html)
