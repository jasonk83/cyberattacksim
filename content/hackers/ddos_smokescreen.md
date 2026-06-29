### 🌊 Distributed Denial of Service (DDoS) as a Smokescreen
Overwhelming a target's network perimeter with a massive flood of volumetric traffic, strategically utilized as a diversionary tactic to exhaust Incident Response resources while a secondary, stealthy breach occurs.

* **Botnet Mobilization:** The attacker commands a distributed network of compromised IoT devices or hijacked servers to simultaneously route traffic toward the target's external IP addresses.
* **Resource Exhaustion:** Volumetric attacks (e.g., UDP floods) or protocol attacks (e.g., SYN floods) overwhelm the target's edge routers, load balancers, and Web Application Firewalls (WAF).
* **Alert Fatigue:** The target's Security Operations Center (SOC) dashboard lights up with critical availability alerts, forcing the entire IT team to aggressively triage the downtime.
* **The True Infiltration:** While IT is completely distracted mitigating the DDoS, the attacker quietly exploits a known vulnerability on an unrelated, unmonitored backend server.
* **Log Obfuscation:** The sheer volume of incoming DDoS traffic makes it incredibly difficult for the SIEM (Security Information and Event Management) system to parse out the subtle, anomalous lateral movement occurring elsewhere on the network.
