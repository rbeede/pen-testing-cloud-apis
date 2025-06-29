# OpenStack Lab Client Setup

_Server setup found in the [server setup section](../server_setup/)_


## Setup environment variable
```shell
export LAB_OPENSTACK_IP=127.0.0.1
```

##### Alternative workshop backup server
`#	export LAB_OPENSTACK_IP=203.0.113.10`

## Setup a directory to create files and work out of
```shell
mkdir -p OpenStack
cd OpenStack
```

## Verify Connectivity

```shell
ping -c 2 $LAB_OPENSTACK_IP

```

```shell
curl --insecure --include https://${LAB_OPENSTACK_IP}:8888/healthcheck
```

You should get back a response indicating the service is responding.

---

## Setup the official OpenStack Swift CLI tool

_Distro specific method_
`sudo apt install python3-swiftclient`

##### Optional venv
```shell
sudo apt-get install python3-venv python3-pip

python3 -m venv venv

pip install python-swiftclient
```

##### You might have to add the installed binary directory to your path
```shell
export PATH=$PATH:$HOME/.local/bin
```

## Validate the CLI can reach the simulator server

```shell
swift --insecure --auth=https://${LAB_OPENSTACK_IP}:8888/auth/v1.0 -U system:root -K testpass --verbose stat
```
## Burp Setup commands

```shell
export https_proxy=http://localhost:8080
```

[Alternative CA cert method](Burp_linux.md)

##### Repeat test command with Burp HTTP proxy in-place
```shell
swift --insecure --auth=https://${LAB_OPENSTACK_IP}:8888/auth/v1.0 -U system:root -K testpass --verbose stat
```


## Verify file uploads work

```shell
echo $USER > sample_object.txt

swift --insecure -A https://${LAB_OPENSTACK_IP}:8888/auth/v1.0 -U system:root -K testpass upload bsides-workshop sample_object.txt

swift --insecure -A https://${LAB_OPENSTACK_IP}:8888/auth/v1.0 -U system:root -K testpass list
```

## Prepare sample data for XSS exercise

```shell
echo $USER > sample_object.txt

swift --insecure -A https://${LAB_OPENSTACK_IP}:8888/auth/v1.0 -U system:root -K testpass upload fileuploads ./sample_object.txt
```
