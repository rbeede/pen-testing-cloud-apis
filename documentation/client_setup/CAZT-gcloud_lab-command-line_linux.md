# Prerequisites

- Python3 installed
- gcloud CLI installed (https://cloud.google.com/sdk/docs/install#linux)
  - Also the `gcloud` command must be available in the system path
- Note that download and install of gcloud can be slow
- You may want the .tar.gz version instead (https://cloud.google.com/sdk/docs/install#linux)
- Use of the docker image can result in sandboxing making it more difficult to attach Burp

Assumes you already downloaded
- `git clone https://github.com/Coalfire-Research/cazt.git`
  - Alt: `curl -O https://github.com/Coalfire-Research/cazt/archive/refs/heads/main.zip`

## Establish service address

Change to workshop IP address if you can't get it to run locally:
```shell
export LAB_IP=127.0.0.1

ping $LAB_IP
```

## Add Python dependencies (some platforms)

#### Ubuntu

```shell
sudo apt install -y python3-venv
```

---

# Burp Setup

[See Burp Doc](Burp_linux.md)

---

# Add CAZT simulation API into the gcloud-cli

```shell
python3 -m venv venv

source venv/bin/activate

pushd cazt/trainee/cloud-clients/gcloud/

pwd

python3 install-cazt-into-gcloud-cli.py

deactivate

popd

pwd
```

Validate with
```shell
gcloud cazt --help
```

---

# Start the simulator server

1. Open a new tab (and keep it open)
   - Burp env variables should _not_ be configured
1. Use the following instructions
   - _Based on the main project https://github.com/Coalfire-Research/cazt_

```shell
cd cazt/

python3 -m venv venv

source venv/bin/activate

pip3 install -r requirements.txt

# It is normal if this is currently empty, for future use
```

```shell
cd simulator/

bash x509/generate-self-signed.bash

ip address show

python3 main_http_endpoint_server.py
```

---

# Populate Sample Test Data

```shell
gcloud cazt create \
    --api-endpoint-overrides=https://$LAB_IP:8443/uat \
    --account=cazt_scen0_Setup-Any@000000001111 \
    --format json \
    --name=MyMoggy \
    --activity-log-object-storage=moggylitterbox-000000001111
```

```shell
gcloud cazt create \
    --api-endpoint-overrides=https://$LAB_IP:8443/uat \
    --account=cazt_scen0_Setup-Any@123456789012  \
    --format json \
    --name=NotMyMoggy \
    --activity-log-object-storage=moggylitterbox-123456789012 
```

```shell
gcloud cazt run-activity \
    --api-endpoint-overrides=https://$LAB_IP:8443/uat \
	--account=cazt_scen0_Setup-Any@000000001111 \
	--format json \
	--arn=arn:cloud:cazt:us-texas-9:000000001111:MyMoggy
```

You now have two tenants (customers) accounts with sample data in them:
- Account 000000001111 with MyMoggy
- Account 123456789012 with NotMyMoggy
