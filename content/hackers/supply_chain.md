### 🔗 Supply Chain Pivot (Integrity)
Weaponizing a target's trusted infrastructure to distribute malicious payloads to the target's external clients, transforming the company into an unwitting distributor of malware.

* **Codebase Compromise:** Hackers infiltrate the company's internal CI/CD (Continuous Integration/Continuous Deployment) pipeline, gaining access to the servers where official software updates are compiled.
* **Malware Injection:** A highly obfuscated trojan is injected into a legitimate software patch or API update right before it is digitally signed by the company's security certificates.
* **Trusted Distribution:** The company unknowingly pushes the compromised update to hundreds or thousands of its B2B clients, who install it blindly because the digital signature validates it as "safe."
* **Exponential Fallout:** The hackers now have backdoor access to the networks of every client that downloaded the update, turning a single breach into a massive, multi-national cyber crisis.
