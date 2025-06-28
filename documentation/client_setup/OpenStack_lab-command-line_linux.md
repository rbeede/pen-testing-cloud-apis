# Assumes Linux


export LAB_OPENSTACK_IP=203.0.113.10


ping -c 2 $LAB_OPENSTACK_IP

mkdir -p OpenStack
cd OpenStack



curl --insecure --include https://${LAB_OPENSTACK_IP}:8080/healthcheck



pip install python-swiftclient
sudo apt  install python3-swiftclient


# You might have to add the installed binary directory to your path
export PATH=$PATH:$HOME/.local/bin


swift --insecure --auth=https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U system:root -K testpass --verbose stat



# Burp Setup commands

export https_proxy=http://localhost:8080


# repeat test command
swift --insecure --auth=https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U system:root -K testpass --verbose stat


# Another test command

echo $USER > sample_object.txt



swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U system:root -K testpass upload bsides-workshop sample_object.txt


swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U system:root -K testpass list





# XSS testing

echo $USER > sample_object.txt



swift --insecure -A https://${LAB_OPENSTACK_IP}:8080/auth/v1.0 -U system:root -K testpass upload fileuploads ./sample_object.txt


# now pwn it