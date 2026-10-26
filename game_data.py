"""
game_data.py
Scenario Definitions, Team Passcodes, Phase Timing, and Modular Content
for CloudStore Command: Cyber Attack Simulation
"""

import os
import random
from typing import Dict, Any, List, Optional, Tuple

def _generate_team_codes() -> Dict[str, str]:
    """
    Generates team passcodes at application startup with randomized 3-digit suffixes for Captain roles.
    Guarantees variation across launches while maintaining fixed admin and instructor passwords.
    """
    def rand_3digits() -> str:
        return f"{random.randint(100, 999):03d}"

    return {
        "main": "admin123",                      # Game Master / Mission Control (always admin123)
        "hackers": f"hacker{rand_3digits()}",    # Threat Actor Command Captain
        "it": f"tech{rand_3digits()}",           # IT Defense Command Captain
        "exec": f"board{rand_3digits()}",        # Executive Boardroom Captain
        "media": f"press{rand_3digits()}",       # Media & PR Scrum Captain
        "instructor": "tryit123",                # Single-Player Instructor Sandbox (fixed)
        "solo": "tryit123"                       # Alias for instructor mode (fixed)
    }

# Team Passcodes (used by Team Captains to unlock decision & polling controls)
TEAM_CODES = _generate_team_codes()

def reset_team_codes() -> Dict[str, str]:
    """Regenerates randomized 3-digit passcodes for team captains."""
    global TEAM_CODES
    TEAM_CODES = _generate_team_codes()
    return TEAM_CODES

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
            "complexity": "Low",
            "damage_potential": "Moderate",
            "anonymity": "High (Stealth)",
            "exposure_penalty": 0,
            "description": "Targeted spoofed invoice deceived finance staff. Executive credentials captured.",
            "md_file": "phishing.md",
            "assessment": "Reliable entry point with low initial suspicion, giving access to user accounts."
        },
        "B": {
            "id": "B",
            "name": "Unpatched Web Server CVE Exploit",
            "icon": "🛠️",
            "damage": -25,
            "complexity": "Medium",
            "damage_potential": "High",
            "anonymity": "Moderate (Standard)",
            "exposure_penalty": 1,
            "description": "Automated scanning identified known remote code execution vulnerability on public gateway.",
            "md_file": "zero_day.md",
            "assessment": "Direct system-level foothold giving the attacker access to core application servers."
        },
        "C": {
            "id": "C",
            "name": "AI LLM Prompt Injection & API Pivot",
            "icon": "🤖",
            "damage": -30,
            "complexity": "High",
            "damage_potential": "Catastrophic",
            "anonymity": "Low (Noisy)",
            "exposure_penalty": 2,
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
            "complexity": "Medium",
            "damage_potential": "High",
            "anonymity": "High (Stealth)",
            "exposure_penalty": 0,
            "description": "Covert exfiltration of 1.5 million customer transaction records and hashes to bulletproof hosting.",
            "md_file": "apt_exfiltration.md",
            "assessment": "Silent exfiltration designed for dark web monetization and immense regulatory fallout."
        },
        "B": {
            "id": "B",
            "name": "Production Database Sabotage & Deletion",
            "icon": "💥",
            "damage": -28,
            "complexity": "Medium",
            "damage_potential": "Catastrophic",
            "anonymity": "Low (Noisy)",
            "exposure_penalty": 2,
            "description": "Attacker deployed malicious drop-table scripts and wiped primary transactional replicas.",
            "md_file": "database_sabotage.md",
            "assessment": "Direct physical/digital destruction aimed at crippling the organization's core operations."
        },
        "C": {
            "id": "C",
            "name": "Double Extortion Ransomware Lockout",
            "icon": "💀",
            "damage": -30,
            "complexity": "High",
            "damage_potential": "Catastrophic",
            "anonymity": "Low (Noisy)",
            "exposure_penalty": 2,
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
            "complexity": "High",
            "damage_potential": "High",
            "anonymity": "High (Stealth)",
            "exposure_penalty": 0,
            "description": "Compromised third-party inventory partner API utilized to poison shipping manifests.",
            "md_file": "supply_chain.md",
            "assessment": "Leverages external vendor trust to infect downstream enterprise infrastructure."
        },
        "B": {
            "id": "B",
            "name": "Volumetric DDoS Smokescreen & API Wipe",
            "icon": "🌊",
            "damage": -28,
            "complexity": "Low",
            "damage_potential": "Moderate",
            "anonymity": "Moderate (Standard)",
            "exposure_penalty": 1,
            "description": "Massive 800 Gbps DDoS attack launched to mask silent cloud IAM permission modifications.",
            "md_file": "ddos_smokescreen.md",
            "assessment": "Overwhelms defense sensors with noise while critical assets are secretly drained."
        },
        "C": {
            "id": "C",
            "name": "APT Deep Persistence & Dark Web Auction",
            "icon": "🏴‍☠️",
            "damage": -30,
            "complexity": "High",
            "damage_potential": "Catastrophic",
            "anonymity": "Moderate (Standard)",
            "exposure_penalty": 1,
            "description": "Advanced persistent threat implants UEFI firmware rootkit and lists corporate IP on dark forums.",
            "md_file": "firmware_persistence.md",
            "assessment": "Maximum reputation devastation and permanent loss of enterprise intellectual property."
        }
    }
}

# IT Defense Containment Options
# Trade-off rule: Aggressive options with severe downtime provide the highest threat containment!
IT_CHOICES = {
    1: [
        {
            "id": "1",
            "label": "Full Credential Reset & Workstation Lockout",
            "label_short": "Opt 1 (Full Lockout Isolation)",
            "downtime": "24 Hours Offline",
            "disruption": "Severe Business Disruption",
            "disruption_penalty": -4,
            "complexity": "High",
            "customer_impact": "Severe Storefront Outage",
            "mitigation_likelihood": "High / Guaranteed",
            "mitigation_range": (0.75, 0.95),
            "mitigation_pct": 0.90,
            "desc": "Revoke all enterprise session tokens, force hardware MFA enrollment, and isolate corporate subnet.",
            "technical_detail": "Guarantees comprehensive threat containment by terminating compromised active tokens across all enterprise tiers.",
            "stock_outlook": "Short-term share price dip due to frozen operations, but institutional investors favor decisive security posture.",
            "reputation_risk": "Short-term frustration over downtime, but eliminates long-term brand destruction from stolen user records.",
            "exec_view": "IT proposes a complete 24-hour company-wide lockout. All employee workstations and internal portals will be disabled."
        },
        {
            "id": "2",
            "label": "Targeted EDR Account Isolation & Lateral Trace",
            "label_short": "Opt 2 (Targeted EDR Isolation)",
            "downtime": "6 Hours Offline",
            "disruption": "Moderate Disruption",
            "disruption_penalty": -2,
            "complexity": "Moderate",
            "customer_impact": "Noticeable Latency & Partial Stoppage",
            "mitigation_likelihood": "Moderate / Contingent",
            "mitigation_range": (0.45, 0.70),
            "mitigation_pct": 0.60,
            "desc": "Isolate only identified suspect accounts and endpoints while deploying active telemetry sensors.",
            "technical_detail": "Provides targeted containment of known indicators; threat actors may evade detection if auxiliary backdoors exist.",
            "stock_outlook": "Moderate market nervousness; analysts question whether partial fixes fully eradicated the intrusion.",
            "reputation_risk": "Isolated customer friction; manageable press coverage provided no further customer data leaks.",
            "exec_view": "IT proposes targeted isolation of suspect accounts with an estimated 6 hours of department downtime."
        },
        {
            "id": "3",
            "label": "Silent Honeypot Monitoring & Passive Tap",
            "label_short": "Opt 3 (Passive Monitoring)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption",
            "disruption_penalty": 0,
            "complexity": "Low",
            "customer_impact": "Minimal / Seamless",
            "mitigation_likelihood": "Low / Uncertain",
            "mitigation_range": (0.15, 0.35),
            "mitigation_pct": 0.25,
            "desc": "Keep all accounts active and route traffic into monitored sandbox honeypots to study tactics.",
            "technical_detail": "Leaves active attacker connections open; adversaries routinely detect sandboxes and escalate core privileges.",
            "stock_outlook": "Protects immediate quarterly earnings guidance, but exposes firm to massive liability if breach worsens.",
            "reputation_risk": "Zero immediate customer complaints, but catastrophic reputation loss if ongoing data exfiltration becomes public.",
            "exec_view": "IT proposes silent monitoring with zero downtime or business interruption."
        }
    ],
    2: [
        {
            "id": "1",
            "label": "Sever Data Centers & Cold-Storage Backup Rebuild",
            "label_short": "Opt 1 (Cold Rebuild Outage)",
            "downtime": "36 Hours Full Outage",
            "disruption": "Severe Disruption",
            "disruption_penalty": -4,
            "complexity": "High",
            "customer_impact": "Severe Storefront Outage",
            "mitigation_likelihood": "High / Guaranteed",
            "mitigation_range": (0.75, 0.95),
            "mitigation_pct": 0.90,
            "desc": "Cut external routing to production clusters and re-image servers from verified off-site cold storage.",
            "technical_detail": "Overcomes malware and extortion persistence by restoring clean, uncompromised bare-metal images.",
            "stock_outlook": "Sharp temporary selloff from complete storefront shutdown; market rewards verified clean recovery.",
            "reputation_risk": "Widespread customer complaints during outage; however, preserves long-term customer trust by protecting core data.",
            "exec_view": "IT proposes unplugging the data center for 36 hours. All digital storefronts and APIs will be offline."
        },
        {
            "id": "2",
            "label": "Emergency Token Invalidation & Subnet Firewalling",
            "label_short": "Opt 2 (Subnet Isolation)",
            "downtime": "8 Hours Partial Outage",
            "disruption": "Moderate Disruption",
            "disruption_penalty": -2,
            "complexity": "Moderate",
            "customer_impact": "Noticeable Checkout Latency",
            "mitigation_likelihood": "Moderate / Contingent",
            "mitigation_range": (0.45, 0.70),
            "mitigation_pct": 0.60,
            "desc": "Segment sensitive database tiers behind emergency ACLs and reset application service principals.",
            "technical_detail": "Constrains attacker lateral reach to partitioned zones, but persistent hooks on edge nodes may survive.",
            "stock_outlook": "Wall Street reacts cautiously; questions remain about lingering operational exposure.",
            "reputation_risk": "Checkout slowdowns irritate active shoppers; social media sentiment requires active PR monitoring.",
            "exec_view": "IT proposes an 8-hour partial maintenance outage to restrict database traffic."
        },
        {
            "id": "3",
            "label": "Live In-Place Hotpatching Without Taking Systems Down",
            "label_short": "Opt 3 (Live Hotpatching)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption",
            "disruption_penalty": 0,
            "complexity": "Low",
            "customer_impact": "Minimal / Seamless",
            "mitigation_likelihood": "Low / Uncertain",
            "mitigation_range": (0.15, 0.35),
            "mitigation_pct": 0.25,
            "desc": "Apply security hotfixes directly to running instances without interrupting customer checkout.",
            "technical_detail": "Unsafe in high-severity intrusions; active in-memory payloads continue siphoning records unhindered.",
            "stock_outlook": "Short-term stock stability, but extreme latent financial risk of catastrophic secondary disclosures.",
            "reputation_risk": "Customers remain unaware in the near term, but risk complete loss of loyalty if compromised later.",
            "exec_view": "IT proposes live patching with zero customer disruption or storefront downtime."
        }
    ],
    3: [
        {
            "id": "1",
            "label": "Sever All Partner API Integrations & Rebuild Trust Root",
            "label_short": "Opt 1 (Vendor Pipeline Sever)",
            "downtime": "48 Hours Integration Halt",
            "disruption": "Severe Disruption",
            "disruption_penalty": -4,
            "complexity": "High",
            "customer_impact": "Severe Order Halt",
            "mitigation_likelihood": "High / Guaranteed",
            "mitigation_range": (0.75, 0.95),
            "mitigation_pct": 0.90,
            "desc": "Sever all third-party supplier pipelines, rotate root cryptographic certs, and audit inbound traffic.",
            "technical_detail": "Completely purges downstream supply-chain infection vectors and revokes untrusted partner credentials.",
            "stock_outlook": "Significant operational supply disruption; analysts praise rigorous root-cause remediation.",
            "reputation_risk": "Delayed fulfillment generates negative reviews, but prevents catastrophic partner-wide compromise.",
            "exec_view": "IT proposes severing all third-party vendor and supplier feeds for 48 hours, halting order fulfillment."
        },
        {
            "id": "2",
            "label": "Edge CDN Scrubbing & Rate Limiting",
            "label_short": "Opt 2 (Edge Scrubbing)",
            "downtime": "10 Hours Slowdown",
            "disruption": "Moderate Disruption",
            "disruption_penalty": -2,
            "complexity": "Moderate",
            "customer_impact": "Noticeable Checkout Latency",
            "mitigation_likelihood": "Moderate / Contingent",
            "mitigation_range": (0.45, 0.70),
            "mitigation_pct": 0.60,
            "desc": "Re-route ingress traffic through external DDoS scrubbing centers with aggressive behavioral captcha.",
            "technical_detail": "Mitigates external traffic floods, but does not eradicate entrenched firmware or internal backdoors.",
            "stock_outlook": "Investors stay watchful; questions linger regarding infrastructure resilience under heavy load.",
            "reputation_risk": "Customer annoyance over aggressive captcha checks and transaction delays.",
            "exec_view": "IT proposes routing through scrubbing centers. Customer checkout will experience noticeable latency."
        },
        {
            "id": "3",
            "label": "Maintain Partner Traffic & Rely on Vendor Warranties",
            "label_short": "Opt 3 (Vendor Self-Attest)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption",
            "disruption_penalty": 0,
            "complexity": "Low",
            "customer_impact": "Minimal / Seamless",
            "mitigation_likelihood": "Low / Uncertain",
            "mitigation_range": (0.15, 0.35),
            "mitigation_pct": 0.25,
            "desc": "Avoid penalizing supplier relationships; accept partner security self-attestation reports.",
            "technical_detail": "Leaves known vulnerable partner routes connected; attackers maintain persistence through supply chain.",
            "stock_outlook": "Protects immediate shipping quotas, but leaves corporate liabilities wide open to regulatory fines.",
            "reputation_risk": "Near-term business-as-usual, but existential brand risk if supplier breach spills into media.",
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
            "label_short": "Opt 1 (Full Lockout Isolation)",
            "downtime": "24 Hours Offline (RTO: 24h)",
            "disruption": "Severe Business Disruption",
            "disruption_penalty": -4,
            "complexity": "High",
            "customer_impact": "Severe Storefront Outage",
            "mitigation_likelihood": "High / Guaranteed",
            "mitigation_range": (0.75, 0.95),
            "mitigation_pct": 0.90,
            "desc": "Revoke all enterprise session tokens, force hardware MFA enrollment, and isolate corporate workstation subnets.",
            "technical_detail": "Guarantees comprehensive threat containment by terminating compromised active user sessions and isolating lateral pathways.",
            "stock_outlook": "Short-term share price drop due to revenue pause, but Wall Street stabilizes as containment is confirmed.",
            "reputation_risk": "Temporary user complaints about downtime, but prevents customer data theft and long-term brand erosion.",
            "exec_view": "IT proposes a complete 24-hour company-wide lockout. All employee workstations will be disabled."
        },
        {
            "id": "2",
            "label": "Targeted Account Quarantine & EDR Deployment",
            "label_short": "Opt 2 (Targeted Quarantine)",
            "downtime": "6 Hours Offline (RTO: 6h)",
            "disruption": "Moderate Disruption",
            "disruption_penalty": -2,
            "complexity": "Moderate",
            "customer_impact": "Noticeable Checkout Latency",
            "mitigation_likelihood": "Moderate / Contingent",
            "mitigation_range": (0.45, 0.70),
            "mitigation_pct": 0.60,
            "desc": "Isolate only the specific compromised finance accounts while deploying Endpoint Detection & Response (EDR) agents.",
            "technical_detail": "Provides targeted containment of suspect endpoints; threat actors may evade detection if secondary credentials exist.",
            "stock_outlook": "Moderate market nervousness; analysts question partial disruptions and lingering vulnerabilities.",
            "reputation_risk": "Customer friction over checkout errors; moderate risk of negative social media sentiment.",
            "exec_view": "IT proposes targeted isolation of suspect accounts with an estimated 6 hours of department downtime."
        },
        {
            "id": "3",
            "label": "Silent Honeypot Monitoring & Passive Tap",
            "label_short": "Opt 3 (Passive Monitoring)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption",
            "disruption_penalty": 0,
            "complexity": "Low",
            "customer_impact": "Minimal / Seamless",
            "mitigation_likelihood": "Low / Uncertain",
            "mitigation_range": (0.15, 0.35),
            "mitigation_pct": 0.25,
            "desc": "Keep accounts active and route traffic into monitored sandbox honeypots to observe attacker tactics.",
            "technical_detail": "Maintains live connections; threat actors frequently detect sandboxes and escalate privileges on active accounts.",
            "stock_outlook": "Maintains short-term earnings guidance, but creates immense catastrophe risk if uncontained breach goes public.",
            "reputation_risk": "Zero immediate customer complaints, but catastrophic brand destruction if accounts are compromised.",
            "exec_view": "IT proposes silent monitoring with zero downtime or business interruption."
        }
    ],
    (1, "B"): [  # Web Server CVE Exploit
        {
            "id": "1",
            "label": "Air-Gap Public Gateways & Emergency Kernel Patching",
            "label_short": "Opt 1 (Air-Gap Patch)",
            "downtime": "24 Hours Offline (RTO: 24h)",
            "disruption": "Severe Business Disruption",
            "disruption_penalty": -4,
            "complexity": "High",
            "customer_impact": "Severe Storefront Outage",
            "mitigation_likelihood": "High / Guaranteed",
            "mitigation_range": (0.75, 0.95),
            "mitigation_pct": 0.90,
            "desc": "Physically disconnect internet-facing web servers and apply emergency operating system and CVE security patches.",
            "technical_detail": "Eliminates remote code execution attack surface by taking the exploited service completely offline.",
            "stock_outlook": "Short-term selloff due to offline checkout portals, but market rewards decisive vulnerability elimination.",
            "reputation_risk": "Public frustration over portal blackout, but shields payment backends from catastrophic exposure.",
            "exec_view": "IT proposes taking public customer portals and web gateways offline for 24 hours to patch zero-day CVE vulnerabilities."
        },
        {
            "id": "2",
            "label": "Deploy Custom WAF Virtual Patching & Host Isolation",
            "label_short": "Opt 2 (WAF Virtual Patch)",
            "downtime": "6 Hours Offline (RTO: 6h)",
            "disruption": "Moderate Disruption",
            "disruption_penalty": -2,
            "complexity": "Moderate",
            "customer_impact": "Noticeable Checkout Latency",
            "mitigation_likelihood": "Moderate / Contingent",
            "mitigation_range": (0.45, 0.70),
            "mitigation_pct": 0.60,
            "desc": "Deploy Web Application Firewall (WAF) regex inspection rules to block exploit payloads while isolating suspect nodes.",
            "technical_detail": "Filters known exploit signatures, though payload obfuscation and encoding may bypass inspection filters.",
            "stock_outlook": "Cautious market response; questions remain on whether custom firewall rules completely stop intrusion.",
            "reputation_risk": "Intermittent false-positive blocks on customer logins; moderate brand friction.",
            "exec_view": "IT proposes applying virtual firewall filters and isolating suspicious web hosts with 6 hours of maintenance downtime."
        },
        {
            "id": "3",
            "label": "Inbound Traffic Inspection & Permissive Logging",
            "label_short": "Opt 3 (Passive Inspection)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption",
            "disruption_penalty": 0,
            "complexity": "Low",
            "customer_impact": "Minimal / Seamless",
            "mitigation_likelihood": "Low / Uncertain",
            "mitigation_range": (0.15, 0.35),
            "mitigation_pct": 0.25,
            "desc": "Maintain live web traffic and monitor inbound attack signatures without blocking incoming connections.",
            "technical_detail": "Leaves exploited web services fully accessible to threat actors; active shell payloads continue unhindered.",
            "stock_outlook": "Preserves immediate checkout revenue, but poses existential downside risk if attackers seize customer databases.",
            "reputation_risk": "Temporary customer ignorance; catastrophic brand collapse upon eventual public disclosure.",
            "exec_view": "IT proposes passive traffic monitoring with zero customer storefront downtime."
        }
    ],
    (1, "C"): [  # AI Prompt Injection
        {
            "id": "1",
            "label": "Hard Offline: Suspend AI Endpoints & Invalidate API Keys",
            "label_short": "Opt 1 (AI Offline Suspension)",
            "downtime": "24 Hours Offline (RTO: 24h)",
            "disruption": "Severe Business Disruption",
            "disruption_penalty": -4,
            "complexity": "High",
            "customer_impact": "Severe Storefront Outage",
            "mitigation_likelihood": "High / Guaranteed",
            "mitigation_range": (0.75, 0.95),
            "mitigation_pct": 0.90,
            "desc": "Suspend all customer-facing LLM endpoints, revoke compromised backend API tokens, and purge context memory.",
            "technical_detail": "Completely severs prompt injection exploit pathways by taking automated assistant integration offline.",
            "stock_outlook": "Negative headlines regarding AI downtime; tech analysts appreciate immediate containment of backend APIs.",
            "reputation_risk": "Customer complaints over disabled support assistants, but prevents weaponization of customer chat.",
            "exec_view": "IT proposes shutting down all automated customer assistants and backend APIs for 24 hours."
        },
        {
            "id": "2",
            "label": "Deploy Aggressive Input Sanitization Guardrail & Throttling",
            "label_short": "Opt 2 (Guardrail Deployment)",
            "downtime": "6 Hours Offline (RTO: 6h)",
            "disruption": "Moderate Disruption",
            "disruption_penalty": -2,
            "complexity": "Moderate",
            "customer_impact": "Noticeable Checkout Latency",
            "mitigation_likelihood": "Moderate / Contingent",
            "mitigation_range": (0.45, 0.70),
            "mitigation_pct": 0.60,
            "desc": "Deploy input regex sanitization filters to strip jailbreak prompts and enforce rate-limiting on user sessions.",
            "technical_detail": "Suppresses common prompt injection patterns, but sophisticated linguistic obfuscation may still pivot to APIs.",
            "stock_outlook": "Investors cautiously optimistic on proactive AI governance; some uncertainty over filter efficacy.",
            "reputation_risk": "Frustration over chatbot rate limits; mild customer sentiment drop.",
            "exec_view": "IT proposes a 6-hour maintenance window to install input guardrail filters on chatbot portals."
        },
        {
            "id": "3",
            "label": "Silent Prompt Logging & Asynchronous Security Review",
            "label_short": "Opt 3 (Passive Prompt Logging)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption",
            "disruption_penalty": 0,
            "complexity": "Low",
            "customer_impact": "Minimal / Seamless",
            "mitigation_likelihood": "Low / Uncertain",
            "mitigation_range": (0.15, 0.35),
            "mitigation_pct": 0.25,
            "desc": "Keep customer chatbots online and asynchronously flag anomalous prompts for retrospective review.",
            "technical_detail": "Leaves LLM assistant backend APIs connected; adversary continues manipulating business logic and extracting tokens.",
            "stock_outlook": "Protects customer checkout experience today, but invites devastating class-action risk tomorrow.",
            "reputation_risk": "Zero immediate disruption, but catastrophic brand erosion if chatbot leaks private customer histories.",
            "exec_view": "IT proposes passive chat monitoring with zero customer disruption."
        }
    ],
    (2, "A"): [  # PII & Card Exfiltration
        {
            "id": "1",
            "label": "Database Subnet Isolation & Global Credential Revocation",
            "label_short": "Opt 1 (DB Isolation Outage)",
            "downtime": "36 Hours Full Outage (RTO: 36h)",
            "disruption": "Severe Disruption",
            "disruption_penalty": -4,
            "complexity": "High",
            "customer_impact": "Severe Storefront Outage",
            "mitigation_likelihood": "High / Guaranteed",
            "mitigation_range": (0.75, 0.95),
            "mitigation_pct": 0.90,
            "desc": "Sever all external database routes and reset enterprise service principal credentials.",
            "technical_detail": "Thwarts exfiltration pipelines by terminating database network egress across all active clusters.",
            "stock_outlook": "Heavy immediate market selloff from transactional freeze; long-term solvency protected against regulatory fines.",
            "reputation_risk": "Major customer backlash during multi-day downtime; crucial to preserving customer PII and card safety.",
            "exec_view": "IT proposes an emergency 36-hour database outage to sever all exfiltration channels."
        },
        {
            "id": "2",
            "label": "Targeted Egress Firewalling & Service Principal Reset",
            "label_short": "Opt 2 (Targeted Egress Block)",
            "downtime": "8 Hours Partial Outage (RTO: 8h)",
            "disruption": "Moderate Disruption",
            "disruption_penalty": -2,
            "complexity": "Moderate",
            "customer_impact": "Noticeable Checkout Latency",
            "mitigation_likelihood": "Moderate / Contingent",
            "mitigation_range": (0.45, 0.70),
            "mitigation_pct": 0.60,
            "desc": "Block unauthorized outbound C2 ports and rotate compromised transaction keys.",
            "technical_detail": "Limits standard exfiltration routes, though encrypted tunnel staging on alternate ports may bypass blocks.",
            "stock_outlook": "Mixed market sentiment; investors wonder if customer card data remains exposed.",
            "reputation_risk": "Noticeable payment errors during key rotation; elevated risk of social media backlash.",
            "exec_view": "IT proposes an 8-hour partial maintenance outage to restrict outbound data channels."
        },
        {
            "id": "3",
            "label": "Live In-Place Hotpatching & Dynamic Token Rotation",
            "label_short": "Opt 3 (Live Hotpatching)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption",
            "disruption_penalty": 0,
            "complexity": "Low",
            "customer_impact": "Minimal / Seamless",
            "mitigation_likelihood": "Low / Uncertain",
            "mitigation_range": (0.15, 0.35),
            "mitigation_pct": 0.25,
            "desc": "Rotate database tokens dynamically without interrupting live checkout transactions.",
            "technical_detail": "Leaves active adversary sessions in memory; compromised tokens continue siphoning records unimpeded.",
            "stock_outlook": "Avoids immediate revenue hit, but guarantees astronomical GDPR / PCI regulatory fines if exfiltration continues.",
            "reputation_risk": "Superficial stability masking catastrophic breach; severe risk of permanent loss of customer trust.",
            "exec_view": "IT proposes live token updates with zero checkout downtime."
        }
    ],
    (2, "B"): [  # Database Sabotage
        {
            "id": "1",
            "label": "Sever Production Clusters & Cold-Storage Backup Rebuild",
            "label_short": "Opt 1 (Cold Rebuild Outage)",
            "downtime": "36 Hours Full Outage (RTO: 36h)",
            "disruption": "Severe Disruption",
            "disruption_penalty": -4,
            "complexity": "High",
            "customer_impact": "Severe Storefront Outage",
            "mitigation_likelihood": "High / Guaranteed",
            "mitigation_range": (0.75, 0.95),
            "mitigation_pct": 0.90,
            "desc": "Cut external routing to production clusters and re-image servers from verified off-site cold storage.",
            "technical_detail": "Restores guaranteed clean, tamper-free database snapshots and removes malicious wiper scripts.",
            "stock_outlook": "Severe short-term stock devaluation during total shutdown; restores fundamental enterprise valuation upon verified rebuild.",
            "reputation_risk": "Severe operational freeze sparks widespread frustration, but guarantees data integrity and prevents corrupt orders.",
            "exec_view": "IT proposes unplugging data centers for 36 hours to restore uncorrupted database snapshots."
        },
        {
            "id": "2",
            "label": "Restrict Database Traffic & Run Forensic Verification Scripts",
            "label_short": "Opt 2 (Forensic Audit)",
            "downtime": "8 Hours Partial Outage (RTO: 8h)",
            "disruption": "Moderate Disruption",
            "disruption_penalty": -2,
            "complexity": "Moderate",
            "customer_impact": "Noticeable Checkout Latency",
            "mitigation_likelihood": "Moderate / Contingent",
            "mitigation_range": (0.45, 0.70),
            "mitigation_pct": 0.60,
            "desc": "Freeze transaction replicas and run automated consistency scripts line-by-line.",
            "technical_detail": "Identifies high-level dropped tables, but subtle data tampering and logical corruption may remain unnoticed.",
            "stock_outlook": "Analysts maintain watchful wait-and-see rating; questions linger on inventory accuracy.",
            "reputation_risk": "Sporadic order glitches and checkout delays; moderate negative sentiment.",
            "exec_view": "IT proposes an 8-hour partial outage to audit and reconcile database tables."
        },
        {
            "id": "3",
            "label": "Live Read-Only Mode & Failsafe Integrity Logic",
            "label_short": "Opt 3 (Read-Only Mode)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption",
            "disruption_penalty": 0,
            "complexity": "Low",
            "customer_impact": "Minimal / Seamless",
            "mitigation_likelihood": "Low / Uncertain",
            "mitigation_range": (0.15, 0.35),
            "mitigation_pct": 0.25,
            "desc": "Switch database to read-only replica mode without interrupting catalog browsing.",
            "technical_detail": "Fails to purge attacker implants; corrupted transaction records continue causing cascading financial errors.",
            "stock_outlook": "Temporary stock stability, followed by sudden collapse if corrupted transaction logs cause restatements.",
            "reputation_risk": "Customers encounter phantom inventory and unfulfilled orders, causing widespread customer abandonment.",
            "exec_view": "IT proposes read-only browsing mode with zero customer store downtime."
        }
    ],
    (2, "C"): [  # Ransomware
        {
            "id": "1",
            "label": "Burn and Rebuild Bare-Metal from Clean Offline Golden Images",
            "label_short": "Opt 1 (Bare Metal Rebuild)",
            "downtime": "36 Hours Full Outage (RTO: 36h)",
            "disruption": "Severe Disruption",
            "disruption_penalty": -4,
            "complexity": "High",
            "customer_impact": "Severe Storefront Outage",
            "mitigation_likelihood": "High / Guaranteed",
            "mitigation_range": (0.75, 0.95),
            "mitigation_pct": 0.90,
            "desc": "Physically wipe encrypted domain controllers and re-image bare-metal servers from golden offline media.",
            "technical_detail": "Overcomes ransomware impact by completely expelling attacker encryption keys and root persistence.",
            "stock_outlook": "Sharp market dip during total rebuild; market rewards firm for refusing to fund criminal syndicates.",
            "reputation_risk": "Customers experience prolonged total blackout, but corporate reputation emerges resilient and fortified.",
            "exec_view": "IT proposes a 36-hour total shutdown to wipe and re-install all encrypted domain servers."
        },
        {
            "id": "2",
            "label": "Emergency Network Partition & Decryption Sandbox",
            "label_short": "Opt 2 (Network Partition)",
            "downtime": "8 Hours Partial Outage (RTO: 8h)",
            "disruption": "Moderate Disruption",
            "disruption_penalty": -2,
            "complexity": "Moderate",
            "customer_impact": "Noticeable Checkout Latency",
            "mitigation_likelihood": "Moderate / Contingent",
            "mitigation_range": (0.45, 0.70),
            "mitigation_pct": 0.60,
            "desc": "Partition compromised subnet zones and isolate encrypted volumes in forensic sandboxes.",
            "technical_detail": "Contains lateral encryption spread to isolated subnets, though secondary dormant payloads may still detonate.",
            "stock_outlook": "Market remains highly volatile; credit rating agencies place company on negative watch.",
            "reputation_risk": "Partial store functionality creates mixed customer signals; substantial social media anxiety.",
            "exec_view": "IT proposes an 8-hour network partition to quarantine encrypted subnet hosts."
        },
        {
            "id": "3",
            "label": "Keep Production Online & Pursue Back-Channel Key Negotiation",
            "label_short": "Opt 3 (Threat Bounty Negotiation)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption",
            "disruption_penalty": 0,
            "complexity": "Low",
            "customer_impact": "Minimal / Seamless",
            "mitigation_likelihood": "Low / Uncertain",
            "mitigation_range": (0.15, 0.35),
            "mitigation_pct": 0.25,
            "desc": "Attempt back-channel negotiations for decryption keys while keeping production storefronts online.",
            "technical_detail": "High risk of extortion failure; extorters routinely double-extort or provide non-functioning decryption tools.",
            "stock_outlook": "Short-term relief, but massive regulatory penalties and sanctions risk if illegal ransom is paid.",
            "reputation_risk": "Devastating brand betrayal if dark web leaks reveal corporate payouts to extortionists.",
            "exec_view": "IT proposes keeping servers active and pursuing digital decryption keys with zero downtime."
        }
    ],
    (3, "A"): [  # Supply Chain Logistics API Poisoning
        {
            "id": "1",
            "label": "Sever Supplier Feeds & Root Certificate Revocation",
            "label_short": "Opt 1 (Supplier Pipeline Sever)",
            "downtime": "48 Hours Integration Halt (RTO: 48h)",
            "disruption": "Severe Disruption",
            "disruption_penalty": -4,
            "complexity": "High",
            "customer_impact": "Severe Order Halt",
            "mitigation_likelihood": "High / Guaranteed",
            "mitigation_range": (0.75, 0.95),
            "mitigation_pct": 0.90,
            "desc": "Disconnect all external vendor and supplier integration pipelines and rotate root cryptographic certificates.",
            "technical_detail": "Completely purges downstream supply-chain infection vectors and revokes untrusted partner credentials.",
            "stock_outlook": "Significant operational supply disruption; analysts praise rigorous root-cause remediation.",
            "reputation_risk": "Delayed fulfillment generates negative reviews, but prevents catastrophic partner-wide compromise.",
            "exec_view": "IT proposes severing all third-party vendor and supplier feeds for 48 hours, halting order fulfillment."
        },
        {
            "id": "2",
            "label": "Edge CDN Scrubbing & Rate Limiting",
            "label_short": "Opt 2 (Edge Scrubbing)",
            "downtime": "10 Hours Slowdown (RTO: 10h)",
            "disruption": "Moderate Disruption",
            "disruption_penalty": -2,
            "complexity": "Moderate",
            "customer_impact": "Noticeable Checkout Latency",
            "mitigation_likelihood": "Moderate / Contingent",
            "mitigation_range": (0.45, 0.70),
            "mitigation_pct": 0.60,
            "desc": "Re-route external partner traffic through edge filtering inspection with strict behavioral limits.",
            "technical_detail": "Mitigates external traffic floods, but compromised legitimate credentials may still pass behavioral filters.",
            "stock_outlook": "Market remains cautious as fulfillment velocity slows down.",
            "reputation_risk": "Moderate consumer friction from checkout latency, but containment limits data loss.",
            "exec_view": "IT proposes an edge scrubbing filter slowing checkout traffic for 10 hours."
        },
        {
            "id": "3",
            "label": "Maintain Partner Traffic & Rely on Vendor Warranties",
            "label_short": "Opt 3 (Passive Monitoring)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption",
            "disruption_penalty": 0,
            "complexity": "Low",
            "customer_impact": "Minimal / Seamless",
            "mitigation_likelihood": "Low / Uncertain",
            "mitigation_range": (0.15, 0.35),
            "mitigation_pct": 0.25,
            "desc": "Avoid penalizing supplier relationships by accepting external vendor self-attestation reports.",
            "technical_detail": "Leaves known compromised partner routes connected; attackers continue to inject poisoned updates.",
            "stock_outlook": "Short-term revenue holds, but catastrophic liability if downstream customer networks are breached.",
            "reputation_risk": "Zero initial disruption, but devastating loss of enterprise partner trust if breaches spread.",
            "exec_view": "IT proposes maintaining normal partner feeds with zero operational downtime."
        }
    ],
    (3, "B"): [  # Volumetric DDoS Smokescreen & API Wipe
        {
            "id": "1",
            "label": "Emergency BGP Anycast Routing & Scrubbing Center Divert",
            "label_short": "Opt 1 (BGP Anycast Divert)",
            "downtime": "24 Hours Scrubbing Reroute (RTO: 24h)",
            "disruption": "Severe Disruption",
            "disruption_penalty": -4,
            "complexity": "High",
            "customer_impact": "High Checkout Latency & CAPTCHAs",
            "mitigation_likelihood": "High / Guaranteed",
            "mitigation_range": (0.75, 0.95),
            "mitigation_pct": 0.90,
            "desc": "Reroute all incoming traffic through global upstream DDoS scrubbing centers and inspect API calls for hidden wiper scripts.",
            "technical_detail": "Filters volumetric flood while deep packet inspection identifies and isolates covert background database wiper payloads.",
            "stock_outlook": "Temporary stock dip during traffic scrubbing; market applauds protection of core asset records.",
            "reputation_risk": "Customers encounter aggressive verification challenges, but enterprise data integrity remains uncompromised.",
            "exec_view": "IT proposes rerouting all network traffic to external scrubbing centers for 24 hours to uncover hidden wiper payloads."
        },
        {
            "id": "2",
            "label": "Edge CDN Rate Limiting & Geo-Blocking",
            "label_short": "Opt 2 (Geo-Blocking)",
            "downtime": "8 Hours Partial Throttling (RTO: 8h)",
            "disruption": "Moderate Disruption",
            "disruption_penalty": -2,
            "complexity": "Moderate",
            "customer_impact": "Noticeable Checkout Friction",
            "mitigation_likelihood": "Moderate / Contingent",
            "mitigation_range": (0.45, 0.70),
            "mitigation_pct": 0.60,
            "desc": "Apply aggressive edge rate-limits and block traffic originating from high-risk foreign autonomous systems.",
            "technical_detail": "Suppresses public-facing traffic spikes, but domestic botnets and stealthy API calls may bypass geographic filters.",
            "stock_outlook": "Equities market fluctuates as localized customer segments report connectivity drops.",
            "reputation_risk": "Blocked international customers voice frustration, but domestic transactions continue.",
            "exec_view": "IT proposes edge rate-limiting and geo-blocking for 8 hours to throttle attack volume."
        },
        {
            "id": "3",
            "label": "Upstream ISP Null-Routing (Blackholing)",
            "label_short": "Opt 3 (Passive Blackholing)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption",
            "disruption_penalty": 0,
            "complexity": "Low",
            "customer_impact": "Minimal / Seamless",
            "mitigation_likelihood": "Low / Uncertain",
            "mitigation_range": (0.15, 0.35),
            "mitigation_pct": 0.25,
            "desc": "Rely on standard ISP upstream blackholing of targeted IPs without dedicated scrubbing infrastructure.",
            "technical_detail": "Legitimate customers are dropped alongside attack floods, while adversaries' stealth wiper scripts execute uninterrupted.",
            "stock_outlook": "Avoids active downtime costs, but invites crippling stock drop when uncontained backend data loss surfaces.",
            "reputation_risk": "False sense of normalcy broken when customers discover unfulfilled orders and wiped account history.",
            "exec_view": "IT proposes passive ISP blackholing with zero system downtime or active mitigation."
        }
    ],
    (3, "C"): [  # APT Deep Persistence & UEFI Rootkits
        {
            "id": "1",
            "label": "Full Hardware Scuttle & Cloud Migration",
            "label_short": "Opt 1 (Hardware Scuttle)",
            "downtime": "5-7 Days Cluster Rebuild (RTO: 120h)",
            "disruption": "Severe Disruption",
            "disruption_penalty": -4,
            "complexity": "High",
            "customer_impact": "Major Operational Upheaval",
            "mitigation_likelihood": "High / Guaranteed",
            "mitigation_range": (0.75, 0.95),
            "mitigation_pct": 0.90,
            "desc": "Decommission and air-gap all compromised bare-metal server nodes, rebuilding enterprise operations in fresh cloud infrastructure.",
            "technical_detail": "Physically severs motherboard SPI flash implants and BMC rootkits by completely replacing physical execution environments.",
            "stock_outlook": "Substantial short-term capital expenditure and stock slump; long-term resilience rewarded by enterprise clients.",
            "reputation_risk": "Severe operational slowdown, but guarantees the company is 100% purged of foreign state implants.",
            "exec_view": "IT proposes decommissioning infected physical server racks and migrating to verified cloud instances (5-7 day rebuild)."
        },
        {
            "id": "2",
            "label": "Hardware SPI Reflashing & Secure Boot Audit",
            "label_short": "Opt 2 (SPI Reflashing)",
            "downtime": "48-72 Hours Maintenance (RTO: 48h)",
            "disruption": "Moderate Disruption",
            "disruption_penalty": -2,
            "complexity": "Moderate",
            "customer_impact": "Extended Maintenance Outage",
            "mitigation_likelihood": "Moderate / Contingent",
            "mitigation_range": (0.45, 0.70),
            "mitigation_pct": 0.60,
            "desc": "Flash firmware chips with vendor cryptographic golden images and enforce hardware-level Secure Boot signatures.",
            "technical_detail": "Overwrites malicious UEFI firmware, but sophisticated memory-resident implants or altered boot ROMs may resist flashing.",
            "stock_outlook": "Market remains cautious pending confirmation that persistent implants have been neutralized.",
            "reputation_risk": "Customers tolerate maintenance window, but brand remains under shadow of lingering rootkit risk.",
            "exec_view": "IT proposes a 48-hour maintenance window to manually reflash hardware motherboard firmware."
        },
        {
            "id": "3",
            "label": "Outbound Network Egress Blockade & Sinkholing",
            "label_short": "Opt 3 (Passive Monitoring)",
            "downtime": "0 Hours (Zero Downtime)",
            "disruption": "Zero Disruption",
            "disruption_penalty": 0,
            "complexity": "Low",
            "customer_impact": "Minimal / Seamless",
            "mitigation_likelihood": "Low / Uncertain",
            "mitigation_range": (0.15, 0.35),
            "mitigation_pct": 0.25,
            "desc": "Apply aggressive firewall rules to block known C2 egress IPs while leaving physical servers running.",
            "technical_detail": "Firmware implants remain fully entrenched in hardware; attackers pivot to secondary fallback channels or wait out temporary blocks.",
            "stock_outlook": "Avoids massive hardware write-downs today, but risks complete insolvency if rootkits auction intellectual property.",
            "reputation_risk": "Customers unaware initially, but complete catastrophe if motherboard implants leak private customer records.",
            "exec_view": "IT proposes software egress firewall rules with zero hardware downtime or server replacement."
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

def get_exec_governance_options(it_choice: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Returns contextualized Executive Governance directives tailored to the specific IT recommendation.
    Enforces the uniform triad: 'Agree with IT', 'Compromise', and 'Override IT'.
    """
    if not it_choice:
        return EXEC_GOVERNANCE_OPTIONS

    opt_id = str(it_choice.get("id", "1"))
    it_label = it_choice.get("label", "IT Technical Plan")
    it_short = it_choice.get("label_short", it_label)
    downtime = it_choice.get("downtime", "operational downtime")
    customer_impact = it_choice.get("customer_impact", "customer impact")
    disruption = it_choice.get("disruption", "operational disruption")

    if opt_id == "1":
        # Aggressive, safest, highest downtime/disruption
        agree_desc = (
            f"Authorize IT's full containment directive ({it_short}). Accept {downtime} and {disruption} "
            f"to guarantee maximum threat containment, protect customer data, and prevent regulatory fines."
        )
        comp_desc = (
            f"Direct IT to cut {downtime} in half. Push IT to restore customer storefronts faster, "
            f"accepting 50% threat mitigation and leaving secondary channels exposed."
        )
        override_desc = (
            f"Reject IT's shutdown directive completely. Keep all systems online to avoid revenue loss. "
            f"Provides 0% mitigation and triggers an Executive Override penalty (+10% to +35% damage multiplier) for ignoring IT security counsel."
        )
    elif opt_id == "2":
        # Targeted isolation, moderate disruption
        agree_desc = (
            f"Authorize IT's targeted quarantine directive ({it_short}). Accept {downtime} and {customer_impact} "
            f"to balance threat containment with business continuity."
        )
        comp_desc = (
            f"Expedite IT's targeted quarantine. Instruct IT to reconnect systems after minimal testing, "
            f"halving threat mitigation to protect immediate quarterly revenue."
        )
        override_desc = (
            f"Reject targeted isolations completely to maintain normal business-as-usual operations. "
            f"Provides 0% mitigation and triggers an Executive Override penalty (+10% to +35% damage multiplier) for ignoring IT security counsel."
        )
    else:
        # Passive monitoring / zero downtime (Option 3)
        agree_desc = (
            f"Endorse IT's passive monitoring strategy ({it_short}). Maintain zero downtime and uninterrupted revenue, "
            f"accepting the severe risk that uncontained adversary activity backfires (+5% to +25% damage multiplier)."
        )
        comp_desc = (
            f"Request limited security safeguards while keeping operations running. "
            f"Provides minimal defensive containment (halving the already low mitigation)."
        )
        override_desc = (
            f"Overrule IT's passive approach to enforce zero security intervention or logging. "
            f"Provides 0% mitigation and triggers an Executive Override penalty (+10% to +35% damage multiplier)."
        )

    return [
        {
            "id": "approve",
            "action": "approve",
            "label": "✅ Agree with IT",
            "label_short": "Agree with IT",
            "tagline": f"Authorize: {it_short}",
            "desc": agree_desc
        },
        {
            "id": "downgrade",
            "action": "downgrade",
            "label": "⚖️ Compromise",
            "label_short": "Compromise",
            "tagline": "Halve Operational Downtime & Mitigation",
            "desc": comp_desc
        },
        {
            "id": "overrule",
            "action": "overrule",
            "label": "🚫 Override IT",
            "label_short": "Override IT",
            "tagline": "Enforce Business Continuity (0% Mitigation)",
            "desc": override_desc
        }
    ]

# Executive Governance Directives (Fallback / Baseline)
EXEC_GOVERNANCE_OPTIONS = [
    {
        "id": "approve",
        "action": "approve",
        "label": "✅ Agree with IT",
        "label_short": "Agree with IT",
        "tagline": "Prioritize Long-Term Security & Brand Trust",
        "desc": "Accept operational downtime and immediate stock dip to guarantee threat containment, protect customer PII, and prevent regulatory fines."
    },
    {
        "id": "downgrade",
        "action": "downgrade",
        "label": "⚖️ Compromise",
        "label_short": "Compromise",
        "tagline": "Balance Quarterly Revenue with Threat Control",
        "desc": "Order IT to cut downtime in half to keep primary storefronts operating. Preserves sales channels but leaves secondary vulnerabilities open to continued exploitation."
    },
    {
        "id": "overrule",
        "action": "overrule",
        "label": "🚫 Override IT",
        "label_short": "Override IT",
        "tagline": "Prioritize Immediate Earnings Guidance & Market Valuation",
        "desc": "Reject system shutdowns to maintain uninterrupted sales and prevent investor panic. Leaves networks vulnerable to catastrophic lateral movement and severe legal exposure."
    }
]

# Media Headlines by Round (4 Tiers: Sensationalist, Critical, Balanced, Favorable)
DYNAMIC_HEADLINES = {
    1: [
        {"id": "Headline 1", "label": "Sensationalist Front-Page", "tier": "Sensationalist", "disposition": "Negative", "headline": "💥 CloudStore in Freefall: Catastrophic Infiltration Exposed!", "health_delta": -12, "health_delta_range": (-15, -4), "desc": "Sensationalized panic coverage driving volatile market reactions."},
        {"id": "Headline 2", "label": "Critical Investigative Report", "tier": "Critical", "disposition": "Negative", "headline": "⚠️ CloudStore Breached: Security Lapses Spark Customer Alarm", "health_delta": -5, "health_delta_range": (-9, -2), "desc": "Investigative scrutiny highlighting internal cyber hygiene and compliance concerns."},
        {"id": "Headline 3", "label": "Balanced Industry Coverage", "tier": "Balanced", "disposition": "Neutral", "headline": "📰 CloudStore Investigates Security Anomaly: Systems Monitored", "health_delta": 2, "health_delta_range": (-3, 4), "desc": "Measured reporting noting ongoing incident response with uncertain audience reach."},
        {"id": "Headline 4", "label": "Favorable Public Commendation", "tier": "Favorable", "disposition": "Positive", "headline": "🛡️ Decisive Defense: CloudStore Thwarts Infiltration Attempt", "health_delta": 8, "health_delta_range": (1, 12), "desc": "Commendatory press praising rapid corporate response, subject to public interest."}
    ],
    2: [
        {"id": "Headline 1", "label": "Sensationalist Front-Page", "tier": "Sensationalist", "disposition": "Negative", "headline": "💥 Total Blackout: Extortionists Hold CloudStore Hostage!", "health_delta": -12, "health_delta_range": (-15, -4), "desc": "Front-page headlines stoking widespread public panic and market turmoil."},
        {"id": "Headline 2", "label": "Critical Investigative Report", "tier": "Critical", "disposition": "Negative", "headline": "⚠️ Millions at Risk: CloudStore Stumbles as Breach Deepens", "health_delta": -5, "health_delta_range": (-9, -2), "desc": "Journalistic scrutiny over executive delays and customer data vulnerability."},
        {"id": "Headline 3", "label": "Balanced Industry Coverage", "tier": "Balanced", "disposition": "Neutral", "headline": "📰 CloudStore Executes Incident Response Amid System Strains", "health_delta": 2, "health_delta_range": (-3, 4), "desc": "Factual reporting on containment protocols and corporate operational resilience."},
        {"id": "Headline 4", "label": "Favorable Public Commendation", "tier": "Favorable", "disposition": "Positive", "headline": "🛡️ Customer First: CloudStore Shields Data with Strong Protocols", "health_delta": 8, "health_delta_range": (1, 12), "desc": "Positive media narrative highlighting customer transparency and data defense."}
    ],
    3: [
        {"id": "Headline 1", "label": "Sensationalist Front-Page", "tier": "Sensationalist", "disposition": "Negative", "headline": "💥 Insolvency Looming? CloudStore Collapses Under Cyber Blitz", "health_delta": -12, "health_delta_range": (-15, -4), "desc": "Aggressive market commentary questioning enterprise solvency and continuity."},
        {"id": "Headline 2", "label": "Critical Investigative Report", "tier": "Critical", "disposition": "Negative", "headline": "⚠️ Regulatory Inquiries Launched Against CloudStore Leadership", "health_delta": -5, "health_delta_range": (-9, -2), "desc": "Critical press focus on regulatory sanctions and compliance enforcement."},
        {"id": "Headline 3", "label": "Balanced Industry Coverage", "tier": "Balanced", "disposition": "Neutral", "headline": "📰 CloudStore Concludes Containment Phase; Audits Continue", "health_delta": 2, "health_delta_range": (-3, 4), "desc": "Balanced assessment of long-term recovery prospects and forensic audits."},
        {"id": "Headline 4", "label": "Favorable Public Commendation", "tier": "Favorable", "disposition": "Positive", "headline": "🛡️ Masterclass in Crisis Leadership: CloudStore Prevails", "health_delta": 8, "health_delta_range": (1, 12), "desc": "Glowing review praising the organization's crisis leadership turnaround."}
    ]
}

# ---------------------------------------------------------
# BACKWARD COMPATIBILITY ALIASES
# (Guarantees zero crashes if legacy callers or cached workers access old attributes)
# ---------------------------------------------------------
hacker_options = [
    {
        "id": "H1",
        "name": "Phishing Campaign",
        "description": "This action involves sending fake emails to employees to trick them into giving away their passwords.",
        "assessment": "High likelihood of success, immediate damage usually limited to compromised accounts.",
        "complexity": "Low",
        "projected_impact": -10
    },
    {
        "id": "H2",
        "name": "DDoS Attack",
        "description": "Overwhelms website with fake traffic so real customers cannot access it.",
        "assessment": "Causes temporary financial loss and reputation damage while site is down.",
        "complexity": "Medium",
        "projected_impact": -20
    },
    {
        "id": "H3",
        "name": "Ransomware Deployment",
        "description": "Uses malicious software to lock up company files until a ransom is paid.",
        "assessment": "Severe damage halting business operations if successful.",
        "complexity": "High",
        "projected_impact": -35
    }
]

it_options = [
    {
        "id": "IT1",
        "name": "Isolate Affected Systems",
        "description": "Disconnects infected computers from the network.",
        "assessment": "Quickly stops spread, but isolated departments cannot work.",
        "complexity": "Low",
        "projected_impact": 10
    },
    {
        "id": "IT2",
        "name": "Restore from Backups",
        "description": "Wipes infected computers and restores safe older copy.",
        "assessment": "Removes attacker without paying, but recent unsaved work lost.",
        "complexity": "Medium",
        "projected_impact": 20
    },
    {
        "id": "IT3",
        "name": "Deploy Advanced Threat Hunting",
        "description": "Security experts actively hunt for persistent hidden attackers.",
        "assessment": "Thorough network security, but expensive and time-consuming.",
        "complexity": "High",
        "projected_impact": 35
    }
]

exec_options = [
    {
        "id": "E1",
        "name": "Public Apology and Transparency",
        "description": "Public statement explaining the breach and apologizing.",
        "assessment": "Builds long-term trust, but invites immediate press scrutiny.",
        "complexity": "Low",
        "projected_impact": 10
    },
    {
        "id": "E2",
        "name": "Hire External PR and Legal Firm",
        "description": "Outside crisis experts handle media and legal exposure.",
        "assessment": "Minimizes reputation fallout at high budgetary expense.",
        "complexity": "Medium",
        "projected_impact": 20
    },
    {
        "id": "E3",
        "name": "Negotiate and Pay Ransom",
        "description": "Secretly pay attackers hoping for decryptor and data deletion.",
        "assessment": "Fast recovery attempt, but risks repeat extortion and bad faith.",
        "complexity": "High",
        "projected_impact": 35
    }
]

