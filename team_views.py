"""
team_views.py
Role-specific terminals for Threat Actors, IT Defense, Executive Board, and Media
Includes single-URL Captain vs Viewer modes, live straw polling, and asymmetric information flow.
"""

import sys
import os
from pathlib import Path
import importlib
import streamlit as st
from typing import Dict, Any, List

# Ensure repository root is in sys.path
_repo_dir = str(Path(__file__).resolve().parent)
if _repo_dir not in sys.path:
    sys.path.insert(0, _repo_dir)

if "game_data" in sys.modules and not hasattr(sys.modules["game_data"], "ATTACKS"):
    del sys.modules["game_data"]
    importlib.invalidate_caches()

from state_manager import GameState
from game_data import ATTACKS, IT_CHOICES, EXEC_GOVERNANCE_OPTIONS, DYNAMIC_HEADLINES, get_it_choices, get_exec_governance_options
from ui_components import (
    render_threatening_clock,
    render_briefing_card,
    render_round_recap_card,
    render_final_hacker_action_card,
    render_acronym_glossary
)

def _render_poll_ui(game: GameState, role: str, is_captain: bool, voter_id: str, options: List[Dict[str, Any]]):
    """Renders the live straw poll interface for both Captain and Viewers."""
    poll = game.polls.get(role, {})
    is_poll_open = poll.get("open", False)
    stats = game.get_poll_stats(role)

    st.markdown("---")
    st.markdown("### 🗳️ Team Straw Poll")

    # Polling Status & Management
    if is_captain:
        col_p1, col_p2 = st.columns([2, 1])
        with col_p1:
            st.caption(f"Captain Control | Current votes: **{stats['total_votes']}**")
        with col_p2:
            if not is_poll_open:
                if st.button("📢 Launch Straw Poll", key=f"btn_open_poll_{role}", type="secondary", use_container_width=True):
                    game.open_poll(role, options)
                    st.rerun()
            else:
                if st.button("🔒 Close Straw Poll", key=f"btn_close_poll_{role}", use_container_width=True):
                    game.close_poll(role)
                    st.rerun()

    # Voting Area for Viewers & Captains
    if is_poll_open:
        st.info("🗳️ **A Straw Poll is active!** Cast your vote below to advise your Team Captain:")
        current_vote = poll.get("votes", {}).get(str(voter_id))

        vote_cols = st.columns(len(options))
        for idx, opt in enumerate(options):
            with vote_cols[idx]:
                opt_id = str(opt.get("id"))
                short_desc = opt.get("label_short")
                if short_desc and short_desc != opt_id:
                    btn_text = f"{opt_id} ({short_desc})"
                else:
                    btn_text = f"{opt_id}"

                is_selected = (current_vote == opt_id)
                btn_type = "primary" if is_selected else "secondary"
                btn_label = f"✅ Voted: {btn_text}" if is_selected else f"Vote: {btn_text}"

                if st.button(btn_label, key=f"vote_btn_{role}_{opt_id}", type=btn_type, use_container_width=True):
                    game.cast_vote(role, voter_id, opt_id)
                    st.rerun()

    # Live Bar Chart of Votes (Visible to everyone)
    if stats["total_votes"] > 0:
        st.markdown(f"<div style='font-size: 16px; font-weight: 800; color: var(--text-color, #0f172a); margin-top: 10px; margin-bottom: 6px;'>📊 Live Polling Results ({stats['total_votes']} total votes):</div>", unsafe_allow_html=True)
        for opt in options:
            opt_id = str(opt.get("id"))
            stat = stats["tallies"].get(opt_id, {"count": 0, "percent": 0.0})
            cnt = stat["count"]
            pct = stat["percent"]
            label = opt.get("label_short", opt.get("label", opt.get("name", f"Option {opt_id}")))
            if str(opt_id) in str(label):
                display_label = label
            else:
                display_label = f"{opt_id}: {label}"

            st.markdown(f"<div style='font-size: 15px; font-weight: 700; color: var(--text-color, #1e293b); margin-bottom: 4px;'>{display_label} &mdash; <span style='color: #0284c7; font-weight: 800;'>{cnt} votes ({pct:.1f}%)</span></div>", unsafe_allow_html=True)
            st.progress(pct / 100.0)

    st.markdown("---")


def _render_top_header(title: str, subtitle: str, role_key: str):
    """Renders a prominent header with a clear Refresh button at the top of the main body."""
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title(title)
        st.markdown(f"<div style='font-size: 15px; color: var(--text-color, #475569); opacity: 0.85; margin-top: -10px; margin-bottom: 14px;'>{subtitle}</div>", unsafe_allow_html=True)
    with col2:
        st.write("")
        if st.button("🔄 Refresh View", key=f"top_refresh_{role_key}", use_container_width=True):
            st.rerun()

# ---------------------------------------------------------
# 1. THREAT ACTOR (HACKER) TERMINAL
# ---------------------------------------------------------
@st.fragment(run_every=2)
def render_hacker_terminal(game: GameState, is_captain: bool, voter_id: str):
    _render_top_header("💀 Threat Actor Command Terminal", "Access Level: Adversary / Red Team Infiltration", "hackers")

    if game.phase == "lobby":
        st.warning("⏳ Simulation is in the Lobby. Standby for the Game Master to initiate Round 1.")
        return

    if game.phase == "game_over":
        st.success("🏁 Simulation Concluded! Enterprise impact debrief:")
        render_round_recap_card(game)
        render_final_hacker_action_card(game)
        render_acronym_glossary()
        return

    rem_secs = game.get_remaining_seconds()
    phase_label = "Hacker Exploitation" if game.phase == "hacker" else f"{game.phase.upper()} Phase"
    render_threatening_clock(rem_secs, game.phase_duration, phase_label, game.timer_paused)

    if game.phase == "recap":
        st.success("💥 Round Concluded! Enterprise impact debrief:")
        render_round_recap_card(game)
        st.info("⏳ Waiting for the Game Master to review incident debrief and advance the simulation...")
        render_acronym_glossary()
        return

    if game.phase == "final_hacker_action":
        st.subheader("⚡ Adversary Final Gambit: Press Attack or Retreat")
        st.caption("Your initial intrusion compromised CloudStore's perimeter. Decide whether to press the attack or retreat into the shadows:")

        exp_info = game.get_hacker_exposure_level()

        gambit_options = [
            {
                "id": "press",
                "label": f"🚀 Press the Attack (Secondary Exploit | {exp_info['level']} Catch Risk)",
                "label_short": "Press Attack",
                "desc": f"Execute secondary exploit payloads against payment APIs. Facing {exp_info['level']} detection risk due to cumulative attack signatures."
            },
            {
                "id": "retreat",
                "label": "🛑 Safe Strategic Retreat (Zero Risk Clean Escape)",
                "label_short": "Safe Retreat",
                "desc": "Sever C2 beacons, purge logs, and withdraw safely with existing spoils. Zero additional damage, clean adversary escape."
            }
        ]

        # Poll UI for final action
        _render_poll_ui(game, "hackers", is_captain, voter_id, gambit_options)

        g_cols = st.columns(2)
        with g_cols[0]:
            st.markdown(f"""
            <div style="background-color: #450a0a; border: 2px solid {exp_info['color']}; border-radius: 12px; padding: 18px; margin-bottom: 14px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: 800; color: #fca5a5; font-size: 18px;">🚀 Option 1: Press the Attack</span>
                    <span style="background-color: {exp_info['color']}; color: white; padding: 4px 10px; border-radius: 999px; font-size: 13px; font-weight: 800;">{exp_info['level']}</span>
                </div>
                <div style="color: #fecaca; font-size: 15px; margin-top: 8px; line-height: 1.4;">
                    Execute secondary exploits against payment endpoints and customer transaction ledgers.
                </div>
                <div style="margin-top: 10px; font-size: 14px; color: #ffffff; line-height: 1.5;">
                    <strong>Target Payload:</strong> Unchecked exfiltration of transactional reserves<br/>
                    <strong>⚠️ SOC Detection Warning:</strong> {exp_info['description']}<br/>
                    <em style="color: #cbd5e1; font-size: 13px;">*If intercepted, payloads are neutralized with zero additional damage while investigators recover enterprise assets.*</em>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if is_captain:
                if st.button("🚀 Authorize: Press the Attack", key="btn_hacker_press", type="primary", use_container_width=True):
                    game.submit_final_hacker_action("press")
                    st.rerun()
            else:
                st.caption("🔒 *Only the Team Captain can submit the final attack decision.*")

        with g_cols[1]:
            st.markdown("""
            <div style="background-color: #0f172a; border: 2px solid #475569; border-radius: 12px; padding: 18px; margin-bottom: 14px;">
                <div style="font-weight: 800; color: #f8fafc; font-size: 18px;">🛑 Option 2: Safe Strategic Retreat</div>
                <div style="color: #cbd5e1; font-size: 15px; margin-top: 8px; line-height: 1.4;">
                    Sever Command & Control (C2) beacons, wipe forensic trails, and withdraw into the dark web.
                </div>
                <div style="margin-top: 10px; font-size: 14px; color: #ffffff; line-height: 1.5;">
                    <strong>Campaign Outcome:</strong> Conclude intrusion campaign with current progress<br/>
                    <strong>Detection Risk:</strong> Zero risk. Clean adversary escape guaranteed.
                </div>
            </div>
            """, unsafe_allow_html=True)
            if is_captain:
                if st.button("🛑 Authorize: Safe Retreat", key="btn_hacker_retreat", type="secondary", use_container_width=True):
                    game.submit_final_hacker_action("retreat")
                    st.rerun()
            else:
                st.caption("🔒 *Only the Team Captain can submit the final attack decision.*")

        render_acronym_glossary()
        return

    if game.phase != "hacker":
        st.info("🔒 Attack vector deployed! Standing by while CloudStore's defenders react.")
        if game.selected_attack_data:
            att = game.selected_attack_data
            st.markdown(f"""
            <div style="background-color: #1e1b4b; border-left: 4px solid #818cf8; padding: 16px; border-radius: 10px; margin-bottom: 14px;">
                <div style="font-weight: 800; color: #ffffff; font-size: 17px;">ACTIVE PAYLOAD: {att.get('icon', '🚨')} {att.get('name')}</div>
                <div style="color: #c7d2fe; font-size: 15px; margin-top: 6px;">{att.get('description')}</div>
                <div style="display: flex; gap: 18px; margin-top: 10px; font-size: 14px; color: #e0e7ff;">
                    <span>🧩 Complexity: <strong>{att.get('complexity', 'Medium')}</strong></span>
                    <span>💥 Damage Potential: <strong>{att.get('damage_potential', 'High')}</strong></span>
                    <span>🕶️ Anonymity: <strong>{att.get('anonymity', 'Moderate')}</strong></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # C2 Wiretap Console during defender turns
        st.markdown("### 📡 Adversary C2 Surveillance Console")
        if game.phase == "it":
            st.code("""[C2 Beacon 10.14.0.22] Infiltration node active on CloudStore core subnet.
[Telemetry Intercept] SOC alert triggered: High-priority incident declared.
[Sensor Log] Monitoring IT containment responses...""", language="bash")
        elif game.phase == "exec":
            st.code("""[Signal Intercept] Executive boardroom emergency quorum active.
[Financial Telemetry] Board debating operational downtime vs breach disclosure.
[Market Feed] Volatility indicators rising...""", language="bash")
        elif game.phase == "media":
            st.code("""[Public Wire] Incident leaked to trade publications and wire desks.
[DarkNet Forum] Proof-of-concept exfiltration logs verified.
[PR Watch] Waiting for breaking media spin...""", language="bash")
        render_acronym_glossary()
        return

    st.subheader(f"Round {game.current_round}: Select Primary Infiltration Vector")
    round_attacks = ATTACKS.get(game.current_round, {})
    options_list = list(round_attacks.values())

    # Poll UI
    _render_poll_ui(game, "hackers", is_captain, voter_id, options_list)

    # Attack Vector Cards
    cols = st.columns(len(options_list))
    for idx, att in enumerate(options_list):
        with cols[idx]:
            att_id = att["id"]
            st.markdown(f"### {att.get('icon', '🅰️')} Vector {att_id}")
            st.markdown(f"**{att.get('name')}**")
            st.write(att.get("description", ""))

            st.markdown(f"""
            <div style="background-color: #111827; padding: 10px 14px; border-radius: 8px; border: 1px solid #1f2937; margin: 10px 0; font-size: 14px; color: #f1f5f9; line-height: 1.6;">
                <div>🧩 <strong>Complexity:</strong> {att.get('complexity', 'Medium')}</div>
                <div>💥 <strong>Damage Potential:</strong> {att.get('damage_potential', 'High')}</div>
                <div>🕶️ <strong>Anonymity:</strong> {att.get('anonymity', 'Moderate')}</div>
            </div>
            """, unsafe_allow_html=True)

            # Educational Dossier
            render_briefing_card("hackers", att.get("md_file", ""), att.get("name", ""), att.get("assessment", ""))

            if is_captain:
                if st.button(f"🚀 Deploy Vector {att_id}", key=f"btn_hacker_{att_id}", type="primary", use_container_width=True):
                    game.submit_hacker_attack(att_id)
                    st.success(f"Payload deployed: {att.get('name')}")
                    st.rerun()
            else:
                st.caption("🔒 *Only the Team Captain can submit the final attack decision.*")


# ---------------------------------------------------------
# 2. IT DEFENSE COMMAND TERMINAL
# ---------------------------------------------------------
@st.fragment(run_every=2)
def render_it_terminal(game: GameState, is_captain: bool, voter_id: str):
    _render_top_header("🛡️ IT Defense Command Terminal", "Access Level: Security Operations Center (SOC) / Incident Response", "it")

    if game.phase in ["lobby", "hacker"]:
        st.info("🟢 Network telemetry nominal. Awaiting detection alerts from perimeter intrusion sensors...")
        render_acronym_glossary()
        return

    if game.phase == "final_hacker_action":
        st.warning("⚠️ **ADVERSARY FINAL GAMBIT DETECTED:** Threat actors are positioning for a secondary attack or withdrawal. SOC sensors monitoring...")
        render_acronym_glossary()
        return

    if game.phase == "game_over":
        st.success("🏁 Simulation Concluded! Incident debrief:")
        render_round_recap_card(game)
        render_final_hacker_action_card(game)
        render_acronym_glossary()
        return

    rem_secs = game.get_remaining_seconds()
    phase_label = "IT Containment Deliberation" if game.phase == "it" else f"{game.phase.upper()} Phase"
    render_threatening_clock(rem_secs, game.phase_duration, phase_label, game.timer_paused)

    att = game.selected_attack_data or {}
    st.error(f"🚨 **ACTIVE BREACH DETECTED:** {att.get('icon', '🚨')} **{att.get('name', 'Breach')}** — {att.get('description', '')}")

    # Educational Technical Briefing Dossier
    render_briefing_card("it", att.get("md_file", ""), f"Technical Impact Analysis: {att.get('name', 'Incident')}", att.get("assessment", ""))

    if game.it_choice_id:
        st.success(f"✅ Technical containment proposed: **{game.it_choice_data.get('label', 'Action')}**.")
        if game.phase == "exec":
            st.info("⏳ Waiting for Executive Boardroom to review and issue binding governance directive...")
            render_acronym_glossary()
            return

        if game.phase in ["media", "recap"]:
            exec_act = (game.exec_action or "pending").lower()
            if exec_act == "approve":
                bg_color = "#064e3b"
                border_color = "#10b981"
                badge = "DIRECTIVE: APPROVED FULL CONTAINMENT"
                detail = "The Board approved your technical containment recommendation in full. Maximum threat mitigation is active."
            elif exec_act == "downgrade":
                bg_color = "#78350f"
                border_color = "#f59e0b"
                badge = "DIRECTIVE: DOWNGRADED FOR BUSINESS UPTIME"
                detail = "The Board compromised your containment plan to keep customer portals active. Threat mitigation was halved!"
            else:
                bg_color = "#7f1d1d"
                border_color = "#ef4444"
                badge = "DIRECTIVE: OVERRULED / DISMISSED"
                detail = "The Board rejected system isolations to avoid panic. Threat mitigation collapsed to 0%!"

            st.markdown(f"""
            <div style="background-color: {bg_color}; border: 2px solid {border_color}; border-radius: 12px; padding: 18px; margin: 14px 0;">
                <div style="font-size: 14px; font-weight: 800; color: #ffffff; text-transform: uppercase; letter-spacing: 0.1em;">🏢 EXECUTIVE BOARD DIRECTIVE ISSUED</div>
                <div style="font-size: 22px; font-weight: 800; color: #ffffff; margin-top: 4px;">{badge}</div>
                <div style="font-size: 15px; color: #f8fafc; margin-top: 6px; line-height: 1.4;">{detail}</div>
            </div>
            """, unsafe_allow_html=True)

            if game.phase == "media":
                st.info("⏳ Waiting for Media & PR Scrum to publish breaking news cycle...")
                render_acronym_glossary()
                return

            if game.phase == "recap":
                st.success("🏁 Round Concluded! Incident debrief:")
                render_round_recap_card(game)
                st.info("⏳ Waiting for the Game Master to review incident debrief and advance the simulation...")
                render_acronym_glossary()
                return

    st.subheader(f"Round {game.current_round}: Select Technical Containment Strategy")
    st.caption("⚠️ **Operational Trade-Off:** Strategic choices balance technical complexity, operational downtime, customer impact, and damage mitigation likelihood.")

    options = get_it_choices(game.current_round, game.selected_attack_key)

    # Poll UI
    _render_poll_ui(game, "it", is_captain, voter_id, options)

    for opt in options:
        opt_id = opt["id"]
        st.markdown(f"""
        <div style="background-color: #030712; padding: 18px 20px; border-radius: 12px; border-left: 4px solid #38bdf8; margin-bottom: 14px; border-top: 1px solid #1e293b; border-right: 1px solid #1e293b; border-bottom: 1px solid #1e293b;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 800; color: #f8fafc; font-size: 18px;">Option {opt_id}: {opt['label']}</span>
                <span style="background-color: #0369a1; color: white; padding: 4px 12px; border-radius: 999px; font-size: 14px; font-weight: 800;">Likelihood: {opt.get('mitigation_likelihood', 'Moderate')}</span>
            </div>
            <div style="color: #f1f5f9; font-size: 15px; margin-top: 8px; line-height: 1.4;">{opt.get('desc', '')}</div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 12px; font-size: 14px; line-height: 1.5;">
                <span style="color: #38bdf8;">⚙️ <strong>Complexity of Fix:</strong> {opt.get('complexity', 'Moderate')}</span>
                <span style="color: #f87171;">⏱️ <strong>Projected Downtime:</strong> {opt.get('downtime', 'Unknown')}</span>
                <span style="color: #fb923c;">👥 <strong>Impact on Customers:</strong> {opt.get('customer_impact', 'Noticeable')}</span>
                <span style="color: #a78bfa;">📉 <strong>Disruption:</strong> {opt.get('disruption', 'Disruption')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if is_captain:
            if st.button(f"Deploy & Recommend Option {opt_id}", key=f"btn_it_{opt_id}", type="primary", use_container_width=True):
                game.submit_it_choice(opt_id)
                st.rerun()
        else:
            st.caption(f"🔒 *Option {opt_id} available for voting in Straw Poll.*")

    render_acronym_glossary()


# ---------------------------------------------------------
# 3. EXECUTIVE BOARDROOM TERMINAL (ASYMMETRIC GOVERNANCE)
# ---------------------------------------------------------
@st.fragment(run_every=2)
def render_exec_terminal(game: GameState, is_captain: bool, voter_id: str):
    _render_top_header("💼 Executive Boardroom Terminal", "Access Level: Board of Directors / Chief Executive Office", "exec")

    if game.phase in ["lobby", "hacker"]:
        st.info("🟢 Board in routine session. Monitoring corporate risk posture.")
        render_acronym_glossary()
        return

    if game.phase == "it":
        st.warning("⚠️ Incident detected by SOC! Awaiting formal containment recommendation from IT Leadership...")
        render_acronym_glossary()
        return

    if game.phase == "final_hacker_action":
        st.warning("⚠️ **BOARDROOM CRISIS ALERT:** Adversary final gambit in progress. Awaiting intelligence on whether attackers press forward or retreat...")
        render_acronym_glossary()
        return

    if game.phase == "game_over":
        st.success(f"✅ Governance directive issued: **{game.exec_action.upper() if game.exec_action else 'N/A'}**.")
        render_round_recap_card(game)
        render_final_hacker_action_card(game)
        render_acronym_glossary()
        return

    if game.phase == "media":
        st.success(f"✅ Governance directive issued: **{game.exec_action.upper() if game.exec_action else 'N/A'}**.")
        st.info("⏳ Waiting for Media & PR Scrum to publish breaking news cycle...")
        render_acronym_glossary()
        return

    if game.phase == "recap":
        st.success(f"✅ Governance directive issued: **{game.exec_action.upper() if game.exec_action else 'N/A'}**.")
        render_round_recap_card(game)
        st.info("⏳ Waiting for the Game Master to review incident debrief and advance to the next round...")
        render_acronym_glossary()
        return

    rem_secs = game.get_remaining_seconds()
    phase_label = "Executive Crisis Governance" if game.phase == "exec" else f"{game.phase.upper()} Phase"
    render_threatening_clock(rem_secs, game.phase_duration, phase_label, game.timer_paused)

    att = game.selected_attack_data or {}
    it_plan = game.it_choice_data or {}

    st.error(f"🚨 **ENTERPRISE CRISIS ALERT:** {att.get('icon', '🚨')} **{att.get('name', 'Breach')}** — {att.get('description', '')}")

    # Educational Executive Risk Dossier (Dynamically incorporates chosen IT plan)
    render_briefing_card("exec", att.get("md_file", ""), f"Executive Risk Briefing: {att.get('name', 'Incident')}", "Review projected stock impact, customer sentiment, and regulatory compliance liabilities.", it_plan=it_plan)

    # Strategic Information Briefing: Execs focus on Stock Price Outlook & Customer Reputation
    st.markdown(f"""
    <div style="background-color: #1e1b4b; border: 2px solid #818cf8; padding: 22px; border-radius: 14px; margin: 14px 0;">
        <div style="font-size: 13px; font-weight: 800; color: #a5b4fc; text-transform: uppercase; letter-spacing: 0.1em;">IT PROPOSAL STRATEGIC IMPACT ASSESSMENT</div>
        <div style="font-size: 22px; font-weight: 800; color: #ffffff; margin-top: 4px;">Proposed Action: {it_plan.get('label', 'Emergency Plan')}</div>
        <div style="color: #f1f5f9; font-size: 15px; margin-top: 8px; line-height: 1.4;">{it_plan.get('exec_view', '')}</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 14px; padding: 14px; background-color: #312e81; border-radius: 10px;">
            <div>
                <div style="color: #93c5fd; font-weight: 800; font-size: 14px; letter-spacing: 0.05em;">📈 STOCK PRICE OUTLOOK</div>
                <div style="color: #ffffff; font-size: 14px; margin-top: 4px; line-height: 1.5;">{it_plan.get('stock_outlook', 'Equities market reaction subject to operational duration.')}</div>
            </div>
            <div>
                <div style="color: #fca5a5; font-weight: 800; font-size: 14px; letter-spacing: 0.05em;">🤝 CUSTOMER REPUTATION RISK</div>
                <div style="color: #ffffff; font-size: 14px; margin-top: 4px; line-height: 1.5;">{it_plan.get('reputation_risk', 'Public brand trust contingent on data protection integrity.')}</div>
            </div>
        </div>
        <div style="display: flex; gap: 20px; margin-top: 12px; font-size: 14px; color: #c7d2fe;">
            <span>⏱️ <strong>Est. Downtime:</strong> {it_plan.get('downtime', 'Pending')}</span>
            <span>👥 <strong>Customer Impact:</strong> {it_plan.get('customer_impact', 'Pending')}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if game.exec_action:
        st.success(f"✅ Governance directive issued: **{game.exec_action.upper()}**.")
        if game.phase == "media":
            st.info("⏳ Waiting for Media & PR Scrum to publish breaking news cycle...")
            render_acronym_glossary()
            return
        if game.phase == "recap":
            render_round_recap_card(game)
            render_acronym_glossary()
            return

    # Executive Pushback Pressure Alert based on IT choice severity
    it_opt_id = str(it_plan.get("id", "1"))
    disruption_pen = it_plan.get("disruption_penalty", 0)
    downtime_str = it_plan.get("downtime", "Operational Downtime")
    impact_str = it_plan.get("customer_impact", "Noticeable Disruption")

    if it_opt_id == "1" or disruption_pen <= -3:
        st.markdown(f"""
        <div style="background-color: #450a0a; border: 2px solid #ef4444; border-radius: 12px; padding: 18px; margin: 14px 0;">
            <div style="font-size: 13px; font-weight: 800; color: #fca5a5; text-transform: uppercase; letter-spacing: 0.1em;">
                ⚠️ EXECUTIVE PUSHBACK PRESSURE &bull; BOARDROOM CRISIS DILEMMA
            </div>
            <div style="font-size: 17px; font-weight: 800; color: #ffffff; margin-top: 4px;">
                Commercial & Shareholder Pushback: Severe Alarm Over Proposed System Lockdown
            </div>
            <div style="font-size: 15px; color: #fecaca; margin-top: 6px; line-height: 1.5;">
                IT's recommended plan imposes <strong>{downtime_str}</strong> and <strong>{impact_str}</strong>. Shareholder representatives and retail executives are fiercely urging the Board to push back against a full freeze, warning of immediate quarterly revenue collapse, credit downgrades, and public panic. The Board must decide whether to absorb the financial hit to guarantee threat containment, force a compromise, or overrule IT to protect business continuity.
            </div>
        </div>
        """, unsafe_allow_html=True)
    elif it_opt_id == "3" or it_plan.get("mitigation_pct", 0.6) <= 0.35:
        st.markdown(f"""
        <div style="background-color: #78350f; border: 2px solid #f59e0b; border-radius: 12px; padding: 18px; margin: 14px 0;">
            <div style="font-size: 13px; font-weight: 800; color: #fde68a; text-transform: uppercase; letter-spacing: 0.1em;">
                ⚠️ BOARD COMPLACENCY WARNING &bull; INACTION BACKFIRE RISK
            </div>
            <div style="font-size: 17px; font-weight: 800; color: #ffffff; margin-top: 4px;">
                IT Recommends Passive Monitoring: Minimal Containment Posture
            </div>
            <div style="font-size: 15px; color: #fef3c7; margin-top: 6px; line-height: 1.5;">
                IT proposes zero downtime and silent observation ({it_plan.get('label', 'Passive Approach')}). While storefront transactions continue uninterrupted, adversaries operate almost unhindered. Endorsing this low-mitigation strategy risks an <strong>Inaction Backfire Penalty (+5% to +25% damage)</strong> as the uncontained breach deepens.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background-color: #1e1b4b; border: 2px solid #818cf8; border-radius: 12px; padding: 18px; margin: 14px 0;">
            <div style="font-size: 13px; font-weight: 800; color: #a5b4fc; text-transform: uppercase; letter-spacing: 0.1em;">
                ⚖️ BOARDROOM DELIBERATION &bull; TARGETED MITIGATION TRADE-OFF
            </div>
            <div style="font-size: 17px; font-weight: 800; color: #ffffff; margin-top: 4px;">
                Targeted Quarantine Proposed: Moderate Operational Disruption
            </div>
            <div style="font-size: 15px; color: #c7d2fe; margin-top: 6px; line-height: 1.5;">
                IT recommends targeted quarantine ({downtime_str}). The Board must evaluate whether to fully back IT's technical isolation, push for faster reconnection to preserve revenue, or overrule containment entirely.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Select Binding Corporate Governance Directive")
    st.caption("Decide whether to authorize IT's technical recommendation, force an operational compromise, or overrule IT to protect continuity:")

    options = get_exec_governance_options(it_plan)

    # Poll UI
    _render_poll_ui(game, "exec", is_captain, voter_id, options)

    for opt in options:
        opt_id = opt["id"]
        tagline = opt.get("tagline", "")
        tagline_html = f"<div style='font-size: 13px; font-weight: 700; color: #38bdf8; margin-bottom: 4px;'>{tagline}</div>" if tagline else ""
        st.markdown(f"""
        <div style="background-color: #030712; padding: 18px 20px; border-radius: 12px; border-left: 4px solid #818cf8; margin-bottom: 14px; border-top: 1px solid #1e293b; border-right: 1px solid #1e293b; border-bottom: 1px solid #1e293b;">
            {tagline_html}
            <div style="font-weight: 800; color: #f8fafc; font-size: 17px;">{opt['label']}</div>
            <div style="color: #f1f5f9; font-size: 15px; margin-top: 6px; line-height: 1.4;">{opt['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

        if is_captain:
            if st.button(f"Authorize Directive: {opt['label']}", key=f"btn_exec_{opt_id}", type="primary", use_container_width=True):
                game.submit_exec_choice(opt_id)
                st.rerun()
        else:
            st.caption(f"🔒 *Directive {opt['label']} open for voting in Straw Poll.*")

    render_acronym_glossary()


# ---------------------------------------------------------
# 4. MEDIA & PR SCRUM TERMINAL
# ---------------------------------------------------------
@st.fragment(run_every=2)
def render_media_terminal(game: GameState, is_captain: bool, voter_id: str):
    _render_top_header("🎤 Media & PR Press Scrum", "Access Level: Public Affairs / Investigative Journalism Desk", "media")

    if game.phase in ["lobby", "hacker", "it"]:
        st.info("📡 Monitoring live news wires. Waiting for executive statements from CloudStore leadership...")
        render_acronym_glossary()
        return

    if game.phase == "exec":
        st.warning("📡 Executive Board is currently voting behind closed doors. Press scrum convening...")
        render_acronym_glossary()
        return

    if game.phase == "final_hacker_action":
        st.warning("📡 **NEWS WIRE BULLETIN:** Unconfirmed chatter on dark web forums suggests threat actors are executing a final maneuver...")
        render_acronym_glossary()
        return

    if game.phase == "game_over":
        st.success("📰 Breaking story published! Live impact debrief:")
        render_round_recap_card(game)
        render_final_hacker_action_card(game)
        render_acronym_glossary()
        return

    if game.phase == "recap":
        st.success("📰 Breaking story published! Live impact debrief:")
        render_round_recap_card(game)
        st.info("⏳ Waiting for the Game Master to review incident debrief and advance the simulation...")
        render_acronym_glossary()
        return

    # Breaking Wire & Executive Governance Briefing Card
    att = game.selected_attack_data or {}
    exec_act = (game.exec_action or "pending").upper()
    st.markdown(f"""
    <div style="background-color: #1e1b4b; border: 2px solid #818cf8; border-radius: 12px; padding: 18px; margin-bottom: 14px;">
        <div style="font-size: 13px; font-weight: 800; color: #a5b4fc; text-transform: uppercase; letter-spacing: 0.1em;">📡 BREAKING INTELLIGENCE WIRE</div>
        <div style="font-size: 18px; font-weight: 800; color: #ffffff; margin-top: 4px;">Incident: {att.get('icon', '🚨')} {att.get('name', 'Breach In Progress')}</div>
        <div style="font-size: 15px; color: #c7d2fe; margin-top: 6px;">Executive Board Directive: <strong>{exec_act}</strong></div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader(f"Round {game.current_round}: Select Breaking News Headline")
    st.caption("Choose which journalistic angle leads the front page. Real-world public resonance and viral reach remain unpredictable until news breaks.")

    headlines = DYNAMIC_HEADLINES.get(game.current_round, [])

    # Poll UI
    _render_poll_ui(game, "media", is_captain, voter_id, headlines)

    for idx, item in enumerate(headlines):
        head_label = item.get("id", f"Headline {idx + 1}")
        disp = item.get("disposition", "Neutral")
        disp_color = "#ef4444" if disp == "Negative" else "#10b981" if disp == "Positive" else "#38bdf8"

        st.markdown(f"""
        <div style="background-color: #030712; padding: 18px 20px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center;">
            <div style="flex-grow: 1; margin-right: 14px;">
                <span style="font-size: 14px; font-weight: 800; color: {disp_color}; text-transform: uppercase;">{head_label} &bull; {disp} Tone ({item.get('tier', 'News')})</span><br/>
                <span style="font-size: 18px; font-weight: 800; color: #f8fafc;">\"{item['headline']}\"</span>
                <div style="font-size: 14px; color: #cbd5e1; margin-top: 4px;">{item.get('desc', '')}</div>
            </div>
            <span style="background-color: #1e293b; border: 1px solid #334155; color: #f1f5f9; padding: 6px 12px; border-radius: 999px; font-size: 13px; font-weight: 800; white-space: nowrap;">📡 Virality: Unpredictable</span>
        </div>
        """, unsafe_allow_html=True)

        if is_captain:
            if st.button(f"Publish {head_label}", key=f"btn_media_{idx}", type="primary", use_container_width=True):
                game.submit_media_choice(idx)
                st.rerun()
        else:
            st.caption(f"🔒 *{head_label} open for voting in Straw Poll.*")
