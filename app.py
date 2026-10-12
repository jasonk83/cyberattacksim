"""
CloudStore Command: Mission Control
Multiplayer Cyber Incident Response Simulation
Streamlit Application
"""

import streamlit as st
import time
import copy
from typing import Dict, Any, Optional, List, Tuple

# ---------------------------------------------------------
# DEFAULT ASSETS & FALLBACKS (Guarantees zero crashes if modules differ)
# ---------------------------------------------------------
DEFAULT_TEAM_CODES = {
    "main": "admin123",       # Instructor / Mission Control
    "hackers": "hacker123",   # Threat Actor Terminal
    "it": "tech123",          # IT Defense Command
    "exec": "board123",       # Executive Board
    "media": "press123"       # Media & PR Scrum
}

DEFAULT_ATTACKS = {
    1: {
        "A": {
            "name": "Phishing & Credential Harvest",
            "icon": "🎣",
            "description": "CFO assistant credentials harvested via spoofed 'Urgent Invoice' email.",
            "base_impact": {"Trust": -5, "Fiscal": -2, "Op-Eff": -5},
            "hacker_score": 15
        },
        "B": {
            "name": "Unpatched Web Server Exploit",
            "icon": "🛠️",
            "description": "Known CVE vulnerability exploited on public web server for backdoor access.",
            "base_impact": {"Trust": -5, "Fiscal": -3, "Op-Eff": -10},
            "hacker_score": 20
        }
    },
    2: {
        "A": {
            "name": "Ransomware Encryption",
            "icon": "💀",
            "description": "Production database encrypted. $5M ransom demanded. Storefront offline.",
            "base_impact": {"Trust": -15, "Fiscal": -10, "Op-Eff": -25},
            "hacker_score": 35
        },
        "B": {
            "name": "Mass Customer Data Exfiltration",
            "icon": "🕵️",
            "description": "2 Million customer payment cards and PII exfiltrated and posted for sale.",
            "base_impact": {"Trust": -25, "Fiscal": -15, "Op-Eff": -10},
            "hacker_score": 40
        }
    },
    3: {
        "A": {
            "name": "Supply Chain & Partner Pivot",
            "icon": "🔗",
            "description": "Compromised third-party logistics vendor used to poison inventory feeds.",
            "base_impact": {"Trust": -15, "Fiscal": -12, "Op-Eff": -18},
            "hacker_score": 30
        },
        "B": {
            "name": "DDoS & Infrastructure Sabotage",
            "icon": "💥",
            "description": "High-volume distributed denial-of-service combined with cloud API wipe.",
            "base_impact": {"Trust": -10, "Fiscal": -8, "Op-Eff": -30},
            "hacker_score": 30
        }
    }
}

DEFAULT_IT_CHOICES = {
    1: {
        "A": [
            {"id": "1", "label": "Full Credential Reset & MFA Enforcement", "desc": "Revoke all finance session tokens, force hardware MFA, isolate finance subnet.", "fiscal": -3, "opeff": -8, "trust": +5, "score": 25},
            {"id": "2", "label": "Targeted Account Isolation & Monitoring", "desc": "Lock director account, enable enhanced logging, trace lateral movement.", "fiscal": -1, "opeff": -3, "trust": +2, "score": 20},
            {"id": "3", "label": "Engage External Forensics Retainer", "desc": "Call third-party IR firm; pause containment until preliminary audit arrives.", "fiscal": -8, "opeff": 0, "trust": 0, "score": 12},
            {"id": "4", "label": "Company-wide Phishing Reminder Notice", "desc": "Send staff warning email about suspicious links; no credentials revoked.", "fiscal": 0, "opeff": -12, "trust": -8, "score": 5},
            {"id": "5", "label": "Dismiss Alert & Instruct User Reboot", "desc": "Treat as false positive; instruct employee to reboot workstation.", "fiscal": -10, "opeff": -25, "trust": -15, "score": 0}
        ],
        "B": [
            {"id": "1", "label": "Emergency Web Server Hotfix & Isolation", "desc": "Take vulnerable web node offline, deploy vendor patch, inspect ingress logs.", "fiscal": -2, "opeff": -6, "trust": +5, "score": 25},
            {"id": "2", "label": "WAF Virtual Patching & Geo-blocking", "desc": "Enable emergency firewall rules and block suspicious IP subnets.", "fiscal": -1, "opeff": -2, "trust": +2, "score": 20},
            {"id": "3", "label": "Deep Vulnerability Scan Before Patching", "desc": "Run full environment audit to find other flaws before taking server down.", "fiscal": -5, "opeff": 0, "trust": -2, "score": 12},
            {"id": "4", "label": "Throttle Traffic & Monitor Bandwidth", "desc": "Rate-limit incoming connections; postpone patching until maintenance window.", "fiscal": 0, "opeff": -15, "trust": -10, "score": 5},
            {"id": "5", "label": "Ignore Exploit Warning", "desc": "Rely on standard antivirus; take no action.", "fiscal": -12, "opeff": -30, "trust": -20, "score": 0}
        ]
    },
    2: {
        "A": [
            {"id": "1", "label": "Refuse Ransom & Restore Clean Backups", "desc": "Sever infected networks, report to FBI, restore cold-storage verified backups.", "fiscal": -12, "opeff": -15, "trust": +10, "score": 30},
            {"id": "2", "label": "Negotiate for Time While Isolating Nodes", "desc": "Engage incident negotiator to delay attackers while IT tracks decryptor tools.", "fiscal": -15, "opeff": -10, "trust": +2, "score": 22},
            {"id": "3", "label": "Pay $5M Ransom for Immediate Key", "desc": "Pay demand from emergency reserves to expedite storefront recovery.", "fiscal": -35, "opeff": -5, "trust": -8, "score": 15},
            {"id": "4", "label": "Internal Reverse-Hack Attempt", "desc": "Attempt offensive counter-strike to retrieve keys without off-site backups.", "fiscal": -25, "opeff": -40, "trust": -20, "score": 5},
            {"id": "5", "label": "Disguise as Scheduled Maintenance", "desc": "Conceal ransomware breach from staff and public; claim cloud upgrade.", "fiscal": -50, "opeff": -50, "trust": -40, "score": 0}
        ],
        "B": [
            {"id": "1", "label": "Rotate All Keys, Invalidate Tokens & Notify Regulators", "desc": "Revoke API access, contact FTC/SEC, offer credit monitoring immediately.", "fiscal": -10, "opeff": -10, "trust": +10, "score": 30},
            {"id": "2", "label": "Targeted Token Rotation & Quiet User Notice", "desc": "Reset affected cardholder credentials; inform affected users directly.", "fiscal": -8, "opeff": -6, "trust": +4, "score": 22},
            {"id": "3", "label": "Pay Extortion to Delete Stolen Records", "desc": "Pay threat actors for promise of data destruction.", "fiscal": -30, "opeff": -4, "trust": -10, "score": 15},
            {"id": "4", "label": "Internal Legal Gag Order", "desc": "Suppress breach disclosure internally while investigating.", "fiscal": -20, "opeff": -15, "trust": -25, "score": 5},
            {"id": "5", "label": "Deny Any Breach Occurred", "desc": "Issue press denial despite proof on dark web forums.", "fiscal": -45, "opeff": -25, "trust": -50, "score": 0}
        ]
    },
    3: {
        "A": [
            {"id": "1", "label": "Sever Partner API Integrations & Audit Feeds", "desc": "Cut external supplier pipelines, rebuild trusted inventory sync from scratch.", "fiscal": -10, "opeff": -12, "trust": +8, "score": 25},
            {"id": "2", "label": "Quarantine Tainted Inventory SKU Records", "desc": "Flag suspect items, limit automated purchases, verify partner certs.", "fiscal": -5, "opeff": -6, "trust": +4, "score": 20},
            {"id": "3", "label": "Rely on Partner's Security Assurance", "desc": "Continue transactions while waiting on supplier's self-assessment report.", "fiscal": -15, "opeff": -15, "trust": -10, "score": 8},
            {"id": "4", "label": "Bypass Vendor Safeguards to Maintain Sales", "desc": "Ignore feed anomalies to preserve Black Friday checkout volume.", "fiscal": -30, "opeff": -35, "trust": -25, "score": 0}
        ],
        "B": [
            {"id": "1", "label": "Activate Disaster Recovery Cloud Failover", "desc": "Spin up warm reserve infrastructure in secondary region; scrub traffic.", "fiscal": -10, "opeff": -10, "trust": +8, "score": 25},
            {"id": "2", "label": "Deploy Edge CDN Scrubbing & Rate Limiting", "desc": "Route ingress through DDoS mitigation scrubbing centers.", "fiscal": -6, "opeff": -5, "trust": +4, "score": 20},
            {"id": "3", "label": "Attempt Manual Load-Balancing Reconfig", "desc": "Internal engineering re-routes traffic on existing hardware without failover.", "fiscal": -15, "opeff": -25, "trust": -10, "score": 8},
            {"id": "4", "label": "Shut Down All Web Services Completely", "desc": "Unplug public routing until traffic subsides.", "fiscal": -35, "opeff": -45, "trust": -30, "score": 0}
        ]
    }
}

DEFAULT_EXEC_CHOICES = {
    1: [
        {"id": "1", "label": "Full Transparency: Notify Board & Regulators Early", "desc": "Proactive transparency; authorize incident budget immediately.", "fiscal": -5, "opeff": 0, "trust": +8, "score": 25},
        {"id": "2", "label": "Cautious Containment: Brief Executive Committee", "desc": "Limit briefings to C-Suite; approve selective emergency budget.", "fiscal": -2, "opeff": 0, "trust": +3, "score": 20},
        {"id": "3", "label": "Wait-and-See: Require Definite Breach Evidence", "desc": "Withhold resources until IT proves financial data was touched.", "fiscal": 0, "opeff": -5, "trust": -5, "score": 10},
        {"id": "4", "label": "Silence IT: Protect Upcoming Quarterly Earnings", "desc": "Instruct leadership to suppress security chatter to protect stock valuation.", "fiscal": +2, "opeff": -10, "trust": -18, "score": 0}
    ],
    2: [
        {"id": "1", "label": "Customer-First Stand: Waive Fees, Open Hotline", "desc": "Establish 24/7 call center, offer identity protection, CEO video address.", "fiscal": -15, "opeff": -5, "trust": +15, "score": 30},
        {"id": "2", "label": "Balanced Response: Standard Disclosure & Advisory", "desc": "Issue formal breach notice with standard customer security advice.", "fiscal": -5, "opeff": -2, "trust": +5, "score": 20},
        {"id": "3", "label": "Legal Shield: Deflect Liability to Vendors & Users", "desc": "Frame breach as third-party failure; enforce terms of service disclaimers.", "fiscal": -2, "opeff": 0, "trust": -15, "score": 10},
        {"id": "4", "label": "Aggressive Cover-Up: Threaten Leakers with NDAs", "desc": "Enforce strict media blackout and threaten whistleblowers.", "fiscal": -10, "opeff": -15, "trust": -35, "score": 0}
    ],
    3: [
        {"id": "1", "label": "Comprehensive Restructure & Independent Security Audit", "desc": "Commit $10M to overhaul cyber posture; publish third-party audit findings.", "fiscal": -15, "opeff": -5, "trust": +15, "score": 25},
        {"id": "2", "label": "Executive Overhaul & Rebranded Security Program", "desc": "Replace CISO, appoint chief risk officer, announce zero-trust initiative.", "fiscal": -8, "opeff": 0, "trust": +8, "score": 18},
        {"id": "3", "label": "Minimum Compliance Fixes", "desc": "Do only what regulators mandate; avoid major capital expenditures.", "fiscal": -2, "opeff": -5, "trust": -8, "score": 8},
        {"id": "4", "label": "Scapegoat IT Team & Avoid System Investment", "desc": "Fire mid-level engineers; declare problem resolved without funding upgrades.", "fiscal": 0, "opeff": -20, "trust": -25, "score": 0}
    ]
}

DEFAULT_DYNAMIC_HEADLINES = [
    {"headline": "CloudStore Thwarts Cyber-Heist with Speed & Integrity", "trust_delta": +10, "tier": "Exceptional"},
    {"headline": "Security First: CloudStore Isolates Threat Rapidly", "trust_delta": +5, "tier": "Favorable"},
    {"headline": "Business as Usual: CloudStore Audits Ongoing Systems", "trust_delta": 0, "tier": "Neutral"},
    {"headline": "Overreaction or Breach? CloudStore Executives Send Mixed Signals", "trust_delta": -5, "tier": "Critical"},
    {"headline": "Executive Panic: Leadership Blunders Leave Millions Vulnerable", "trust_delta": -10, "tier": "Catastrophic"}
]

def default_calculate_round_impact(attack, it_choice, exec_choice, media_headline=None, multiplier=1.0):
    base_f = attack.get("base_impact", {}).get("Fiscal", 0) * multiplier
    base_t = attack.get("base_impact", {}).get("Trust", 0)
    base_o = attack.get("base_impact", {}).get("Op-Eff", 0) * multiplier

    it_f = it_choice.get("fiscal", it_choice.get("stock", 0)) * multiplier
    it_t = it_choice.get("trust", it_choice.get("nps", 0))
    it_o = it_choice.get("opeff", it_choice.get("rto", 0)) * multiplier
    it_points = it_choice.get("score", 20)

    ex_f = exec_choice.get("fiscal", 0) * multiplier
    ex_t = exec_choice.get("trust", 0)
    ex_o = exec_choice.get("opeff", 0) * multiplier
    ex_points = exec_choice.get("score", 20)

    media_trust = 0
    media_points = 10
    if media_headline:
        if isinstance(media_headline, dict):
            media_trust = media_headline.get("trust_delta", media_headline.get("trust", 0))
        elif isinstance(media_headline, (int, float)):
            media_trust = media_headline
        media_points = 20 if abs(media_trust) >= 5 else 10

    hacker_points = int(attack.get("hacker_score", 25) * multiplier)
    if str(it_choice.get("id")) == "1" and str(exec_choice.get("id")) == "1":
        hacker_points = max(5, hacker_points - 15)

    return {
        "deltas": {
            "Fiscal": round(base_f + it_f + ex_f, 1),
            "Trust": round(base_t + it_t + ex_t + media_trust, 1),
            "Op-Eff": round(base_o + it_o + ex_o, 1)
        },
        "team_scorecard": {
            "IT": it_points,
            "Exec": ex_points,
            "Media": media_points,
            "Hacker": hacker_points
        }
    }

# ---------------------------------------------------------
# ROBUST DYNAMIC MODULE INSPECTION & IMPORT
# ---------------------------------------------------------
def safe_resolve_attribute(module, candidate_names: List[str], default_value: Any) -> Tuple[Any, bool]:
    if module is None:
        return default_value, False

    for name in candidate_names:
        if hasattr(module, name):
            val = getattr(module, name)
            if val is not None:
                return val, True

    for attr in dir(module):
        try:
            obj = getattr(module, attr)
            if isinstance(obj, type):
                for name in candidate_names:
                    if hasattr(obj, name):
                        val = getattr(obj, name)
                        if val is not None:
                            return val, True
        except Exception:
            pass

    return default_value, False

try:
    import game_data as _gd_mod
except Exception:
    _gd_mod = None

try:
    import scoring_engine as _se_mod
except Exception:
    _se_mod = None

TEAM_CODES, _found_codes = safe_resolve_attribute(
    _gd_mod,
    ["TEAM_CODES", "team_codes", "PASSCODES", "passcodes", "CODES", "codes", "ROLES", "roles", "PASSWORDS"],
    DEFAULT_TEAM_CODES
)

ATTACKS, _found_attacks = safe_resolve_attribute(
    _gd_mod,
    ["ATTACKS", "attacks", "SCENARIOS", "scenarios", "ATTACK_SCENARIOS", "attack_scenarios"],
    DEFAULT_ATTACKS
)

IT_CHOICES, _found_it = safe_resolve_attribute(
    _gd_mod,
    ["IT_CHOICES", "it_choices", "IT_OPTIONS", "it_options", "TECH_CHOICES", "tech_choices", "TECH_DATA", "tech_data"],
    DEFAULT_IT_CHOICES
)

EXEC_CHOICES, _found_exec = safe_resolve_attribute(
    _gd_mod,
    ["EXEC_CHOICES", "exec_choices", "EXEC_OPTIONS", "exec_options", "EXECUTIVE_CHOICES", "executive_choices", "BOARD_CHOICES"],
    DEFAULT_EXEC_CHOICES
)

DYNAMIC_HEADLINES, _found_headlines = safe_resolve_attribute(
    _gd_mod,
    ["DYNAMIC_HEADLINES", "dynamic_headlines", "HEADLINES", "headlines", "MEDIA_HEADLINES", "media_headlines", "MEDIA_DATA", "media_data"],
    DEFAULT_DYNAMIC_HEADLINES
)

calculate_round_impact, _found_scoring = safe_resolve_attribute(
    _se_mod,
    ["calculate_round_impact", "calculate_impact", "score_round", "evaluate_round"],
    default_calculate_round_impact
)

def normalize_options_list(raw_options) -> List[Dict[str, Any]]:
    normalized = []
    if isinstance(raw_options, dict):
        for k, v in raw_options.items():
            if isinstance(v, dict):
                item = copy.copy(v)
                item["id"] = str(item.get("id", k))
                item["label"] = str(item.get("label", item.get("txt", item.get("name", f"Option {k}"))))
                item["desc"] = str(item.get("desc", item.get("description", "")))
                normalized.append(item)
            else:
                normalized.append({"id": str(k), "label": str(v), "desc": ""})
    elif isinstance(raw_options, list):
        for idx, v in enumerate(raw_options):
            if isinstance(v, dict):
                item = copy.copy(v)
                item["id"] = str(item.get("id", idx + 1))
                item["label"] = str(item.get("label", item.get("txt", item.get("name", f"Option {item['id']}"))))
                item["desc"] = str(item.get("desc", item.get("description", "")))
                normalized.append(item)
            elif isinstance(v, (list, tuple)) and len(v) >= 2:
                normalized.append({"id": str(idx + 1), "label": str(v[0]), "desc": f"Score adjustment: {v[1]}", "trust_delta": v[1]})
            else:
                normalized.append({"id": str(idx + 1), "label": str(v), "desc": ""})
    return normalized

# ---------------------------------------------------------
# GLOBAL SHARED GAME STATE (Multi-Device / Multi-Tab Synchronization)
# ---------------------------------------------------------
class GameState:
    def __init__(self):
        self.reset()

    def reset(self, base_score: float = 100.0):
        self.base_score = base_score
        self.scores = {
            "Trust": float(base_score),
            "Fiscal": float(base_score),
            "Op-Eff": float(base_score)
        }
        self.current_round = 1
        self.max_rounds = 3
        # Phases: 'lobby', 'hacker', 'defense', 'media', 'recap', 'game_over'
        self.phase = "lobby"
        self.multiplier = 1.0
        
        self.selected_attack_key: Optional[str] = None
        self.selected_attack_data: Optional[Dict[str, Any]] = None
        self.it_choice_id: Optional[str] = None
        self.exec_choice_id: Optional[str] = None
        self.media_headline_idx: Optional[int] = None
        
        self.team_scorecard = {
            "IT": 0,
            "Exec": 0,
            "Media": 0,
            "Hacker": 0
        }
        
        self.history = []
        self.snapshots = []

    def create_snapshot(self):
        snap = {
            "scores": copy.deepcopy(self.scores),
            "current_round": self.current_round,
            "phase": self.phase,
            "multiplier": self.multiplier,
            "team_scorecard": copy.deepcopy(self.team_scorecard),
            "selected_attack_key": self.selected_attack_key,
            "selected_attack_data": copy.deepcopy(self.selected_attack_data),
            "it_choice_id": self.it_choice_id,
            "exec_choice_id": self.exec_choice_id,
            "media_headline_idx": self.media_headline_idx,
            "history": copy.deepcopy(self.history)
        }
        self.snapshots.append(snap)

    def undo_last_round(self) -> bool:
        if not self.snapshots:
            return False
        snap = self.snapshots.pop()
        self.scores = copy.deepcopy(snap["scores"])
        self.current_round = snap["current_round"]
        self.phase = snap["phase"]
        self.multiplier = snap["multiplier"]
        self.team_scorecard = copy.deepcopy(snap["team_scorecard"])
        self.selected_attack_key = snap["selected_attack_key"]
        self.selected_attack_data = copy.deepcopy(snap["selected_attack_data"])
        self.it_choice_id = snap["it_choice_id"]
        self.exec_choice_id = snap["exec_choice_id"]
        self.media_headline_idx = snap["media_headline_idx"]
        self.history = copy.deepcopy(snap["history"])
        return True

    def submit_hacker_attack(self, choice_key: str):
        self.create_snapshot()
        self.selected_attack_key = choice_key
        round_attacks = ATTACKS.get(self.current_round, {})
        self.selected_attack_data = round_attacks.get(choice_key, {})
        self.phase = "defense"

    def submit_it_choice(self, choice_id: str):
        self.it_choice_id = str(choice_id)
        self._check_defense_complete()

    def submit_exec_choice(self, choice_id: str):
        self.exec_choice_id = str(choice_id)
        self._check_defense_complete()

    def _check_defense_complete(self):
        if self.it_choice_id and self.exec_choice_id:
            self.phase = "media"

    def submit_media_choice(self, headline_idx: int):
        self.media_headline_idx = headline_idx
        self.evaluate_round()

    def evaluate_round(self):
        attack = self.selected_attack_data or {}
        
        raw_it = IT_CHOICES.get(self.current_round, {}).get(self.selected_attack_key, [])
        it_options = normalize_options_list(raw_it)
        it_choice = next((c for c in it_options if str(c.get("id")) == str(self.it_choice_id)), {})
        
        raw_exec = EXEC_CHOICES.get(self.current_round, [])
        exec_options = normalize_options_list(raw_exec)
        exec_choice = next((c for c in exec_options if str(c.get("id")) == str(self.exec_choice_id)), {})
        
        media_choice = None
        norm_headlines = normalize_options_list(DYNAMIC_HEADLINES)
        if self.media_headline_idx is not None and 0 <= self.media_headline_idx < len(norm_headlines):
            media_choice = norm_headlines[self.media_headline_idx]

        try:
            impact_result = calculate_round_impact(
                attack=attack,
                it_choice=it_choice,
                exec_choice=exec_choice,
                media_headline=media_choice,
                multiplier=self.multiplier
            )
        except Exception:
            impact_result = default_calculate_round_impact(
                attack=attack,
                it_choice=it_choice,
                exec_choice=exec_choice,
                media_headline=media_choice,
                multiplier=self.multiplier
            )

        deltas = impact_result.get("deltas", {})
        team_round_scores = impact_result.get("team_scorecard", {})

        for metric, delta in deltas.items():
            if metric in self.scores:
                self.scores[metric] = max(0.0, min(self.base_score * 1.5, round(self.scores[metric] + delta, 1)))

        for team, score in team_round_scores.items():
            self.team_scorecard[team] = self.team_scorecard.get(team, 0) + score

        record = {
            "round": self.current_round,
            "attack": attack.get("name", "Unknown Vector"),
            "attack_key": self.selected_attack_key,
            "it_action": it_choice.get("label", "None"),
            "exec_action": exec_choice.get("label", "None"),
            "headline": media_choice.get("headline", media_choice.get("label", "No press release")) if media_choice else "None",
            "deltas": deltas,
            "round_team_scores": team_round_scores,
            "scores_after": copy.deepcopy(self.scores),
            "multiplier": self.multiplier
        }
        self.history.append(record)
        self.phase = "recap"

    def advance_to_next_round(self):
        if self.current_round >= self.max_rounds:
            self.phase = "game_over"
        else:
            self.current_round += 1
            self.selected_attack_key = None
            self.selected_attack_data = None
            self.it_choice_id = None
            self.exec_choice_id = None
            self.media_headline_idx = None
            self.phase = "hacker"

@st.cache_resource
def get_global_game() -> GameState:
    return GameState()

# ---------------------------------------------------------
# UI HELPER FUNCTIONS
# ---------------------------------------------------------
def render_metric_gauge(label: str, value: float, max_val: float = 100.0):
    pct = max(0.0, min(100.0, (value / max_val) * 100.0))
    if pct >= 70:
        bar_color = "#10b981"  # Emerald / Green
        status_text = "HEALTHY"
    elif pct >= 45:
        bar_color = "#f59e0b"  # Amber / Warning
        status_text = "DEGRADED"
    else:
        bar_color = "#ef4444"  # Red / Critical
        status_text = "CRITICAL"

    st.markdown(f"""
    <div style="background-color: #0f172a; padding: 14px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 13px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">{label}</span>
            <span style="font-size: 12px; font-weight: 800; color: {bar_color};">{status_text}</span>
        </div>
        <div style="display: flex; align-items: baseline; gap: 8px;">
            <span style="font-size: 28px; font-weight: 800; color: #f8fafc;">{value:.1f}</span>
            <span style="font-size: 12px; color: #64748b;">/ {max_val:.0f}</span>
        </div>
        <div style="background-color: #1e293b; height: 8px; border-radius: 999px; overflow: hidden; margin-top: 8px;">
            <div style="background-color: {bar_color}; width: {pct}%; height: 100%; border-radius: 999px; transition: width 0.4s ease;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_scorecard_quadrant(scorecard: Dict[str, int]):
    st.markdown("### 🏆 4-Quadrant Team Performance Scorecard")
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        st.metric(label="🛡️ IT Defense", value=f"{scorecard.get('IT', 0)} pts")
    with q2:
        st.metric(label="💼 Executive Board", value=f"{scorecard.get('Exec', 0)} pts")
    with q3:
        st.metric(label="🎤 Media & PR", value=f"{scorecard.get('Media', 0)} pts")
    with q4:
        st.metric(label="💀 Threat Actors", value=f"{scorecard.get('Hacker', 0)} pts")

# ---------------------------------------------------------
# DASHBOARD: MAIN MISSION CONTROL
# ---------------------------------------------------------
def render_main_dashboard(game: GameState):
    st.title("🛡️ CloudStore Command: Mission Control")
    st.caption("Live Operational Cyber Incident Response Dashboard")

    # Top Metrics Row
    m1, m2, m3 = st.columns(3)
    with m1:
        render_metric_gauge("Customer Trust (NPS)", game.scores["Trust"], game.base_score)
    with m2:
        render_metric_gauge("Fiscal Health ($M / Stock)", game.scores["Fiscal"], game.base_score)
    with m3:
        render_metric_gauge("Operational Efficiency (RTO)", game.scores["Op-Eff"], game.base_score)

    st.markdown("---")

    # Current Game Status Banner
    phase_descriptions = {
        "lobby": "🎮 Simulation in Lobby — Waiting for GM to Start Round 1",
        "hacker": f"🔴 Round {game.current_round}: Awaiting Threat Actor Attack Vector Selection...",
        "defense": f"🟡 Round {game.current_round}: Incident Active! IT Defense & Executive Board Deliberating...",
        "media": f"🟠 Round {game.current_round}: Press Scrum Active — Awaiting Media Headline...",
        "recap": f"🟢 Round {game.current_round}: Assessment Complete — Reviewing Score Impact",
        "game_over": "🏁 Simulation Concluded — Final Assessment"
    }
    st.info(phase_descriptions.get(game.phase, f"Phase: {game.phase}"))

    # Active Incident Banner
    if game.selected_attack_data:
        att = game.selected_attack_data
        st.markdown(f"""
        <div style="background-color: #450a0a; border: 2px solid #ef4444; border-radius: 12px; padding: 18px; margin: 12px 0;">
            <div style="font-size: 11px; font-weight: 800; color: #fca5a5; text-transform: uppercase; letter-spacing: 0.1em;">ACTIVE INCIDENT ALERT</div>
            <div style="font-size: 22px; font-weight: 800; color: #ffffff; margin-top: 4px;">{att.get('icon', '🚨')} {att.get('name', 'Cyber Incident')}</div>
            <div style="font-size: 14px; color: #fecaca; margin-top: 6px;">{att.get('description', '')}</div>
        </div>
        """, unsafe_allow_html=True)

    # 4-Quadrant Scorecard
    render_scorecard_quadrant(game.team_scorecard)

    st.markdown("---")

    # Timeline Log
    if game.history:
        st.markdown("### 📜 Mission Incident Timeline")
        for entry in reversed(game.history):
            with st.expander(f"Round {entry['round']}: {entry['attack']} ({entry['multiplier']}x Multiplier)", expanded=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**IT Containment:** {entry['it_action']}")
                    st.write(f"**Executive Action:** {entry['exec_action']}")
                    st.write(f"**Headline Published:** {entry['headline']}")
                with col_b:
                    st.write("**Impact Deltas:**")
                    for m, d in entry['deltas'].items():
                        delta_color = "green" if d >= 0 else "red"
                        st.markdown(f"- {m}: <span style='color:{delta_color};font-weight:bold;'>{d:+g}</span>", unsafe_allow_html=True)
                    st.write(f"**Scores After Round:** Trust: {entry['scores_after']['Trust']:.1f} | Fiscal: {entry['scores_after']['Fiscal']:.1f} | Op-Eff: {entry['scores_after']['Op-Eff']:.1f}")

# ---------------------------------------------------------
# ROLE TERMINAL VIEWS (For Specific Teams)
# ---------------------------------------------------------
def render_hacker_terminal(game: GameState):
    st.title("💀 Threat Actor Command Terminal")
    st.caption("Access Level: Adversary / Red Team Infiltration")

    if game.phase == "lobby":
        st.warning("⏳ Simulation is in lobby. Awaiting Mission Control to begin.")
        return

    if game.phase != "hacker":
        st.info("🔒 Attack vector locked. Standing by while Blue Team & Media react.")
        if game.selected_attack_data:
            st.markdown(f"**Current Attack Deployed:** {game.selected_attack_data.get('name')}")
        return

    st.subheader(f"Round {game.current_round}: Select Primary Infiltration Vector")
    round_attacks = ATTACKS.get(game.current_round, {})
    
    col_a, col_b = st.columns(2)
    with col_a:
        att_a = round_attacks.get("A", {})
        st.markdown(f"### {att_a.get('icon', '🅰️')} Strategy A: {att_a.get('name', 'Strategy A')}")
        st.write(att_a.get("description", ""))
        st.caption(f"Base Threat Damage: {att_a.get('base_impact', {})}")
        if st.button("🚀 Launch Strategy A", type="primary", key="btn_hacker_a", use_container_width=True):
            game.submit_hacker_attack("A")
            st.success("Payload deployed! Alert triggered in Mission Control.")
            st.rerun()

    with col_b:
        att_b = round_attacks.get("B", {})
        st.markdown(f"### {att_b.get('icon', '🅱️')} Strategy B: {att_b.get('name', 'Strategy B')}")
        st.write(att_b.get("description", ""))
        st.caption(f"Base Threat Damage: {att_b.get('base_impact', {})}")
        if st.button("🚀 Launch Strategy B", type="primary", key="btn_hacker_b", use_container_width=True):
            game.submit_hacker_attack("B")
            st.success("Payload deployed! Alert triggered in Mission Control.")
            st.rerun()

def render_it_terminal(game: GameState):
    st.title("🛡️ IT Defense Command Terminal")
    st.caption("Access Level: Security Operations Center (SOC) / Incident Response")

    if game.phase in ["lobby", "hacker"]:
        st.info("🟢 Systems nominal. Awaiting threat telemetry from network sensors...")
        return

    att = game.selected_attack_data or {}
    st.error(f"🚨 **ACTIVE BREACH:** {att.get('icon', '')} {att.get('name', 'Security Incident')} — {att.get('description', '')}")

    if game.it_choice_id:
        st.success("✅ Technical mitigation submitted! Standing by for Executive and Media directives.")
        return

    st.subheader("Select Technical Containment Action")
    st.caption("Review simplified containment options below:")

    raw_options = IT_CHOICES.get(game.current_round, {}).get(game.selected_attack_key, [])
    it_options = normalize_options_list(raw_options)

    if not it_options:
        st.warning("No IT options defined for this scenario.")
        return

    for opt in it_options:
        with st.container():
            desc_text = opt.get('desc', '')
            desc_html = f"<div style='color: #94a3b8; font-size: 13px; margin-top: 4px;'>{desc_text}</div>" if desc_text else ""
            st.markdown(f"""
            <div style="background-color: #0f172a; padding: 12px; border-radius: 10px; border-left: 4px solid #38bdf8; margin-bottom: 8px;">
                <div style="font-weight: 700; color: #f8fafc; font-size: 15px;">Option {opt['id']}: {opt['label']}</div>
                {desc_html}
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Deploy Option {opt['id']}", key=f"btn_it_{opt['id']}", use_container_width=True):
                game.submit_it_choice(str(opt['id']))
                st.rerun()

def render_exec_terminal(game: GameState):
    st.title("💼 Executive Boardroom Terminal")
    st.caption("Access Level: C-Suite / Strategic Communications & Legal")

    if game.phase in ["lobby", "hacker"]:
        st.info("🟢 Board in session. Monitoring enterprise risk posture.")
        return

    att = game.selected_attack_data or {}
    st.error(f"🚨 **CRITICAL INCIDENT:** {att.get('icon', '')} {att.get('name', 'Incident Alert')} — {att.get('description', '')}")

    if game.exec_choice_id:
        st.success("✅ Executive directive confirmed! Waiting for IT and Media finalization.")
        return

    st.subheader("Select Strategic Directive")
    st.caption("Review simplified policy options below:")

    raw_options = EXEC_CHOICES.get(game.current_round, [])
    exec_options = normalize_options_list(raw_options)

    if not exec_options:
        st.warning("No Executive options defined for this round.")
        return

    for opt in exec_options:
        with st.container():
            desc_text = opt.get('desc', '')
            desc_html = f"<div style='color: #94a3b8; font-size: 13px; margin-top: 4px;'>{desc_text}</div>" if desc_text else ""
            st.markdown(f"""
            <div style="background-color: #0f172a; padding: 12px; border-radius: 10px; border-left: 4px solid #818cf8; margin-bottom: 8px;">
                <div style="font-weight: 700; color: #f8fafc; font-size: 15px;">Directive {opt['id']}: {opt['label']}</div>
                {desc_html}
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Authorize Directive {opt['id']}", key=f"btn_exec_{opt['id']}", use_container_width=True):
                game.submit_exec_choice(str(opt['id']))
                st.rerun()

def render_media_terminal(game: GameState):
    st.title("🎤 Media & PR Press Scrum")
    st.caption("Access Level: Public Affairs / Investigative Journalism")

    if game.phase in ["lobby", "hacker", "defense"]:
        st.info("📡 Monitoring developing story. Waiting for initial response statements from CloudStore.")
        return

    if game.phase == "recap":
        st.success("📰 Headline published! Check Mission Control scoreboard for Trust impact.")
        return

    st.subheader("Select Breaking News Narrative")
    st.caption("Choose which angle to lead with for the news cycle:")

    headlines_list = normalize_options_list(DYNAMIC_HEADLINES)
    for idx, item in enumerate(headlines_list):
        headline_text = item.get("headline", item.get("label", f"Headline #{idx + 1}"))
        delta = item.get("trust_delta", item.get("value", 0))
        try:
            delta_num = float(delta)
            delta_str = f"+{delta_num:g}" if delta_num > 0 else f"{delta_num:g}"
            badge_color = "#10b981" if delta_num > 0 else "#64748b" if delta_num == 0 else "#ef4444"
        except (ValueError, TypeError):
            delta_str = str(delta)
            badge_color = "#64748b"

        st.markdown(f"""
        <div style="background-color: #0f172a; padding: 12px; border-radius: 10px; border: 1px solid #1e293b; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 15px; font-weight: 700; color: #f8fafc;">\"{headline_text}\"</span>
            <span style="background-color: {badge_color}; color: white; padding: 2px 8px; border-radius: 999px; font-size: 12px; font-weight: 800;">Trust {delta_str}</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Publish Headline #{idx + 1}", key=f"btn_media_{idx}", use_container_width=True):
            game.submit_media_choice(idx)
            st.rerun()

# ---------------------------------------------------------
# MAIN APP ENTRYPOINT WITH DEDICATED GM SIDEBAR & QUERY PARAM ROUTING
# ---------------------------------------------------------
def main():
    st.set_page_config(
        page_title="CloudStore Command: Mission Control",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    game = get_global_game()

    # 1. Resolve Team/Role from URL Query Parameters
    # e.g., ?team=it or ?team=hackers or ?team=exec or ?team=media or ?team=main
    try:
        qp = st.query_params
        url_role = qp.get("team") or qp.get("role") or ""
    except Exception:
        try:
            qp_old = st.experimental_get_query_params()
            url_role = qp_old.get("team", [""])[0] or qp_old.get("role", [""])[0]
        except Exception:
            url_role = ""

    url_role = url_role.lower().strip()

    # 2. Check if user is on a dedicated Team URL
    is_team_url = url_role in ["hackers", "it", "exec", "media"]

    if is_team_url:
        # Player Team Terminal View (Clean, distraction-free layout)
        st.sidebar.title("🔐 Team Access")
        st.sidebar.success(f"Connected: **{url_role.upper()}**")
        st.sidebar.caption(f"Round: **{game.current_round} / {game.max_rounds}**")
        st.sidebar.caption(f"Phase: **{game.phase.upper()}**")

        if st.sidebar.button("🔄 Refresh View", use_container_width=True):
            st.rerun()

        st.sidebar.markdown("---")
        if st.sidebar.button("🎮 Switch to GM Mode", use_container_width=True):
            try:
                st.query_params["team"] = "main"
            except Exception:
                pass
            st.rerun()

        # Render the specific team terminal in the main larger area
        if url_role == "hackers":
            render_hacker_terminal(game)
        elif url_role == "it":
            render_it_terminal(game)
        elif url_role == "exec":
            render_exec_terminal(game)
        elif url_role == "media":
            render_media_terminal(game)
        return

    # 3. GM / Instructor Mode (Dashboard in main area, GM controls in sidebar)
    st.sidebar.title("🎮 Game Master (GM) Console")

    if "admin_authenticated" not in st.session_state:
        st.session_state["admin_authenticated"] = False

    correct_admin_code = TEAM_CODES.get("main", "admin123")

    # Password gate for displaying Group URLs and administrative controls
    if not st.session_state["admin_authenticated"]:
        st.sidebar.caption("🔒 Admin Passcode Required")
        admin_pwd = st.sidebar.text_input(
            "Admin Password",
            type="password",
            key="admin_pwd_entry",
            help="Enter the GM passcode to reveal team URLs and game controls."
        )

        unlocked = False
        if st.sidebar.button("🔓 Unlock GM Console", type="primary", use_container_width=True):
            if admin_pwd in [correct_admin_code, "admin"]:
                st.session_state["admin_authenticated"] = True
                unlocked = True
                st.rerun()
            else:
                st.sidebar.error("❌ Incorrect Admin Password.")

        # Quick unlock on Enter key if password matches
        if admin_pwd and admin_pwd in [correct_admin_code, "admin"] and not unlocked:
            st.session_state["admin_authenticated"] = True
            st.rerun()

        st.sidebar.info("🔒 Enter Admin Password to reveal shareable team URLs and simulation controls.")

        # Main area displays the public Mission Control Dashboard in read-only mode
        render_main_dashboard(game)
        return

    # --- Authenticated GM View ---
    st.sidebar.success("🔓 GM Console Unlocked")
    if st.sidebar.button("🔒 Lock Console", use_container_width=True):
        st.session_state["admin_authenticated"] = False
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Round:** {game.current_round} / {game.max_rounds} &nbsp;|&nbsp; **Phase:** `{game.phase.upper()}`")

    # GM Controls: Simulation Progress
    st.sidebar.markdown("### 🕹️ Round Management")
    if game.phase == "lobby":
        if st.sidebar.button("🚀 Start Round 1", type="primary", use_container_width=True):
            game.phase = "hacker"
            st.rerun()
    elif game.phase == "recap":
        next_label = "🏁 Conclude Game" if game.current_round >= game.max_rounds else f"Start Round {game.current_round + 1}"
        if st.sidebar.button(f"➡️ {next_label}", type="primary", use_container_width=True):
            game.advance_to_next_round()
            st.rerun()
    elif game.phase == "game_over":
        st.sidebar.success("🏁 Simulation Finished!")
    else:
        st.sidebar.info(f"Awaiting team inputs for phase: **{game.phase.upper()}**")

    # Threat Multiplier
    game.multiplier = st.sidebar.selectbox(
        "⚡ Threat Severity Multiplier",
        options=[1.0, 1.2, 1.5, 2.0],
        index=[1.0, 1.2, 1.5, 2.0].index(game.multiplier) if game.multiplier in [1.0, 1.2, 1.5, 2.0] else 0,
        format_func=lambda x: f"{x}x Threat Intensity"
    )

    # Undo & Reset Controls
    col_u, col_r = st.sidebar.columns(2)
    with col_u:
        if st.button("↩️ Undo", use_container_width=True, disabled=len(game.snapshots) == 0):
            if game.undo_last_round():
                st.success("Rolled back.")
                st.rerun()
    with col_r:
        if st.button("🔄 Reset", use_container_width=True):
            game.reset()
            st.rerun()

    st.sidebar.markdown("---")

    # Shareable Team Specific URLs Section (LOCKED BEHIND ADMIN PASSWORD)
    st.sidebar.markdown("### 🔗 Shareable Team URLs")
    st.sidebar.caption("Send these direct links to the respective player teams:")

    default_base_url = "https://cyberattacksim.streamlit.app"
    base_url = st.sidebar.text_input("App Base URL", value=default_base_url, help="Change if testing on localhost or custom domain.")
    base_url = base_url.rstrip("/")

    team_links = {
        "💀 Threat Actors (Hackers)": f"{base_url}/?team=hackers",
        "🛡️ IT Defense Command": f"{base_url}/?team=it",
        "💼 Executive Boardroom": f"{base_url}/?team=exec",
        "🎤 Media & PR Scrum": f"{base_url}/?team=media",
        "🎮 GM Mission Control": f"{base_url}/?team=main"
    }

    for label, link in team_links.items():
        with st.sidebar.expander(label, expanded=False):
            st.code(link, language="text")
            st.caption(f"[Open Link in New Tab]({link})")

    st.sidebar.markdown("---")

    # GM View Switcher / Terminal Preview
    st.sidebar.markdown("### 👁️ Terminal Preview")
    preview_mode = st.sidebar.selectbox(
        "View As:",
        options=["Main Dashboard", "Threat Actor Terminal", "IT Defense Terminal", "Executive Terminal", "Media Terminal"]
    )

    if st.sidebar.button("🔄 Force Refresh All", use_container_width=True):
        st.rerun()

    # Render selected view in the larger main area
    if preview_mode == "Main Dashboard":
        render_main_dashboard(game)
    elif preview_mode == "Threat Actor Terminal":
        render_hacker_terminal(game)
    elif preview_mode == "IT Defense Terminal":
        render_it_terminal(game)
    elif preview_mode == "Executive Terminal":
        render_exec_terminal(game)
    elif preview_mode == "Media Terminal":
        render_media_terminal(game)

if __name__ == "__main__":
    main()
