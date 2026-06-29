### 🏗️ IT System Impact: Phishing Infiltration
The primary technical goal is to prevent lateral movement. A compromised identity is actively navigating the network, and IT must sever their access without disrupting legitimate business workflows.

**Recovery Timelines & Technical Impact by Decision:**
* **Immediate Enterprise-Wide Password Reset:** (RTO: 6 Hours) Extremely disruptive to productivity. Instantly terminates the hacker's access but locks out thousands of remote workers and service accounts.
* **Targeted Quarantine & EDR Deployment:** (RTO: 2 Hours) Isolates the specific compromised machine and user account while deploying Endpoint Detection and Response tools to track lateral movement. Low business disruption.
* **Silent Monitoring (Honeypot):** (RTO: 72 Hours) Leaves the compromised account active but routes them into a fake, monitored environment to study their tactics. High risk if they escape the sandbox.
* **Do Nothing:** (RTO: Indefinite) Assuming the threat is minor; the hacker will inevitably escalate privileges.
