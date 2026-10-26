"""
ui_components.py
Reusable UI widgets for CloudStore Command: Cyber Attack Simulation
Includes Threatening Ticking Clock, Health Gauge, Polling Bars, and Briefings.
"""

import sys
import os
from pathlib import Path
import streamlit as st
import time
from typing import Dict, Any, List, Optional

# Ensure repository root is in sys.path
_repo_dir = str(Path(__file__).resolve().parent)
if _repo_dir not in sys.path:
    sys.path.insert(0, _repo_dir)

from game_data import load_markdown_content

def render_threatening_clock(remaining_secs: int, total_secs: int, phase_name: str, is_paused: bool = False):
    """
    Renders an ominous, high-stakes ticking countdown clock.
    Features red/amber warning colors, digital typography, and pulse animations.
    """
    mins = max(0, remaining_secs) // 60
    secs = max(0, remaining_secs) % 60
    time_str = f"{mins:02d}:{secs:02d}"

    # Determine alert state
    is_urgent = remaining_secs <= 60 and not is_paused
    is_expired = remaining_secs <= 0

    if is_expired:
        border_color = "#ef4444"
        glow_color = "rgba(239, 68, 68, 0.6)"
        clock_color = "#f87171"
        status_label = "🚨 CRITICAL TIMEOUT — DECISION IMMEDIATE REQUIRED"
        anim_css = "animation: pulse-urgent 1s infinite;"
    elif is_urgent:
        border_color = "#f59e0b"
        glow_color = "rgba(245, 158, 11, 0.6)"
        clock_color = "#fbbf24"
        status_label = "⚠️ THREAT WINDOW RAPIDLY CLOSING"
        anim_css = "animation: pulse-urgent 1.2s infinite;"
    elif is_paused:
        border_color = "#475569"
        glow_color = "rgba(71, 85, 105, 0.3)"
        clock_color = "#94a3b8"
        status_label = "⏸️ SIMULATION PAUSED BY GAME MASTER"
        anim_css = ""
    else:
        border_color = "#dc2626"
        glow_color = "rgba(220, 38, 38, 0.3)"
        clock_color = "#fca5a5"
        status_label = f"⏳ ACTIVE THREAT WINDOW — {phase_name.upper()} PHASE"
        anim_css = ""

    pct = max(0.0, min(100.0, (remaining_secs / max(1, total_secs)) * 100.0))

    html = f"""
    <style>
    @keyframes pulse-urgent {{
        0% {{ box-shadow: 0 0 8px {glow_color}; }}
        50% {{ box-shadow: 0 0 24px {glow_color}; }}
        100% {{ box-shadow: 0 0 8px {glow_color}; }}
    }}
    .threat-clock-container {{
        background: linear-gradient(180deg, #090d16 0%, #030712 100%);
        border: 2px solid {border_color};
        border-radius: 14px;
        padding: 14px 20px;
        margin: 10px 0 20px 0;
        text-align: center;
        box-shadow: 0 4px 20px {glow_color};
        {anim_css}
    }}
    .clock-title {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, monospace;
        font-size: 14px;
        font-weight: 800;
        color: {clock_color};
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }}
    .clock-digits {{
        font-family: "Courier New", Courier, monospace;
        font-size: 46px;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: 0.08em;
        text-shadow: 0 0 14px {glow_color};
        line-height: 1.15;
    }}
    .clock-bar-bg {{
        background-color: #1e293b;
        height: 10px;
        border-radius: 999px;
        overflow: hidden;
        margin-top: 10px;
    }}
    .clock-bar-fill {{
        background: linear-gradient(90deg, {border_color}, {clock_color});
        width: {pct}%;
        height: 100%;
        border-radius: 999px;
        transition: width 0.5s ease;
    }}
    </style>
    <div class="threat-clock-container">
        <div class="clock-title">{status_label}</div>
        <div class="clock-digits">{time_str}</div>
        <div class="clock-bar-bg">
            <div class="clock-bar-fill"></div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_health_gauge(health: float, bankrupt_cutoff: int, win_cutoff: int):
    """Renders the primary unified Company Health Score gauge with calibrated thresholds."""
    val = max(0.0, min(100.0, float(health)))
    
    if val >= win_cutoff:
        status_text = "WINNING TIER (RESILIENT)"
        bar_color = "#10b981"  # Emerald
        glow = "rgba(16, 185, 129, 0.4)"
    elif val >= bankrupt_cutoff:
        status_text = "SURVIVING TIER (DAMAGED)"
        bar_color = "#f59e0b"  # Amber
        glow = "rgba(245, 158, 11, 0.4)"
    else:
        status_text = "BANKRUPTCY IMMINENT"
        bar_color = "#ef4444"  # Red
        glow = "rgba(239, 68, 68, 0.6)"

    html = f"""
    <div style="background-color: #030712; padding: 20px 22px; border-radius: 14px; border: 1px solid #1e293b; box-shadow: 0 4px 18px {glow}; margin-bottom: 18px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 15px; font-weight: 800; color: #cbd5e1; text-transform: uppercase; letter-spacing: 0.1em;">🏢 Unified Enterprise Health</span>
            <span style="font-size: 14px; font-weight: 800; color: {bar_color}; letter-spacing: 0.05em;">{status_text}</span>
        </div>
        <div style="display: flex; align-items: baseline; gap: 10px;">
            <span style="font-size: 46px; font-weight: 900; color: #f8fafc; font-family: monospace;">{val:.1f}</span>
            <span style="font-size: 18px; font-weight: 700; color: #94a3b8;">/ 100.0 HP</span>
        </div>
        <div style="background-color: #1e293b; height: 16px; border-radius: 999px; overflow: hidden; margin-top: 12px; position: relative;">
            <div style="background-color: {bar_color}; width: {val}%; height: 100%; border-radius: 999px; transition: width 0.4s ease;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: 600; color: #cbd5e1; margin-top: 8px;">
            <span>💥 Bankrupt (&lt; {bankrupt_cutoff})</span>
            <span>🛡️ Survive ({bankrupt_cutoff} - {win_cutoff - 1})</span>
            <span>🏆 Win (&ge; {win_cutoff})</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_briefing_card(role: str, filename: str, fallback_title: str, fallback_desc: str, it_plan: Optional[Dict[str, Any]] = None):
    """Renders markdown scenario briefing from content/ with clean formatting."""
    md_content = load_markdown_content(role, filename)
    if role == "exec" and it_plan:
        downtime = it_plan.get("downtime", "Operational Downtime")
        cust_impact = it_plan.get("customer_impact", "Noticeable Latency")
        mit_like = it_plan.get("mitigation_likelihood", "Moderate")
        stock = it_plan.get("stock_outlook", "Market reaction dependent on duration.")
        rep = it_plan.get("reputation_risk", "Brand perception contingent on containment integrity.")
        plan_label = it_plan.get("label", "Proposed Technical Action")
        plan_short = it_plan.get("label_short", plan_label)

        exec_it_summary = f"""
---
**🛡️ Active IT Department Recommendation Under Board Review:**
* **Recommended Containment Plan**: **{plan_label}**
* **Projected System Downtime**: {downtime}
* **Customer & Operations Impact**: {cust_impact}
* **Threat Mitigation Likelihood**: {mit_like}
* **📈 Stock Price Outlook**: {stock}
* **🤝 Customer Reputation Risk**: {rep}

**Corporate Governance Directives Under Deliberation:**
* **✅ Agree with IT**: Authorize {plan_short}. Accept operational downtime to ensure maximum threat containment and protect enterprise data.
* **⚖️ Compromise**: Order IT to cut downtime in half, halving containment to keep customer storefronts operating.
* **🚫 Override IT**: Reject IT's shutdown to maintain business continuity (0% mitigation; triggers an Executive Override penalty of +10% to +35% damage).
"""
        md_content = (md_content or "") + exec_it_summary

    with st.expander(f"📖 Intelligence Dossier: {fallback_title}", expanded=True):
        if md_content:
            st.markdown(md_content)
        else:
            st.info(fallback_desc)

def render_round_recap_card(game):
    """Renders the round debrief and net impact breakdown across all player terminals."""
    if not game.history:
        return
    entry = game.history[-1]
    delta_color = "#10b981" if entry['net_delta'] >= 0 else "#ef4444"
    it_surprise = entry.get('it_surprise', '')
    media_surprise = entry.get('media_surprise', '')
    attack_meta = f"Complexity: {entry.get('attack_complexity', 'Medium')} | Anonymity: {entry.get('attack_anonymity', 'Moderate')}"

    surprise_html = ""
    if it_surprise or media_surprise:
        it_line = f'<div style="font-size: 14px; color: #f1f5f9; margin-bottom: 6px; line-height: 1.4;">🛡️ <strong>IT Defense:</strong> {it_surprise}</div>' if it_surprise else ''
        media_line = f'<div style="font-size: 14px; color: #f1f5f9; line-height: 1.4;">📰 <strong>Media Resonance:</strong> {media_surprise}</div>' if media_surprise else ''
        surprise_html = (
            f'<div style="background-color: #0f172a; border-radius: 10px; padding: 14px; margin: 14px 0; border: 1px solid #1e293b;">'
            f'<div style="font-size: 13px; font-weight: 800; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">🔍 Surprise & Reality Check (Outcome Analysis)</div>'
            f'{it_line}'
            f'{media_line}'
            f'</div>'
        )

    penalty_badges = []
    if entry.get("backfire_pct", 0) > 0:
        penalty_badges.append(f"+{entry['backfire_pct']:.0f}% Inaction Backfire")
    if entry.get("override_pct", 0) > 0:
        penalty_badges.append(f"+{entry['override_pct']:.0f}% Exec Override Penalty")
    penalty_str = f" <span style='color: #fca5a5; font-size: 13px;'>({', '.join(penalty_badges)})</span>" if penalty_badges else ""

    recap_html = (
        f'<div style="background-color: #030712; border: 2px solid #38bdf8; border-radius: 14px; padding: 22px; margin: 18px 0;">'
        f'<div style="font-size: 14px; font-weight: 800; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.1em;">ROUND {entry["round"]} INCIDENT DEBRIEF</div>'
        f'<div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 6px;">'
        f'<span style="font-size: 22px; font-weight: 900; color: #ffffff;">{entry["attack_name"]}</span>'
        f'<span style="font-size: 26px; font-weight: 900; color: {delta_color};">{entry["net_delta"]:+g} HP</span>'
        f'</div>'
        f'<div style="font-size: 14px; color: #cbd5e1; margin-top: 4px;">Adversary Vector Profile: <em>{attack_meta}</em></div>'
        f'<div style="font-size: 15px; color: #f1f5f9; margin-top: 6px;">Breaking Headline: <em>"{entry["headline"]}"</em> ({entry["media_delta"]:+g} HP)</div>'
        f'{surprise_html}'
        f'<hr style="border-color: #1e293b; margin: 14px 0;" />'
        f'<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 14px; color: #f1f5f9; line-height: 1.5;">'
        f'<div><strong>Threat Exploit:</strong> {entry["attack_damage"]:+g} HP{penalty_str}</div>'
        f'<div><strong>IT Defense Mitigated:</strong> +{entry["it_mitigated"]:g} HP ({entry.get("it_mit_pct", 60)}%)</div>'
        f'<div><strong>Operational Disruption:</strong> {entry["disruption_penalty"]:+g} HP</div>'
        f'<div><strong>Governance:</strong> {entry["exec_decision"]}</div>'
        f'</div>'
        f'<div style="margin-top: 14px; font-size: 16px; font-weight: 800; color: #f8fafc;">'
        f'Enterprise Health: {entry["health_before"]:.1f} → <span style="color: {delta_color};">{entry["health_after"]:.1f} / 100.0 HP</span>'
        f'</div>'
        f'</div>'
    )
    st.markdown(recap_html, unsafe_allow_html=True)

def render_final_hacker_action_card(game):
    """Renders the debrief of the Adversary Final Gambit (Press Attack vs Retreat)."""
    data = getattr(game, "final_hacker_action_data", None)
    if not data:
        return

    action = data.get("action", "retreat")
    delta = data.get("net_delta", 0)
    delta_color = "#10b981" if delta > 0 else "#ef4444" if delta < 0 else "#94a3b8"
    exposure = data.get("exposure_level", "Standard")

    if action == "press":
        card_bg = "#450a0a" if not data.get("caught") else "#3b0764"
        card_border = "#ef4444" if not data.get("caught") else "#a855f7"
        badge = f"🚨 ADVERSARY PRESSED THE ATTACK &bull; EXPOSURE: {exposure.upper()}"
    else:
        card_bg = "#0f172a"
        card_border = "#475569"
        badge = "🛑 ADVERSARY RETREATED INTO THE SHADOWS"

    card_html = (
        f'<div style="background-color: {card_bg}; border: 2px solid {card_border}; border-radius: 14px; padding: 22px; margin: 18px 0;">'
        f'<div style="font-size: 14px; font-weight: 800; color: #fca5a5; text-transform: uppercase; letter-spacing: 0.1em;">{badge}</div>'
        f'<div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 6px;">'
        f'<span style="font-size: 20px; font-weight: 900; color: #ffffff;">Final Gambit Outcome</span>'
        f'<span style="font-size: 24px; font-weight: 900; color: {delta_color};">{delta:+g} HP</span>'
        f'</div>'
        f'<div style="color: #f8fafc; font-size: 15px; margin-top: 8px; line-height: 1.5;">{data.get("summary", "")}</div>'
        f'<div style="margin-top: 10px; font-size: 14px; color: #cbd5e1;">Enterprise Health Shift: {data.get("health_before", 0):.1f} → <strong style="color: {delta_color};">{data.get("health_after", 0):.1f} HP</strong></div>'
        f'</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)

def render_acronym_glossary():
    """Renders an interactive educational cybersecurity vocabulary & acronym glossary."""
    with st.expander("📚 Student Cybersecurity Vocabulary & Acronym Glossary (Click to Expand)", expanded=False):
        st.markdown("""
        | Acronym | Full Term | Classroom Definition & Practical Context |
        | :--- | :--- | :--- |
        | **IT** | Information Technology | Enterprise computing systems, cloud infrastructure, and technical administration. |
        | **SOC** | Security Operations Center | The centralized incident response team monitoring network alerts and defending endpoints 24/7. |
        | **RTO** | Recovery Time Objective | The maximum acceptable duration of system downtime after an outage before the business suffers catastrophic loss. |
        | **EDR** | Endpoint Detection & Response | Advanced behavioral monitoring tools installed on workstations/servers to isolate infected devices before malware spreads. |
        | **CVE** | Common Vulnerabilities & Exposures | Standardized public catalog identifying known software security flaws (e.g., CVE-2024-XXXXX). |
        | **PII** | Personally Identifiable Information | Sensitive customer/employee data (passwords, credit cards, SSNs) protected by regulatory laws like GDPR and CCPA. |
        | **APT** | Advanced Persistent Threat | Highly skilled, well-funded cyber adversary groups (often state-sponsored) conducting stealthy, prolonged intrusions. |
        | **UEFI** | Unified Extensible Firmware Interface | Low-level firmware code on motherboards that executes before the operating system boots. Implants here survive OS reinstalls! |
        | **WAF** | Web Application Firewall | Protective security barrier filtering and inspecting incoming web traffic to block SQL injections and web exploits. |
        | **C2** | Command and Control | Attacker-controlled servers used to send instructions and extract stolen data from compromised internal machines. |
        | **DDoS** | Distributed Denial of Service | Cyberattack that floods servers with millions of fake requests, knocking public websites offline. |
        | **NPS** | Net Promoter Score | Metric measuring customer loyalty, trust, and brand perception (-100 to +100). |
        | **SEC** | Securities & Exchange Commission | U.S. regulatory agency enforcing legal disclosure of material cyber incidents and penalties for corporate deception. |
        | **OSINT** | Open-Source Intelligence | Publicly available intelligence (social media, public DNS, search engines) used by hackers for reconnaissance. |
        | **HP** | Health Points | Simulated enterprise vitality metric (0 to 100) reflecting financial solvency, system availability, and brand trust. |
        """)


