"""
game_data.py
Scenario Definitions, Team Passcodes, Phase Timing, and Modular Content
for CloudStore Command: Cyber Attack Simulation
"""

import os
from typing import Dict, Any, List, Optional

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
    "hacker": 300,   # 5 Minutes (300s)
    "it": 300,       # 5 Minutes (300s)
    "exec": 180,     # 3 Minutes (180s)
    "media": 300,    # 5 Minutes (300s)
    "recap": 120     # 2 Minutes (120s)
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
            "md_file": "apt_exfiltration.md",
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
        {"id": "Headline 1", "label": "Headline 1", "tier": "Sensationalist", "headline": "💥 CloudStore in Freefall: Catastrophic Infiltration Exposed!", "health_delta": -12, "desc": "Sensationalized panic coverage driving immediate stock selloff."},
        {"id": "Headline 2", "label": "Headline 2", "tier": "Critical", "headline": "⚠️ CloudStore Breached: Security Lapses Spark Customer Alarm", "health_delta": -5, "desc": "Critical investigative report highlighting lax cyber hygiene."},
        {"id": "Headline 3", "label": "Headline 3", "tier": "Balanced", "headline": "📰 CloudStore Investigates Security Anomaly: Systems Monitored", "health_delta": 2, "desc": "Objective news coverage noting ongoing internal review."},
        {"id": "Headline 4", "label": "Headline 4", "tier": "Favorable", "headline": "🛡️ Decisive Defense: CloudStore Thwarts Infiltration Attempt", "health_delta": 8, "desc": "Commendatory press praising rapid corporate response."}
    ],
    2: [
        {"id": "Headline 1", "label": "Headline 1", "tier": "Sensationalist", "headline": "💥 Total Blackout: Extortionists Hold CloudStore Hostage!", "health_delta": -12, "desc": "Front-page headlines stoking widespread public panic."},
        {"id": "Headline 2", "label": "Headline 2", "tier": "Critical", "headline": "⚠️ Millions at Risk: CloudStore Stumbles as Breach Deepens", "health_delta": -5, "desc": "Journalistic scrutiny over executive delays and lost customer trust."},
        {"id": "Headline 3", "label": "Headline 3", "tier": "Balanced", "headline": "📰 CloudStore Executes Incident Response Amid System Strains", "health_delta": 2, "desc": "Factual reporting on containment protocols and business impact."},
        {"id": "Headline 4", "label": "Headline 4", "tier": "Favorable", "headline": "🛡️ Customer First: CloudStore Shields Data with Strong Protocols", "health_delta": 8, "desc": "Positive media narrative highlighting transparency and resilience."}
    ],
    3: [
        {"id": "Headline 1", "label": "Headline 1", "tier": "Sensationalist", "headline": "💥 Insolvency Looming? CloudStore Collapses Under Cyber Blitz", "health_delta": -12, "desc": "Brutal market commentary questioning enterprise survival."},
        {"id": "Headline 2", "label": "Headline 2", "tier": "Critical", "headline": "⚠️ Regulatory Inquiries Launched Against CloudStore Leadership", "health_delta": -5, "desc": "Critical focus on regulatory fines and compliance liabilities."},
        {"id": "Headline 3", "label": "Headline 3", "tier": "Balanced", "headline": "📰 CloudStore Concludes Containment Phase; Audits Continue", "health_delta": 2, "desc": "Balanced assessment of long-term recovery prospects."},
        {"id": "Headline 4", "label": "Headline 4", "tier": "Favorable", "headline": "🛡️ Masterclass in Crisis Leadership: CloudStore Prevails", "health_delta": 8, "desc": "Glowing review praising the organization's crisis turnaround."}
    ]
}
