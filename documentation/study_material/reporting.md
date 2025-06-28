# Reporting Tips

- Re-read the bounty program rules
- Steps to reproduce
  - Use plain-text where possible
    - Easy copy+paste = faster verification by provider
    - Screenshot if necessary for formatting/demo
- Example - Vulnerability accessing other customer's data:
  - Indicate you only accessed your own test data, not other real customers
  - Provide the IAM policies used in test setup
  - For steps to reproduce use
    - Cloud-native CLI tools that developers understand
    - Alternatively curl
    - Alternatively the raw HTTP request manipulated in Burp Suite proxy
  - Include samples of proof of the working exploit
