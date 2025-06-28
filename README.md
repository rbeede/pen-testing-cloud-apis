# Pen-testing Cloud APIs: Workshop

An updated collection of resources used for a workshop on penetration testing of cloud APIs. This version consolidates multiple cloud technologies into a training workshop for application security penetration testing of multiple clouds.

##### Major Updates
- Dropped support for Windows Powershell/CMD
  - Linux is simply much faster for setup during a workshop
- More prominent examples of using the gcloud clients for API pen testing
- Updated deployment tools and instructions to allow each workshop trainee to run everything locally

#### What's Covered
- Hacking a simulated vulnerable Google Cloud REST API
- Hacking a simulated vulnerable OpenStack Swift API
  - Including how to use the vulnerability to attack web GUIs
- Hacking a simulated vulnerable Salesforce Cloud App

##### Not Covered
- Azure - work-in-progress 📋
- AWS - Does not have a public bug bounty reward program
  - https://aws.amazon.com/security/vulnerability-reporting/
  - HackerOne for Amazon (retail)
    - https://hackerone.com/amazonvrp
	- > All AWS related services and products will be out-of-scope

## Workshop Structure
1. [Study Material](documentation/study_material/README.md)
  - Highlevel summary of concepts important for pen testing APIs
  - More detailed explanations and examples for each high-level objective
1. [Server Simulator Setup](documentation/server_setup/)
  - Technical steps for setup of the emulated cloud-service (server) components
  - Permits take-home testing outside of the workshop material as well as reducing dependency on a working workshop conference Internet connection
1. [Client-side Setup](documentation/client_setup/)
  - Important details on required software for the pen tester
  - Lesson material for how to get working cloud REST API calls into pen testing tools
1. [Exercises](documentation/exercises/README.md)
  - Privilege Escalation
  - IDOR/Confused Deputy to steal another tenant's (customer's) data
  - Leveraging XSS via an API
  - Bypass field encryption using injection vulnerabilities to access restricted data
  
## Where to Start
1. Setup the server simulator infrastructure
1. Setup your local pen testing client software
1. Begin in the [Exercises] section

---

##### Previous Work
- [PaaS Cloud Goat (Hacking Salesforce Apps)](https://github.com/rbeede/paas-cloud-goat)
  - https://defcon.org/html/defcon-32/dc-32-workshops.html#54228
- [Cloud AuthoriZation Trainer](https://github.com/rbeede/cazt)
  - https://www.blackhat.com/us-23/arsenal/schedule/#cloud-authz-trainer-cazt-33486
- [OpenStack API Hacking](https://github.com/rbeede/BSidesSATX2023)

##### Author Bio
- https://www.rodneybeede.com/curriculum%20vitae/bio.html

Workshop was publicly released for Def Con 33 Workshops - August 2025