### 🎣 Spear Phishing
A highly targeted social engineering campaign leveraging tailored reconnaissance to deceive a specific high-value individual into compromising network security.

* **OSINT Reconnaissance:** Threat actors utilize Open-Source Intelligence (LinkedIn, corporate directories, social media) to identify organizational hierarchies and single out individuals with privileged access (e.g., Finance or IT admins).
* **Pretexting & Spoofing:** Attackers craft a culturally and contextually accurate scenario (pretext), often spoofing the sender's email address or domain to impersonate a trusted vendor or C-suite executive.
* **Weaponized Payload:** The email contains a malicious link directing the target to a pixel-perfect credential harvesting portal, or a weaponized macro embedded within a standard business document.
* **Initial Access:** Once the target inputs their credentials or executes the macro, the attacker captures the authentication token or drops a lightweight trojan onto the endpoint.
* **Defense Evasion:** The attacker immediately uses the legitimate (but compromised) credentials to log in, bypassing traditional perimeter firewalls since the traffic appears as authorized user activity.
