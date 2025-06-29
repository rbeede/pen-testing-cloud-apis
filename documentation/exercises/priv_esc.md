# Privilege Escalation

## Google Cloud via CAZT

Following the challenge at:
https://github.com/Coalfire-Research/cazt/blob/main/documentation/lab_manual/scenarios/07-impersonation.md

The end goal is to get a response that looks like:

```json
{
  "Message": "123456789012 using impersonation arn:cloud:iam:us-texas-9:123456789012:FullAdmin"
}
```

### Tips:

- Based on the IAM policy can you get a baseline QA response by making an expected legitimate request with expected inputs?
- Identify which input(s) you want to attack to exploit privilege escalation
- Note: You are attacking the authorization, not the authentication
