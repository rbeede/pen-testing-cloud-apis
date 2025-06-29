# OpenStack Swift Simulated Vulnerable Server

Tested on Ubuntu 24.04 x86_64

Pre-setup virtual machine images are available in the repository releases page: https://github.com/rbeede/pen-testing-cloud-apis/releases

---

## Setup Steps

1. Ensure you have approximately 6GiB of free space
1. Ensure your distro has the tools for XFS filesystem support
   - WSL2 by default does not
   - `sudo apt install xfsprogs`
   - `sudo modprobe -v xfs`
1. Clone the workshop repo
1. Go into the `documentation/server_setup/OpenStack/` folder

`sudo bash lab-server_openstack_install.bash`

## Startup Steps

1. Objects will be persisted upon reboot
1. After a reboot login to the server and execute
   - `sudo swift-init all start`
   - It is safe to ignore Unable to find XXX config section messages
   
The simulated web UI should be run on the same server where swift is running and started as follows:
1. Start a `screen` session so the server persists
1. You do _not_ need to be root
1. `cd documentation/server_setup/OpenStack/`
1. `python3 xss_python_swift_rest_api_server.py 9080`

## Reset workshop data

If you need a fresh start you can clear the data with

```shell
swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U system:root -K testpass delete fileuploads

swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U account1:normal -K expected delete deptdocs

swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U account2:somebody -K else delete research 

swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U codeerror:unexpecteduser -K shouldnothappen delete warez
```

## (Re)create workshop test data

If you did a fresh start and want the exercise data to be available:

```shell
# From the workshop repo you cloned
pushd documentation/server_setup/OpenStack/openstack-demo/demo-testdata/
```

```shell

echo $USER > sample_object.txt

swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U system:root -K testpass upload bsides-workshop sample_object.txt


# setup XSS example

swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U system:root -K testpass upload fileuploads .\sample_object.txt

swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U system:root -K testpass upload fileuploads .\sugarskull-2019_orig.png


# setup IAM examples

# Base check that accounts work

swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U account1:normal -K expected list
swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U account2:somebody -K else list
swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U codeerror:unexpecteduser -K shouldnothappen list


# Setup default uploads
swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U account1:normal -K expected upload deptdocs .\sugarskull-2019_orig.png
swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U account1:normal -K expected upload deptdocs .\sample_object.txt

swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U account2:somebody -K else upload research .\super-secret-doc-for-account2-only.txt
swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U account2:somebody -K else upload research ".\initials profile picture - small.png"
swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U account2:somebody -K else upload research ".\fyi emoji.png"

# Hacker account
swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U codeerror:unexpecteduser -K shouldnothappen upload warez .\pumpkin.JPG
```


```shell
popd
```
