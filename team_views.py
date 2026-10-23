"""
team_views.py
Role-specific terminals for Threat Actors, IT Defense, Executive Board, and Media
Includes single-URL Captain vs Viewer modes, live straw polling, and asymmetric information flow.
"""

import streamlit as st
from typing import Dict, Any, List
from state_manager import GameState
from game_data import ATTACKS, IT_CHOICES, EXEC_GOVERNANCE_OPTIONS, DYNAMIC_HEADLINES
from ui_components import render_threatening_clock, render_briefing_card

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
                label = opt.get("label", opt.get("name", f"Option {opt_id}"))
                is_selected = (current_vote == opt_id)
                btn_type = "primary" if is_selected else "secondary"
                btn_label = f"✅ Voted: {opt_id}" if is_selected else f"Vote: {opt_id}"

                if st.button(btn_label, key=f"vote_btn_{role}_{opt_id}", type=btn_type, use_container_width=True):
                    game.cast_vote(role, voter_id, opt_id)
                    st.rerun()

    # Live Bar Chart of Votes (Visible to everyone)
    if stats["total_votes"] > 0:
        st.markdown(f"**Live Polling Results ({stats['total_votes']} total votes):**")
        for opt in options:
            opt_id = str(opt.get("id"))
            stat = stats["tallies"].get(opt_id, {"count": 0, "percent": 0.0})
            cnt = stat["count"]
            pct = stat["percent"]
            label = opt.get("label", opt.get("name", f"Option {opt_id}"))

            st.write(f"**{opt_id}: {label}** — {cnt} votes ({pct:.1f}%)")
            st.progress(pct / 100.0)

    st.markdown("---")


# ---------------------------------------------------------
# 1. THREAT ACTOR (HACKER) TERMINAL
# ---------------------------------------------------------
def render_hacker_terminal(game: GameState, is_captain: bool, voter_id: str):
    st.title("💀 Threat Actor Command Terminal")
    st.caption("Access Level: Adversary / Red Team Infiltration")

    if game.phase == "lobby":
        st.warning("⏳ Simulation is in the Lobby. Standby for the Game Master to initiate Round 1.")
        return

    rem_secs = game.get_remaining_seconds()
    render_threatening_clock(rem_secs, game.phase_duration, "Hacker Exploitation", game.timer_paused)

    if game.phase != "hacker":
        st.info("🔒 Attack vector deployed! Standing by while CloudStore's defenders react.")
        if game.selected_attack_data:
            att = game.selected_attack_data
            st.markdown(f"""
            <div style="background-color: #1e1b4b; border-left: 4px solid #818cf8; padding: 14px; border-radius: 8px;">
                <div style="font-weight: 800; color: #ffffff;">ACTIVE PAYLOAD: {att.get('icon', '🚨')} {att.get('name')}</div>
                <div style="color: #c7d2fe; font-size: 13px; margin-top: 4px;">{att.get('description')}</div>
            </div>
            """, unsafe_allow_html=True)
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
            st.caption(f"**Threat Damage:** {att.get('damage')} Enterprise HP")
            
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
def render_it_terminal(game: GameState, is_captain: bool, voter_id: str):
    st.title("🛡️ IT Defense Command Terminal")
    st.caption("Access Level: Security Operations Center (SOC) / Incident Response")

    if game.phase in ["lobby", "hacker"]:
        st.info("🟢 Network telemetry nominal. Awaiting detection alerts from perimeter intrusion sensors...")
        return

    rem_secs = game.get_remaining_seconds()
    render_threatening_clock(rem_secs, game.phase_duration, "IT Containment Deliberation", game.timer_paused)

    att = game.selected_attack_data or {}
    st.error(f"🚨 **ACTIVE BREACH DETECTED:** {att.get('icon', '🚨')} **{att.get('name', 'Breach')}** — {att.get('description', '')}")

    if game.it_choice_id:
        st.success(f"✅ Technical containment proposed: **{game.it_choice_data.get('label', 'Action')}**.")
        st.info("⏳ Waiting for Executive Boardroom to review and issue binding governance directive...")
        return

    st.subheader(f"Round {game.current_round}: Select Technical Containment Strategy")
    st.caption("⚠️ **Operational Trade-Off Rule:** Aggressive options with severe downtime provide the highest threat mitigation!")

    options = IT_CHOICES.get(game.current_round, [])

    # Poll UI
    _render_poll_ui(game, "it", is_captain, voter_id, options)

    for opt in options:
        opt_id = opt["id"]
        mit_pct = int(opt["mitigation_pct"] * 100)
        st.markdown(f"""
        <div style="background-color: #030712; padding: 16px; border-radius: 12px; border-left: 4px solid #38bdf8; margin-bottom: 12px; border-top: 1px solid #1e293b; border-right: 1px solid #1e293b; border-bottom: 1px solid #1e293b;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: 800; color: #f8fafc; font-size: 16px;">Option {opt_id}: {opt['label']}</span>
                <span style="background-color: #0369a1; color: white; padding: 3px 8px; border-radius: 999px; font-size: 11px; font-weight: 800;">Mitigates {mit_pct}% Damage</span>
            </div>
            <div style="color: #cbd5e1; font-size: 13px; margin-top: 6px;">{opt.get('desc', '')}</div>
            <div style="display: flex; gap: 16px; margin-top: 8px; font-size: 12px;">
                <span style="color: #f87171; font-weight: 700;">⏱️ Est. Downtime: {opt.get('downtime', 'Unknown')}</span>
                <span style="color: #fb923c; font-weight: 700;">📉 {opt.get('disruption', '')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if is_captain:
            if st.button(f"Deploy & Recommend Option {opt_id}", key=f"btn_it_{opt_id}", type="primary", use_container_width=True):
                game.submit_it_choice(opt_id)
                st.rerun()
        else:
            st.caption(f"🔒 *Option {opt_id} available for voting in Straw Poll.*")


# ---------------------------------------------------------
# 3. EXECUTIVE BOARDROOM TERMINAL (ASYMMETRIC GOVERNANCE)
# ---------------------------------------------------------
def render_exec_terminal(game: GameState, is_captain: bool, voter_id: str):
    st.title("💼 Executive Boardroom Terminal")
    st.caption("Access Level: Board of Directors / Chief Executive Office")

    if game.phase in ["lobby", "hacker"]:
        st.info("🟢 Board in routine session. Monitoring corporate risk posture.")
        return

    if game.phase == "it":
        st.warning("⚠️ Incident detected by SOC! Awaiting formal containment recommendation from IT Leadership...")
        return

    rem_secs = game.get_remaining_seconds()
    render_threatening_clock(rem_secs, game.phase_duration, "Executive Crisis Governance", game.timer_paused)

    att = game.selected_attack_data or {}
    it_plan = game.it_choice_data or {}

    st.error(f"🚨 **ENTERPRISE CRISIS ALERT:** {att.get('icon', '🚨')} **{att.get('name', 'Breach')}** — {att.get('description', '')}")

    # Asymmetric Information Briefing: Execs see IT downtime & disruption, but NOT protection %!
    st.markdown(f"""
    <div style="background-color: #1e1b4b; border: 2px solid #818cf8; padding: 18px; border-radius: 12px; margin: 12px 0;">
        <div style="font-size: 11px; font-weight: 800; color: #a5b4fc; text-transform: uppercase; letter-spacing: 0.1em;">IT DEPARTMENT DIRECTIVE PROPOSAL</div>
        <div style="font-size: 20px; font-weight: 800; color: #ffffff; margin-top: 4px;">Proposed Action: {it_plan.get('label', 'Emergency Plan')}</div>
        <div style="color: #e0e7ff; font-size: 14px; margin-top: 8px;">{it_plan.get('exec_view', '')}</div>
        <div style="margin-top: 10px; padding: 8px 12px; background-color: #312e81; border-radius: 6px; font-size: 12px; color: #c7d2fe;">
            🔒 <strong>Technical Security Effectiveness:</strong> <em>[CLASSIFIED BY IT — HIDDEN FROM BOARD]</em>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if game.exec_action:
        st.success(f"✅ Governance directive issued: **{game.exec_action.upper()}**.")
        st.info("⏳ Waiting for Media & PR Scrum to publish breaking news cycle...")
        return

    st.subheader("Select Binding Corporate Governance Directive")
    st.caption("Decide whether to authorize IT's disruptive system shutdown or overrule them to preserve business operations:")

    options = EXEC_GOVERNANCE_OPTIONS

    # Poll UI
    _render_poll_ui(game, "exec", is_captain, voter_id, options)

    for opt in options:
        opt_id = opt["id"]
        st.markdown(f"""
        <div style="background-color: #030712; padding: 14px; border-radius: 12px; border-left: 4px solid #818cf8; margin-bottom: 10px; border-top: 1px solid #1e293b; border-right: 1px solid #1e293b; border-bottom: 1px solid #1e293b;">
            <div style="font-weight: 800; color: #f8fafc; font-size: 15px;">{opt['label']}</div>
            <div style="color: #cbd5e1; font-size: 13px; margin-top: 4px;">{opt['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

        if is_captain:
            if st.button(f"Authorize Directive: {opt['label']}", key=f"btn_exec_{opt_id}", type="primary", use_container_width=True):
                game.submit_exec_choice(opt_id)
                st.rerun()
        else:
            st.caption(f"🔒 *Directive {opt['label']} open for voting in Straw Poll.*")


# ---------------------------------------------------------
# 4. MEDIA & PR SCRUM TERMINAL
# ---------------------------------------------------------
def render_media_terminal(game: GameState, is_captain: bool, voter_id: str):
    st.title("🎤 Media & PR Press Scrum")
    st.caption("Access Level: Public Affairs / Investigative Journalism Desk")

    if game.phase in ["lobby", "hacker", "it"]:
        st.info("📡 Monitoring live news wires. Waiting for executive statements from CloudStore leadership...")
        return

    if game.phase == "exec":
        st.warning("📡 Executive Board is currently voting behind closed doors. Press scrum convening...")
        return

    rem_secs = game.get_remaining_seconds()
    render_threatening_clock(rem_secs, game.phase_duration, "Breaking News Publication", game.timer_paused)

    att = game.selected_attack_data or {}
    exec_act = game.exec_action or "Unknown"

    st.markdown(f"""
    <div style="background-color: #172554; border: 2px solid #3b82f6; padding: 14px; border-radius: 12px; margin-bottom: 14px;">
        <div style="font-size: 11px; font-weight: 800; color: #93c5fd; text-transform: uppercase;">BREAKING INTELLIGENCE WIRE</div>
        <div style="font-size: 18px; font-weight: 800; color: #ffffff; margin-top: 2px;">{att.get('name', 'Incident')}</div>
        <div style="color: #bfdbfe; font-size: 13px; margin-top: 4px;">Executive Board Directive Issued: <strong>{exec_act.upper()}</strong></div>
    </div>
    """, unsafe_allow_html=True)

    if game.phase == "recap":
        st.success("📰 Breaking story published! View Mission Control projector for the impact on Company Health.")
        return

    st.subheader(f"Round {game.current_round}: Select Breaking News Headline")
    st.caption("Choose which journalistic angle leads the front page (helps or hurts the enterprise):")

    headlines = DYNAMIC_HEADLINES.get(game.current_round, [])

    # Poll UI
    _render_poll_ui(game, "media", is_captain, voter_id, headlines)

    for idx, item in enumerate(headlines):
        delta = item.get("health_delta", 0)
        delta_str = f"+{delta}" if delta > 0 else f"{delta}"
        badge_color = "#10b981" if delta > 0 else "#64748b" if delta == 0 else "#ef4444"

        st.markdown(f"""
        <div style="background-color: #030712; padding: 14px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-size: 15px; font-weight: 800; color: #f8fafc;">\"{item['headline']}\"</span>
                <div style="font-size: 12px; color: #94a3b8; margin-top: 2px;">{item.get('desc', '')}</div>
            </div>
            <span style="background-color: {badge_color}; color: white; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 800; white-space: nowrap;">Health {delta_str}</span>
        </div>
        """, unsafe_allow_html=True)

        if is_captain:
            if st.button(f"Publish Headline #{idx + 1}", key=f"btn_media_{idx}", type="primary", use_container_width=True):
                game.submit_media_choice(idx)
                st.rerun()
        else:
            st.caption(f"🔒 *Headline #{idx + 1} open for voting in Straw Poll.*")
