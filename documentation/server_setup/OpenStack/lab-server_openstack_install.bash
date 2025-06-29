# A self-contained Swift deployment with some preset credentials for the lab. Assumes Ubuntu/Debian package manager apt.

# SAIO documentation was very out of date and assumed dev work on swift itself
# Modified build with Ubuntu 24.04 LTS Server 64-bit
#	http://greenstack.die.upm.es/2015/06/02/openstack-essentials-part-2-installing-swift-on-ubuntu/
#

# docker options existed but did not make it easy to modify with a "vuln" API

set -x
set -e


if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root."
    exit 1
fi


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )


apt-get update

apt-get -y install swift-proxy
apt-get -y install  swift-account swift-container swift-object

apt-get -y install swift

mkdir -p /var/run/swift
chown swift:swift /var/run/swift

mkdir -p /srv/node/vda1
# while NOT mounted, these perms ensure openstack swift only works when successfully started later
chown root:root /srv/node/vda1
chmod 0000 /srv/node/vda1

cd /etc/swift/

openssl req -x509 -newkey rsa:4096 -nodes -out cert.crt -keyout cert.key -days 3653 -subj "/CN=lab.openstack.swift.cloud.localtest.me"

mkdir -p /var/cache/swift && chown swift:swift /var/cache/swift
apt-get -y install memcached

swift-ring-builder account.builder create 7 1 1
swift-ring-builder container.builder create 7 1 1
swift-ring-builder object.builder create 7 1 1
export ZONE=1
export STORAGE_LOCAL_NET_IP=127.0.0.1
export WEIGHT=100
export DEVICE=vda1
swift-ring-builder account.builder add z$ZONE-$STORAGE_LOCAL_NET_IP:6002/$DEVICE $WEIGHT
swift-ring-builder container.builder add z$ZONE-$STORAGE_LOCAL_NET_IP:6001/$DEVICE $WEIGHT
swift-ring-builder object.builder add z$ZONE-$STORAGE_LOCAL_NET_IP:6000/$DEVICE $WEIGHT
swift-ring-builder account.builder
swift-ring-builder container.builder
swift-ring-builder object.builder

swift-ring-builder account.builder rebalance
swift-ring-builder container.builder rebalance
swift-ring-builder object.builder rebalance


truncate -s 5G /srv/swift-disk
mkfs.xfs /srv/swift-disk

echo "" >> /etc/fstab
echo "/srv/swift-disk	/srv/node/vda1	xfs	loop,noatime	0	0" >> /etc/fstab

mount -a

# WHILE mounted
chown swift:swift /srv/node/vda1




swift-init all stop     || true

#########
#########
## From the repo dir #openstack-demo/etc_swift-confs/# install into /etc/swift/ all the conf files
#########

cp --recursive --verbose --force $SCRIPT_DIR/openstack-demo/etc_swift-confs/* /etc/swift/

chown --recursive root:swift /etc/swift/

chmod u=rw,g=r,o= /etc/swift/*.conf

#########



swift-init all start     || true


echo OpenStack Swift service installed and started, you may need to prepopulate test data
