### 💀 Technical SOC Briefing: Double Extortion Ransomware Lockout
Adversary deployed high-speed encryption across active directory domain controllers and exfiltrated sensitive files to dark web leak sites, demanding a $5M extortion payment.

**Containment Strategies & Technical Impact Analysis:**
* **Option 1: Burn and Rebuild Bare-Metal from Clean Offline Golden Images**  
  *Recovery Time Objective (RTO): 36 Hours Offline &bull; Threat Mitigation: 90% (Maximum)*  
  Completely wipes encrypted bare-metal servers and restores systems from isolated offline golden backups. Severe disruption (-4 Health penalty), but guarantees complete eradication of ransomware binaries and attacker persistence.
* **Option 2: Emergency Network Partition & Decryption Sandbox**  
  *Recovery Time Objective (RTO): 8 Hours Offline &bull; Threat Mitigation: 60% (Balanced)*  
  Partitions compromised subnet zones and attempts sandbox decryption of affected partitions. Moderate disruption (-2 Health penalty). Encrypted secondary controllers may remain locked.
* **Option 3: Keep Production Online & Pursue Back-Channel Key Negotiation**  
  *Recovery Time Objective (RTO): 0 Hours &bull; Threat Mitigation: 25% (Permissive)*  
  Keeps remaining infrastructure online and opens secretive ransom negotiation channels. Zero operational disruption (0 Health penalty), but high risk: cybercriminals frequently fail to supply functioning decrypters.
