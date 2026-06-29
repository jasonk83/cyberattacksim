### 🕵️ IT System Impact: A.P.T. Data Exfiltration
A silent, persistent threat is tunneling data out. IT must sever the egress connections and hunt down every hidden backdoor the APT has established.

**Recovery Timelines & Technical Impact by Decision:**
* **Sever Total Internet Connectivity:** (RTO: 12 Hours) Pulls the plug on the entire organization. Stops exfiltration instantly, but turns the company into a digital island.
* **Implement Strict Egress Port Blocking:** (RTO: 6 Hours) Blocks all non-essential outbound traffic (e.g., forcing everything through port 443). May break external APIs and cloud services.
* **Quietly Route Hacker to a Decoy Server:** (RTO: 48 Hours) Allows the hacker to keep stealing data, but secretly swaps the real database with a server full of fake, traceable information to uncover their identity.
