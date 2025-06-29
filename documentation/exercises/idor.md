# IDOR / Confused Deputy

## Google Cloud via CAZT

Following the challenge at:
https://github.com/Coalfire-Research/cazt/blob/main/documentation/lab_manual/scenarios/02-cross_tenant.md

The end goal is to call the GetMoggy API from the attacker's ` --account=cazt_scen2_cross-tenant@123456789012` to get the resource that belongs to the victim in account 000000002222. A response that looks like:
```
{
  "ActivityLogObjectStorage": "moggylitterbox-000000002222",
  "CreatedAt": 1751213493,
  "Description": null,
  "Name": "NotMyMoggy"
}
```

### Tips:

- Identify which input(s) you want to attack to exploit
- Note: You are attacking the authorization, not the authentication
- How can an input be manipulated to fool a service into accessing the wrong thing?
