### 🏗️ Technical SOC Briefing: Spear Phishing & Credential Theft
Targeted spear phishing deceived finance personnel, granting threat actors legitimate session tokens on CloudStore corporate workstations. The immediate technical objective is preventing unauthorized lateral movement without permanently disabling enterprise business functions.

**Containment Strategies & Technical Impact Analysis:**
* **Option 1: Enterprise-Wide Password Reset & Workstation Lockout**  
  *Recovery Time Objective (RTO): 24 Hours Offline &bull; Threat Mitigation: 90% (Maximum)*  
  Revokes all active enterprise Kerberos/OAuth tokens, isolates employee VLANs, and forces hardware MFA (Multi-Factor Authentication) enrollment. Extremely disruptive to operations (-4 Health penalty), but terminates 90% of active intrusion spread immediately.
* **Option 2: Targeted Account Quarantine & EDR Deployment**  
  *Recovery Time Objective (RTO): 6 Hours Offline &bull; Threat Mitigation: 60% (Balanced)*  
  Quarantines only suspect finance accounts while deploying Endpoint Detection & Response (EDR) behavioral monitoring agents across endpoints. Moderate disruption (-2 Health penalty). Threat actors may still pivot if secondary credentials were compromised.
* **Option 3: Silent Honeypot Monitoring & Passive Tap**  
  *Recovery Time Objective (RTO): 0 Hours &bull; Threat Mitigation: 25% (Permissive)*  
  Leaves accounts active and routes suspicious sessions into a deceptive sandbox environment to observe adversary tactics. Zero operational disruption (0 Health penalty), but high risk: attackers frequently escape monitoring to escalate privileges.
