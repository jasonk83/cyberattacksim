"""
game_data.py
Scenario Definitions, Team Passcodes, Phase Timing, and Modular Content
for CloudStore Command: Cyber Attack Simulation
"""

import os
from typing import Dict, Any, List, Optional, Tuple

# Team Passcodes (used by Team Captains to unlock decision & polling controls)
TEAM_CODES = {
    "main": "admin123",       # Game Master / Mission Control
    "hackers": "hacker123",   # Threat Actor Command
    "it": "tech123",          # IT Defense Command
    "exec": "board123",       # Executive Boardroom
    "media": "press123"       # Media & PR Scrum
}

# Phase Timers in Seconds
PHASE_DURATIONS = {
    "hacker": 300,               # 5 Minutes (300s)
    "it": 300,                   # 5 Minutes (300s)
    "exec": 180,                 # 3 Minutes (180s)
    "media": 300,                # 5 Minutes (300s)
    "recap": 120,                # 2 Minutes (120s)
    "final_hacker_action": 180   # 3 Minutes (180s)
}

# Directory path for modular markdown scenario content
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, "content")

def load_markdown_content(role: str, filename: str) -> str:
    """Safely loads educational markdown briefings from the content/ directory."""
    try:
        path = os.path.join(CONTENT_DIR, role, filename)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read().strip()
    except Exception:
        pass
    return ""

# Attack Vectors by Round (All intrusions succeed, damage varies by vector)
ATTACKS = {
    1: {
        "A": {
            "id": "A",
            "name": "Spear Phishing & Credential Harvest",
            "icon": "🎣",
            "damage": -20,
            "description": "Targeted spoofed invoice deceived finance staff. Executive credentials captured.",
            "md_file": "phishing.md",
            "assessment": "Reliable entry point with low initial suspicion, giving access to user accounts."
        },
        "B": {
            "id": "B",
            "name": "Unpatched Web Server CVE Exploit",
            "icon": "🛠️",
            "damage": -25,
            "description": "Automated scanning identified known remote code execution vulnerability on public gateway.",
            "md_file": "zero_day.md",
            "assessment": "Direct system-level foothold giving the attacker access to core application servers."
        },
        "C": {
            "id": "C",
            "name": "AI LLM Prompt Injection & API Pivot",
            "icon": "🤖",
            "damage": -30,
            "description": "Adversarial prompts injected into customer support chatbot to exfiltrate backend system keys.",
            "md_file": "prompt_injection.md",
            "assessment": "Novel and insidious attack that weaponizes automated internal assistants to compromise API layers."
        }
    },
    2: {
        "A": {
            "id": "A",
            "name": "Mass Customer PII & Card Exfiltration",
            "icon": "🕵️",
            "damage": -25,
            "description": "Covert exfiltration of 1.5 million customer transaction records and hashes to bulletproof hosting.",
            "md_file": "apt_exfiltration.md",
            "assessment": "Silent exfiltration designed for dark web monetization and immense regulatory fallout."
        },
        "B": {
            "id": "B",
            "name": "Production Database Sabotage & Deletion",
            "icon": "💥",
            "damage": -28,
            "description": "Attacker deployed malicious drop-table scripts and wiped primary transactional replicas.",
            "md_file": "database_sabotage.md",
            "assessment": "Direct physical/digital destruction aimed at crippling the organization's core operations."
        },
        "C": {
            "id": "C",
            "name": "Double Extortion Ransomware Lockout",
            "icon": "💀",
            "damage": -30,
            "description": "High-speed encryption of active directory domain controllers with $5M ransom note posted.",
            "md_file": "double_extortion.md",
            "assessment": "Total operational blackout coupled with threats of public data leaks if ransom is unpaid."
        }
    },
    3: {
        "A": {
            "id": "A",
            "name": "Supply Chain Logistics API Poisoning",
            "icon": "🔗",
            "damage": -25,
            "description": "Compromised third-party inventory partner API utilized to poison shipping manifests.",
            "md_file": "supply_chain.md",
            "assessment": "Leverages external vendor trust to infect downstream enterprise infrastructure."
        },
        "B": {
            "id": "B",
            "name": "Volumetric DDoS Smokescreen & API Wipe",
            "icon": "🌊",
            "damage": -28,
            "description": "Massive 800 Gbps DDoS attack launched to mask silent cloud IAM permission modifications.",
            "md_file": "ddos_smokescreen.md",
            "assessment": "Overwhelms defense sensors with noise while critical assets are secretly drained."
        },
        "C": {
            "id": "C",
            "name": "APT Deep Persistence & Dark Web Auction",
            "icon": "🏴‍☠️",
            "damage": -30,
            "description": "Advanced persistent threat implants UEFI firmware rootkit and lists corporate IP on dark forums.",
            "md_file": "firmware_persistence.md",
            "assessment": "Maximum reputation devastation and permanent loss of enterprise intellectual property."
        }
    }
}

# IT Defense Containment Options
# Trade-off rule: Less attractive options (heavy downtime & disruption) provide the STRONGEST protection!
IT_CHOICES = {
    1: [
        {
            "id": "1",
            "label": "Full Credential Reset & Workstation Lockout",
            "label_short": "Opt 1 (24h Full Lockout)",
            "downtime": "24 Hours Offline",
            "disruption": "Severe Business Disruption (-4 Health Penalty)",
            "disruption_penalty": -4,
            "mitigation_pct": 0.90,
            "desc": "Revoke all enterprise session tokens, force hardware MFA enrollment, and isolate corporate subnet.",
            "technical_detail": "Stops 90% of hacker lateral spread by immediately terminating compromised active tokens.",
            "exec_view": "IT proposes a complete 24-hour company-wide lockout. All employee workstations will be disabled."
        },
        {
            "id": "2",
            "label": "Targeted EDR Account Isolation & Lateral Trace",
            "label_short": "Opt 2 (6h EDR Isolation)",
            "downtime": "6 Hours Offline",
            "disruption": "Moderate Disruption (-2 Health Penalty)",
            "disruption_penalty": -2,
            "mitigation_pct": 0.60,
            "desc": "Isolate only identified suspect accounts and endpoints while deploying active telemetry sensors.",
            "technical_detail": "Mitigates 60% of damage; threat actors may still evade detection if auxiliary backdoors exist.",
            "exec_view": "IT proposes targeted isolation of suspect accounts with an estimated 6 hours of department downtime."
        },
        {
            "id": "3",
            "label": "Silent Honeypot Monitoring & Passive Tap",
            "label_short": "Opt 3 (0h Passive Tap)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption (0 Health Penalty)",
            "disruption_penalty": 0,
            "mitigation_pct": 0.25,
            "desc": "Keep all accounts active and route traffic into monitored sandbox honeypots to study tactics.",
            "technical_detail": "High risk! Mitigates only 25% of damage; attackers frequently detect sandboxes and expand access.",
            "exec_view": "IT proposes silent monitoring with zero downtime or business interruption."
        }
    ],
    2: [
        {
            "id": "1",
            "label": "Sever Data Centers & Cold-Storage Backup Rebuild",
            "label_short": "Opt 1 (36h Cold Rebuild)",
            "downtime": "36 Hours Full Outage",
            "disruption": "Severe Disruption (-4 Health Penalty)",
            "disruption_penalty": -4,
            "mitigation_pct": 0.90,
            "desc": "Cut external routing to production clusters and re-image servers from verified off-site cold storage.",
            "technical_detail": "Thwarts 90% of extortion/encryption damage by wiping infected systems completely.",
            "exec_view": "IT proposes unplugging the data center for 36 hours. All digital storefronts and APIs will be offline."
        },
        {
            "id": "2",
            "label": "Emergency Token Invalidation & Subnet Firewalling",
            "label_short": "Opt 2 (8h Subnet Isolation)",
            "downtime": "8 Hours Partial Outage",
            "disruption": "Moderate Disruption (-2 Health Penalty)",
            "disruption_penalty": -2,
            "mitigation_pct": 0.60,
            "desc": "Segment sensitive database tiers behind emergency ACLs and reset application service principals.",
            "technical_detail": "Mitigates 60% of damage, but persistent malware hooks on unsegmented nodes may survive.",
            "exec_view": "IT proposes an 8-hour partial maintenance outage to restrict database traffic."
        },
        {
            "id": "3",
            "label": "Live In-Place Hotpatching Without Taking Systems Down",
            "label_short": "Opt 3 (0h Hotpatching)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption (0 Health Penalty)",
            "disruption_penalty": 0,
            "mitigation_pct": 0.25,
            "desc": "Apply security hotfixes directly to running instances without interrupting customer checkout.",
            "technical_detail": "Mitigates only 25% of damage; active attacker memory payloads continue running undisturbed.",
            "exec_view": "IT proposes live patching with zero customer disruption or storefront downtime."
        }
    ],
    3: [
        {
            "id": "1",
            "label": "Sever All Partner API Integrations & Rebuild Trust Root",
            "label_short": "Opt 1 (48h Vendor Sever)",
            "downtime": "48 Hours Integration Halt",
            "disruption": "Severe Disruption (-4 Health Penalty)",
            "disruption_penalty": -4,
            "mitigation_pct": 0.90,
            "desc": "Sever all third-party supplier pipelines, rotate root cryptographic certs, and audit inbound traffic.",
            "technical_detail": "90% mitigation against supply-chain contamination and persistent backdoors.",
            "exec_view": "IT proposes severing all third-party vendor and supplier feeds for 48 hours, halting order fulfillment."
        },
        {
            "id": "2",
            "label": "Edge CDN Scrubbing & Rate Limiting",
            "label_short": "Opt 2 (10h Scrubbing)",
            "downtime": "10 Hours Slowdown",
            "disruption": "Moderate Disruption (-2 Health Penalty)",
            "disruption_penalty": -2,
            "mitigation_pct": 0.60,
            "desc": "Re-route ingress traffic through external DDoS scrubbing centers with aggressive behavioral captcha.",
            "technical_detail": "Mitigates 60% of infrastructure overload, but does not eradicate entrenched firmware rootkits.",
            "exec_view": "IT proposes routing through scrubbing centers. Customer checkout will experience noticeable latency."
        },
        {
            "id": "3",
            "label": "Maintain Partner Traffic & Rely on Vendor Warranties",
            "label_short": "Opt 3 (0h Self-Attest)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption (0 Health Penalty)",
            "disruption_penalty": 0,
            "mitigation_pct": 0.25,
            "desc": "Avoid penalizing supplier relationships; accept partner security self-attestation reports.",
            "technical_detail": "Mitigates only 25% of damage; the compromised partner remains an open gateway into our network.",
            "exec_view": "IT proposes keeping all vendor feeds open without disruption to holiday revenue."
        }
    ]
}

# Attack-Specific IT Containment Options (Aligned directly with educational dossiers)
ATTACK_SPECIFIC_IT_CHOICES: Dict[Tuple[int, str], List[Dict[str, Any]]] = {
    (1, "A"): [  # Spear Phishing & Credential Harvest
        {
            "id": "1",
            "label": "Enterprise-Wide Password Reset & Workstation Lockout",
            "label_short": "Opt 1 (24h Full Lockout)",
            "downtime": "24 Hours Offline (RTO: 24h)",
            "disruption": "Severe Business Disruption (-4 Health Penalty)",
            "disruption_penalty": -4,
            "mitigation_pct": 0.90,
            "desc": "Revoke all enterprise session tokens, force hardware MFA enrollment, and isolate corporate workstation subnets.",
            "technical_detail": "Stops 90% of attacker lateral movement by immediately terminating compromised user sessions.",
            "exec_view": "IT proposes a complete 24-hour company-wide lockout. All employee workstations will be disabled."
        },
        {
            "id": "2",
            "label": "Targeted Account Quarantine & EDR Deployment",
            "label_short": "Opt 2 (6h EDR Isolation)",
            "downtime": "6 Hours Offline (RTO: 6h)",
            "disruption": "Moderate Disruption (-2 Health Penalty)",
            "disruption_penalty": -2,
            "mitigation_pct": 0.60,
            "desc": "Isolate only the specific compromised finance accounts while deploying Endpoint Detection & Response (EDR) agents.",
            "technical_detail": "Mitigates 60% of damage; threat actors may still evade detection if secondary credentials were compromised.",
            "exec_view": "IT proposes targeted isolation of suspect accounts with an estimated 6 hours of department downtime."
        },
        {
            "id": "3",
            "label": "Silent Honeypot Monitoring & Passive Tap",
            "label_short": "Opt 3 (0h Passive Tap)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption (0 Health Penalty)",
            "disruption_penalty": 0,
            "mitigation_pct": 0.25,
            "desc": "Keep accounts active and route traffic into monitored sandbox honeypots to observe attacker tactics.",
            "technical_detail": "High risk! Mitigates only 25% of damage; attackers frequently detect sandboxes and escalate privileges.",
            "exec_view": "IT proposes silent monitoring with zero downtime or business interruption."
        }
    ],
    (1, "B"): [  # Web Server CVE Exploit
        {
            "id": "1",
            "label": "Air-Gap Public Gateways & Emergency Kernel Patching",
            "label_short": "Opt 1 (24h Air-Gap Patch)",
            "downtime": "24 Hours Offline (RTO: 24h)",
            "disruption": "Severe Business Disruption (-4 Health Penalty)",
            "disruption_penalty": -4,
            "mitigation_pct": 0.90,
            "desc": "Physically disconnect internet-facing web servers and apply emergency operating system and CVE security patches.",
            "technical_detail": "Eliminates 90% of vulnerability attack surface by taking the exploited service completely offline.",
            "exec_view": "IT proposes taking public customer portals and web gateways offline for 24 hours to patch zero-day CVE vulnerabilities."
        },
        {
            "id": "2",
            "label": "Deploy Custom WAF Virtual Patching & Host Isolation",
            "label_short": "Opt 2 (6h WAF Virtual Patch)",
            "downtime": "6 Hours Offline (RTO: 6h)",
            "disruption": "Moderate Disruption (-2 Health Penalty)",
            "disruption_penalty": -2,
            "mitigation_pct": 0.60,
            "desc": "Deploy Web Application Firewall (WAF) regex inspection rules to block exploit payloads while isolating suspect nodes.",
            "technical_detail": "Mitigates 60% of damage; advanced attackers may use payload encoding to bypass firewall rules.",
            "exec_view": "IT proposes applying virtual firewall filters and isolating suspicious web hosts with 6 hours of maintenance downtime."
        },
        {
            "id": "3",
            "label": "Inbound Traffic Inspection & Permissive Logging",
            "label_short": "Opt 3 (0h Passive Inspection)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption (0 Health Penalty)",
            "disruption_penalty": 0,
            "mitigation_pct": 0.25,
            "desc": "Maintain live web traffic and monitor inbound attack signatures without blocking incoming connections.",
            "technical_detail": "Mitigates only 25% of damage; leaves remote code execution vulnerabilities active for exploitation.",
            "exec_view": "IT proposes passive traffic monitoring with zero customer storefront downtime."
        }
    ],
    (1, "C"): [  # AI Prompt Injection
        {
            "id": "1",
            "label": "Hard Offline: Suspend AI Endpoints & Invalidate API Keys",
            "label_short": "Opt 1 (24h AI Offline)",
            "downtime": "24 Hours Offline (RTO: 24h)",
            "disruption": "Severe Business Disruption (-4 Health Penalty)",
            "disruption_penalty": -4,
            "mitigation_pct": 0.90,
            "desc": "Suspend all customer-facing LLM endpoints, revoke compromised backend API tokens, and purge context memory.",
            "technical_detail": "Stops 90% of prompt injection exploit pathways by taking automated assistant integration offline.",
            "exec_view": "IT proposes shutting down all automated customer assistants and backend APIs for 24 hours."
        },
        {
            "id": "2",
            "label": "Deploy Aggressive Input Sanitization Guardrail & Throttling",
            "label_short": "Opt 2 (6h Guardrail Deploy)",
            "downtime": "6 Hours Offline (RTO: 6h)",
            "disruption": "Moderate Disruption (-2 Health Penalty)",
            "disruption_penalty": -2,
            "mitigation_pct": 0.60,
            "desc": "Deploy input regex sanitization filters to strip jailbreak prompts and enforce rate-limiting on user sessions.",
            "technical_detail": "Mitigates 60% of damage; sophisticated linguistic obfuscation may still trigger auxiliary API pivots.",
            "exec_view": "IT proposes a 6-hour maintenance window to install input guardrail filters on chatbot portals."
        },
        {
            "id": "3",
            "label": "Silent Prompt Logging & Asynchronous Security Review",
            "label_short": "Opt 3 (0h Prompt Log)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption (0 Health Penalty)",
            "disruption_penalty": 0,
            "mitigation_pct": 0.25,
            "desc": "Keep customer chatbots online and asynchronously flag anomalous prompts for retrospective review.",
            "technical_detail": "Mitigates only 25% of damage; the adversary retains live access to manipulate backend business logic.",
            "exec_view": "IT proposes passive chat monitoring with zero customer disruption."
        }
    ],
    (2, "A"): [  # PII & Card Exfiltration
        {
            "id": "1",
            "label": "Database Subnet Isolation & Global Credential Revocation",
            "label_short": "Opt 1 (36h DB Isolation)",
            "downtime": "36 Hours Full Outage (RTO: 36h)",
            "disruption": "Severe Disruption (-4 Health Penalty)",
            "disruption_penalty": -4,
            "mitigation_pct": 0.90,
            "desc": "Sever all external database routes and reset enterprise service principal credentials.",
            "technical_detail": "Thwarts 90% of ongoing exfiltration by terminating all database network egress.",
            "exec_view": "IT proposes an emergency 36-hour database outage to sever all exfiltration channels."
        },
        {
            "id": "2",
            "label": "Targeted Egress Firewalling & Service Principal Reset",
            "label_short": "Opt 2 (8h Egress Block)",
            "downtime": "8 Hours Partial Outage (RTO: 8h)",
            "disruption": "Moderate Disruption (-2 Health Penalty)",
            "disruption_penalty": -2,
            "mitigation_pct": 0.60,
            "desc": "Block unauthorized outbound C2 ports and rotate compromised transaction keys.",
            "technical_detail": "Mitigates 60% of damage, but encrypted tunnel staging may bypass port-based blocks.",
            "exec_view": "IT proposes an 8-hour partial maintenance outage to restrict outbound data channels."
        },
        {
            "id": "3",
            "label": "Live In-Place Hotpatching & Dynamic Token Rotation",
            "label_short": "Opt 3 (0h Live Rotation)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption (0 Health Penalty)",
            "disruption_penalty": 0,
            "mitigation_pct": 0.25,
            "desc": "Rotate database tokens dynamically without interrupting live checkout transactions.",
            "technical_detail": "Mitigates only 25% of damage; active attacker sessions in memory continue siphoning records.",
            "exec_view": "IT proposes live token updates with zero checkout downtime."
        }
    ],
    (2, "B"): [  # Database Sabotage
        {
            "id": "1",
            "label": "Sever Production Clusters & Cold-Storage Backup Rebuild",
            "label_short": "Opt 1 (36h Cold Rebuild)",
            "downtime": "36 Hours Full Outage (RTO: 36h)",
            "disruption": "Severe Disruption (-4 Health Penalty)",
            "disruption_penalty": -4,
            "mitigation_pct": 0.90,
            "desc": "Cut external routing to production clusters and re-image servers from verified off-site cold storage.",
            "technical_detail": "Eliminates 90% of sabotage impact by restoring guaranteed clean, tamper-free database snapshots.",
            "exec_view": "IT proposes unplugging data centers for 36 hours to restore uncorrupted database snapshots."
        },
        {
            "id": "2",
            "label": "Restrict Database Traffic & Run Forensic Verification Scripts",
            "label_short": "Opt 2 (8h Data Audit)",
            "downtime": "8 Hours Partial Outage (RTO: 8h)",
            "disruption": "Moderate Disruption (-2 Health Penalty)",
            "disruption_penalty": -2,
            "mitigation_pct": 0.60,
            "desc": "Freeze transaction replicas and run automated consistency scripts line-by-line.",
            "technical_detail": "Mitigates 60% of damage, but subtle data tampering and logical corruption may remain unnoticed.",
            "exec_view": "IT proposes an 8-hour partial outage to audit and reconcile database tables."
        },
        {
            "id": "3",
            "label": "Live Read-Only Mode & Failsafe Integrity Logic",
            "label_short": "Opt 3 (0h Read-Only)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption (0 Health Penalty)",
            "disruption_penalty": 0,
            "mitigation_pct": 0.25,
            "desc": "Switch database to read-only replica mode without interrupting catalog browsing.",
            "technical_detail": "Mitigates only 25% of damage; corrupted transaction records continue causing cascading errors.",
            "exec_view": "IT proposes read-only browsing mode with zero customer store downtime."
        }
    ],
    (2, "C"): [  # Ransomware
        {
            "id": "1",
            "label": "Burn and Rebuild Bare-Metal from Clean Offline Golden Images",
            "label_short": "Opt 1 (36h Bare Metal)",
            "downtime": "36 Hours Full Outage (RTO: 36h)",
            "disruption": "Severe Disruption (-4 Health Penalty)",
            "disruption_penalty": -4,
            "mitigation_pct": 0.90,
            "desc": "Physically wipe encrypted domain controllers and re-image bare-metal servers from golden offline media.",
            "technical_detail": "Overcomes 90% of ransomware impact by completely expelling attacker encryption keys and persistence.",
            "exec_view": "IT proposes a 36-hour total shutdown to wipe and re-install all encrypted domain servers."
        },
        {
            "id": "2",
            "label": "Emergency Network Partition & Decryption Sandbox",
            "label_short": "Opt 2 (8h Net Partition)",
            "downtime": "8 Hours Partial Outage (RTO: 8h)",
            "disruption": "Moderate Disruption (-2 Health Penalty)",
            "disruption_penalty": -2,
            "mitigation_pct": 0.60,
            "desc": "Partition compromised subnet zones and isolate encrypted volumes in forensic sandboxes.",
            "technical_detail": "Mitigates 60% of damage, but encryption payloads on partially partitioned nodes may still finish.",
            "exec_view": "IT proposes an 8-hour network partition to quarantine encrypted subnet hosts."
        },
        {
            "id": "3",
            "label": "Keep Production Online & Pursue Back-Channel Key Negotiation",
            "label_short": "Opt 3 (0h Threat Bounty)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption (0 Health Penalty)",
            "disruption_penalty": 0,
            "mitigation_pct": 0.25,
            "desc": "Attempt back-channel negotiations for decryption keys while keeping production storefronts online.",
            "technical_detail": "High risk! Mitigates only 25% of damage; extorters often provide corrupt or non-functioning decrypters.",
            "exec_view": "IT proposes keeping servers active and pursuing digital decryption keys with zero downtime."
        }
    ]
}

def get_it_choices(round_num: int, attack_key: Optional[str] = None) -> List[Dict[str, Any]]:
    """Returns IT containment options aligned with the active attack vector."""
    if attack_key:
        pair = (int(round_num), str(attack_key).upper())
        if pair in ATTACK_SPECIFIC_IT_CHOICES:
            return ATTACK_SPECIFIC_IT_CHOICES[pair]
    return IT_CHOICES.get(int(round_num), IT_CHOICES.get(1, []))

# Executive Governance Directives (Executives review IT's proposed plan blindly)
EXEC_GOVERNANCE_OPTIONS = [
    {
        "id": "approve",
        "action": "approve",
        "label": "✅ Approve IT Recommendation",
        "tagline": "Prioritize Security & Containment",
        "desc": "Authorize IT's full containment directive. Accept the proposed operational downtime and customer disruption to guarantee maximum breach containment."
    },
    {
        "id": "downgrade",
        "action": "downgrade",
        "label": "⚖️ Downgrade to Business Compromise",
        "tagline": "Balance Revenue & Containment",
        "desc": "Order IT to cut the downtime in half and keep primary customer portals online. (Note: Halves IT's containment effectiveness, but preserves short-term business operations)."
    },
    {
        "id": "overrule",
        "action": "overrule",
        "label": "🚫 Overrule IT Plan (Protect Business Continuity)",
        "tagline": "Prioritize Immediate Revenue & Appearances",
        "desc": "Reject system shutdowns and maintain uninterrupted operations. Protect immediate quarterly revenue and stock valuation, leaving the network vulnerable to continued attacker intrusion."
    }
]

# Media Headlines by Round (4 Tiers: Sensationalist, Critical, Balanced, Favorable)
DYNAMIC_HEADLINES = {
    1: [
        {"id": "Headline 1", "label": "Sensationalist (-12 HP)", "tier": "Sensationalist", "headline": "💥 CloudStore in Freefall: Catastrophic Infiltration Exposed!", "health_delta": -12, "desc": "Sensationalized panic coverage driving immediate stock selloff."},
        {"id": "Headline 2", "label": "Critical (-5 HP)", "tier": "Critical", "headline": "⚠️ CloudStore Breached: Security Lapses Spark Customer Alarm", "health_delta": -5, "desc": "Critical investigative report highlighting lax cyber hygiene."},
        {"id": "Headline 3", "label": "Balanced (+2 HP)", "tier": "Balanced", "headline": "📰 CloudStore Investigates Security Anomaly: Systems Monitored", "health_delta": 2, "desc": "Objective news coverage noting ongoing internal review."},
        {"id": "Headline 4", "label": "Favorable (+8 HP)", "tier": "Favorable", "headline": "🛡️ Decisive Defense: CloudStore Thwarts Infiltration Attempt", "health_delta": 8, "desc": "Commendatory press praising rapid corporate response."}
    ],
    2: [
        {"id": "Headline 1", "label": "Sensationalist (-12 HP)", "tier": "Sensationalist", "headline": "💥 Total Blackout: Extortionists Hold CloudStore Hostage!", "health_delta": -12, "desc": "Front-page headlines stoking widespread public panic."},
        {"id": "Headline 2", "label": "Critical (-5 HP)", "tier": "Critical", "headline": "⚠️ Millions at Risk: CloudStore Stumbles as Breach Deepens", "health_delta": -5, "desc": "Journalistic scrutiny over executive delays and lost customer trust."},
        {"id": "Headline 3", "label": "Balanced (+2 HP)", "tier": "Balanced", "headline": "📰 CloudStore Executes Incident Response Amid System Strains", "health_delta": 2, "desc": "Factual reporting on containment protocols and business impact."},
        {"id": "Headline 4", "label": "Favorable (+8 HP)", "tier": "Favorable", "headline": "🛡️ Customer First: CloudStore Shields Data with Strong Protocols", "health_delta": 8, "desc": "Positive media narrative highlighting transparency and resilience."}
    ],
    3: [
        {"id": "Headline 1", "label": "Sensationalist (-12 HP)", "tier": "Sensationalist", "headline": "💥 Insolvency Looming? CloudStore Collapses Under Cyber Blitz", "health_delta": -12, "desc": "Brutal market commentary questioning enterprise survival."},
        {"id": "Headline 2", "label": "Critical (-5 HP)", "tier": "Critical", "headline": "⚠️ Regulatory Inquiries Launched Against CloudStore Leadership", "health_delta": -5, "desc": "Critical focus on regulatory fines and compliance liabilities."},
        {"id": "Headline 3", "label": "Balanced (+2 HP)", "tier": "Balanced", "headline": "📰 CloudStore Concludes Containment Phase; Audits Continue", "health_delta": 2, "desc": "Balanced assessment of long-term recovery prospects."},
        {"id": "Headline 4", "label": "Favorable (+8 HP)", "tier": "Favorable", "headline": "🛡️ Masterclass in Crisis Leadership: CloudStore Prevails", "health_delta": 8, "desc": "Glowing review praising the organization's crisis turnaround."}
    ]
}
