### 🕵️ Technical SOC Briefing: Mass Customer PII & Card Exfiltration
Advanced Persistent Threat (APT) actors established covert exfiltration channels, siphoning 1.5 million customer Personally Identifiable Information (PII) records and encrypted credit card tokens to offshore servers.

**Containment Strategies & Technical Impact Analysis:**
* **Option 1: Database Subnet Isolation & Global Credential Revocation**  
  *Recovery Time Objective (RTO): 36 Hours Offline &bull; Threat Mitigation: 90% (Maximum)*  
  Disconnects all external database routing, revokes cluster service accounts, and isolates storage tiers. Severe disruption (-4 Health penalty), but terminates 90% of active exfiltration tunnels immediately.
* **Option 2: Targeted Egress Firewalling & Service Principal Reset**  
  *Recovery Time Objective (RTO): 8 Hours Offline &bull; Threat Mitigation: 60% (Balanced)*  
  Enforces strict outbound firewall rules on known Command and Control (C2) ports and resets compromised service keys. Moderate disruption (-2 Health penalty). Encrypted proxy tunnels may still bypass port restrictions.
* **Option 3: Live In-Place Hotpatching & Dynamic Token Rotation**  
  *Recovery Time Objective (RTO): 0 Hours &bull; Threat Mitigation: 25% (Permissive)*  
  Rotates database credentials on running nodes without interrupting customer transactions. Zero operational disruption (0 Health penalty), but active memory-resident attacker tools continue siphoning records.
