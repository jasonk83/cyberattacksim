### 💀 Technical SOC Briefing: Double Extortion Ransomware Lockout
Adversary deployed high-speed encryption across active directory domain controllers and exfiltrated sensitive files to dark web leak sites, demanding an extortion payment. Containment must eliminate encryption rootkits without funding criminal syndicates.

**Containment Strategies & Operational Assessment:**
* **Option 1: Burn and Rebuild Bare-Metal from Clean Offline Golden Images**  
  *Complexity: High &bull; Projected Downtime: Extended (RTO: 36h) &bull; Mitigation Likelihood: High / Guaranteed*  
  Completely wipes encrypted bare-metal servers and restores systems from isolated offline golden backups. Severe operational disruption, but delivers a high likelihood of completely eradicating ransomware binaries and attacker persistence.
* **Option 2: Emergency Network Partition & Decryption Sandbox**  
  *Complexity: Moderate &bull; Projected Downtime: Moderate (RTO: 8h) &bull; Mitigation Likelihood: Moderate / Contingent*  
  Partitions compromised subnet zones and attempts sandbox decryption of affected partitions. Moderate operational disruption with moderate mitigation odds: encrypted secondary controllers may remain locked.
* **Option 3: Keep Production Online & Pursue Back-Channel Key Negotiation**  
  *Complexity: Low &bull; Projected Downtime: None (Zero Downtime) &bull; Mitigation Likelihood: Low / Uncertain*  
  Keeps remaining infrastructure online and opens secretive ransom negotiation channels. Zero operational disruption, but low likelihood of containment: cybercriminals frequently fail to supply functioning decrypters and double-extort victims.
