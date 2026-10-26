### 🔗 Technical SOC Briefing: Supply Chain Logistics API Poisoning
Adversaries compromised third-party software updates and logistics vendor API keys, using trusted downstream connections to inject malicious payloads into corporate commerce systems.

**Containment Strategies & Operational Assessment:**
* **Option 1: Sever Supplier Feeds & Root Certificate Revocation**  
  *Complexity: High &bull; Projected Downtime: Extended (RTO: 48h) &bull; Mitigation Likelihood: High / Guaranteed*  
  Disconnects all external vendor and supplier integration pipelines and rotates root cryptographic certificates. Halts downstream shipping fulfillment, but provides a high likelihood of completely purging untrusted vendor injection vectors.
* **Option 2: Edge CDN Scrubbing & Rate Limiting**  
  *Complexity: Moderate &bull; Projected Downtime: Moderate (RTO: 10h) &bull; Mitigation Likelihood: Moderate / Contingent*  
  Re-routes external partner traffic through edge filtering inspection with strict behavioral limits. Moderate transaction slowdowns with moderate mitigation odds: compromised legitimate credentials may still pass behavioral filters.
* **Option 3: Maintain Partner Traffic & Rely on Vendor Warranties**  
  *Complexity: Low &bull; Projected Downtime: None (Zero Downtime) &bull; Mitigation Likelihood: Low / Uncertain*  
  Avoids penalizing supplier relationships by accepting external vendor self-attestation reports. Zero operational disruption, but low likelihood of containment: leaves known compromised partner routes connected.
