### 🕵️ Technical SOC Briefing: Mass Customer PII & Card Exfiltration
Advanced Persistent Threat (APT) actors established covert exfiltration channels, siphoning 1.5 million customer Personally Identifiable Information (PII) records and encrypted credit card tokens to offshore servers. The SOC must prevent catastrophic data leakage while managing prolonged outages.

**Containment Strategies & Operational Assessment:**
* **Option 1: Database Subnet Isolation & Global Credential Revocation**  
  *Complexity: High &bull; Projected Downtime: Extended (RTO: 36h) &bull; Mitigation Likelihood: High / Guaranteed*  
  Disconnects all external database routing, revokes cluster service accounts, and isolates storage tiers. Causes severe transactional disruption, but delivers a high likelihood of terminating active exfiltration tunnels immediately.
* **Option 2: Targeted Egress Firewalling & Service Principal Reset**  
  *Complexity: Moderate &bull; Projected Downtime: Moderate (RTO: 8h) &bull; Mitigation Likelihood: Moderate / Contingent*  
  Enforces strict outbound firewall rules on known Command and Control (C2) ports and resets compromised service keys. Moderate disruption with moderate mitigation odds: encrypted proxy tunnels and alternative egress ports may bypass restrictions.
* **Option 3: Live In-Place Hotpatching & Dynamic Token Rotation**  
  *Complexity: Low &bull; Projected Downtime: None (Zero Downtime) &bull; Mitigation Likelihood: Low / Uncertain*  
  Rotates database credentials on running nodes without interrupting customer transactions. Zero operational disruption, but low likelihood of containment: active memory-resident attacker tools continue siphoning records unimpeded.
