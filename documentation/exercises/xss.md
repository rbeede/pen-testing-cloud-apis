# Cross-site Scripting (XSS)

## OpenStack

Ensure that all setup per [](../client_setup/OpenStack_lab-command-line_linux.md) is complete.

The end goal is to get successful XSS in a web browser.
![image](https://github.com/user-attachments/assets/8e1da94d-23ee-4266-9c84-49a7a803057f)

## URL of frontend:

`http://${LAB_OPENSTACK_IP}:9080/REST/API/endpoint.cgi`

## Tips:

- If a front-end UI denies uploads where might it miss?
- https://docs.openstack.org/ocata/cli-reference/swift.html
- Remember: Object Storage != Filesystem Storage nor the same limitations
  - https://docs.openstack.org/api-ref/object-store/index.html#objects
