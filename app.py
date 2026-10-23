"""
CloudStore Command: Mission Control
Multiplayer Cyber Incident Response Tabletop Simulation
Streamlit Application
"""

import streamlit as st
import uuid
from typing import Dict, Any, Optional

from state_manager import GameState
from game_data import TEAM_CODES
from scoring_engine import evaluate_final_outcome, get_outcome_thresholds
from ui_components import render_threatening_clock, render_health_gauge
from team_views import (
    render_hacker_terminal,
    render_it_terminal,
    render_exec_terminal,
    render_media_terminal
)

# ---------------------------------------------------------
# GLOBAL SINGLETON GAME STATE
# ---------------------------------------------------------
@st.cache_resource
def get_global_game() -> GameState:
    return GameState()

# ---------------------------------------------------------
# GM PROJECTOR & MISSION CONTROL SCOREBOARD
# ---------------------------------------------------------
def render_main_dashboard(game: GameState):
    st.title("🛡️ CloudStore Command: Mission Control")
    st.caption("Live Operational Cyber Incident Response Tabletop Simulation")

    # Threatening Countdown Clock
    rem_secs = game.get_remaining_seconds()
    phase_labels = {
        "lobby": "Lobby Briefing",
        "hacker": "Threat Actor Infiltration",
        "it": "IT Containment Deliberation",
        "exec": "Executive Crisis Governance",
        "media": "Press Scrum & Media Spin",
        "recap": "Round Assessment",
        "game_over": "Simulation Concluded"
    }
    render_threatening_clock(
        rem_secs,
        game.phase_duration,
        phase_labels.get(game.phase, game.phase),
        game.timer_paused
    )

    # Primary Company Health Score
    b_cutoff, w_cutoff = get_outcome_thresholds(game.max_rounds)
    render_health_gauge(game.company_health, b_cutoff, w_cutoff)

    # Real-Time Team Status Telemetry Badges
    st.markdown("### 📡 Live Team Deliberation Telemetry")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"**💀 Threat Actors:**")
        st.info(game.team_status.get("hackers", "Standby"))
    with col2:
        st.markdown(f"**🛡️ IT Defense:**")
        st.info(game.team_status.get("it", "Standby"))
    with col3:
        st.markdown(f"**💼 Executive Board:**")
        st.info(game.team_status.get("exec", "Standby"))
    with col4:
        st.markdown(f"**🎤 Media & PR:**")
        st.info(game.team_status.get("media", "Standby"))

    st.markdown("---")

    # Final Outcome Assessment Screen
    if game.phase == "game_over":
        tier, title, desc = evaluate_final_outcome(game.company_health, game.max_rounds)
        if tier == "Win":
            box_color = "#065f46"
            border_color = "#10b981"
            badge = "🏆 MISSION SUCCESS — ENTERPRISE PREVAILED"
        elif tier == "Survive":
            box_color = "#78350f"
            border_color = "#f59e0b"
            badge = "🛡️ SURVIVED — ENTERPRISE DAMAGED BUT SOLVENT"
        else:
            box_color = "#7f1d1d"
            border_color = "#ef4444"
            badge = "💥 CATASTROPHIC FAILURE — BANKRUPTCY DECLARED"

        st.markdown(f"""
        <div style="background-color: {box_color}; border: 3px solid {border_color}; border-radius: 16px; padding: 24px; text-align: center; margin: 20px 0;">
            <div style="font-size: 14px; font-weight: 800; color: #ffffff; letter-spacing: 0.15em;">{badge}</div>
            <div style="font-size: 32px; font-weight: 900; color: #ffffff; margin-top: 6px;">{title}</div>
            <div style="font-size: 16px; color: #f8fafc; max-width: 750px; margin: 12px auto 0 auto; line-height: 1.5;">{desc}</div>
            <div style="font-size: 20px; font-weight: 800; color: #fde68a; margin-top: 14px;">Final Company Health: {game.company_health:.1f} / 100.0 HP</div>
        </div>
        """, unsafe_allow_html=True)

    # Active Incident Alert Card
    if game.selected_attack_data:
        att = game.selected_attack_data
        st.markdown(f"""
        <div style="background-color: #450a0a; border: 2px solid #ef4444; border-radius: 12px; padding: 18px; margin: 12px 0;">
            <div style="font-size: 11px; font-weight: 800; color: #fca5a5; text-transform: uppercase; letter-spacing: 0.1em;">ACTIVE ENTERPRISE BREACH</div>
            <div style="font-size: 22px; font-weight: 800; color: #ffffff; margin-top: 4px;">{att.get('icon', '🚨')} {att.get('name', 'Incident Alert')}</div>
            <div style="font-size: 14px; color: #fecaca; margin-top: 6px;">{att.get('description', '')}</div>
        </div>
        """, unsafe_allow_html=True)

    # Incident History Log
    if game.history:
        st.markdown("### 📜 Incident Chronology & Round Impact")
        for entry in reversed(game.history):
            with st.expander(f"Round {entry['round']}: {entry['attack_name']} (Net Delta: {entry['net_delta']:+g} HP)", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Threat Vector:** {entry['attack_name']} ({entry['attack_damage']:+g} HP)")
                    st.write(f"**IT Defense Proposal:** {entry['it_plan']} (Mitigated: +{entry['it_mitigated']:g} HP, Disruption: {entry['disruption_penalty']:+g} HP)")
                    st.write(f"**Executive Governance:** {entry['exec_decision']}")
                    st.write(f"**Media Headline:** \"{entry['headline']}\" ({entry['media_delta']:+g} HP)")
                    st.caption(f"Real-World Execution Friction Roll: {entry['friction']:+g} HP")
                with c2:
                    delta_color = "green" if entry['net_delta'] >= 0 else "red"
                    st.markdown(f"**Net Health Change:** <span style='font-size: 22px; font-weight: 800; color:{delta_color};'>{entry['net_delta']:+g} HP</span>", unsafe_allow_html=True)
                    st.write(f"Health Before: **{entry['health_before']:.1f}** &nbsp;→&nbsp; Health After: **{entry['health_after']:.1f}**")
                    st.caption(f"Threat Multiplier: {entry['multiplier']}x")

# ---------------------------------------------------------
# MAIN APP ENTRYPOINT
# ---------------------------------------------------------
def main():
    st.set_page_config(
        page_title="CloudStore Command: Mission Control",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    game = get_global_game()

    # Session persistent voter ID for straw polls
    if "voter_id" not in st.session_state:
        st.session_state["voter_id"] = str(uuid.uuid4())
    voter_id = st.session_state["voter_id"]

    # 1. Resolve Team/Role from URL Query Parameter (?team=...)
    try:
        url_role = st.query_params.get("team", "")
    except Exception:
        url_role = ""
    url_role = str(url_role).lower().strip()

    is_team_url = url_role in ["hackers", "it", "exec", "media"]

    # ---------------------------------------------------------
    # DEDICATED TEAM TERMINAL VIEW (SINGLE URL: VIEWER / CAPTAIN)
    # ---------------------------------------------------------
    if is_team_url:
        captain_key = f"is_captain_{url_role}"
        if captain_key not in st.session_state:
            st.session_state[captain_key] = False

        st.sidebar.title("🔐 Team Access")
        st.sidebar.success(f"Team: **{url_role.upper()}**")
        st.sidebar.caption(f"Round: **{game.current_round} / {game.max_rounds}**")
        st.sidebar.caption(f"Phase: **{game.phase.upper()}**")

        # Captain Authentication Toggle
        st.sidebar.markdown("---")
        if st.session_state[captain_key]:
            st.sidebar.success("⭐ **CAPTAIN MODE UNLOCKED**")
            st.sidebar.caption("You have authorization to launch team polls and submit binding decisions.")
            if st.sidebar.button("Relinquish Captain Role", use_container_width=True):
                st.session_state[captain_key] = False
                st.rerun()
        else:
            st.sidebar.info("👁️ **VIEWER MODE (TEAM MEMBER)**")
            st.sidebar.caption("You can read scenario intelligence and cast advisory votes in Straw Polls.")
            pwd_input = st.sidebar.text_input(
                "Captain Passcode",
                type="password",
                key=f"pwd_entry_{url_role}",
                help="Enter your team passcode to unlock Captain controls."
            )
            correct_pwd = TEAM_CODES.get(url_role, "")
            if st.sidebar.button("Unlock Captain Role", type="primary", use_container_width=True):
                if pwd_input == correct_pwd:
                    st.session_state[captain_key] = True
                    st.rerun()
                else:
                    st.sidebar.error("❌ Invalid Captain Passcode.")

        st.sidebar.markdown("---")
        if st.sidebar.button("🔄 Refresh View", use_container_width=True):
            st.rerun()

        if st.sidebar.button("🎮 Switch to GM Mode", use_container_width=True):
            st.query_params["team"] = "main"
            st.rerun()

        # Render specific team terminal view
        is_capt = st.session_state[captain_key]
        if url_role == "hackers":
            render_hacker_terminal(game, is_capt, voter_id)
        elif url_role == "it":
            render_it_terminal(game, is_capt, voter_id)
        elif url_role == "exec":
            render_exec_terminal(game, is_capt, voter_id)
        elif url_role == "media":
            render_media_terminal(game, is_capt, voter_id)
        return

    # ---------------------------------------------------------
    # GM MISSION CONTROL & PROJECTOR VIEW
    # ---------------------------------------------------------
    st.sidebar.title("🎮 Game Master (GM) Console")

    if "admin_authenticated" not in st.session_state:
        st.session_state["admin_authenticated"] = False

    correct_admin_code = TEAM_CODES.get("main", "admin123")

    if not st.session_state["admin_authenticated"]:
        st.sidebar.caption("🔒 GM Passcode Required")
        admin_pwd = st.sidebar.text_input("Admin Password", type="password", key="admin_pwd_main")
        if st.sidebar.button("🔓 Unlock GM Console", type="primary", use_container_width=True):
            if admin_pwd in [correct_admin_code, "admin"]:
                st.session_state["admin_authenticated"] = True
                st.rerun()
            else:
                st.sidebar.error("❌ Incorrect Admin Password.")

        st.sidebar.info("🔒 Enter Admin Password to reveal shareable team URLs and simulation controls.")
        render_main_dashboard(game)
        return

    # Authenticated GM Controls
    st.sidebar.success("🔓 GM Console Unlocked")
    if st.sidebar.button("🔒 Lock Console", use_container_width=True):
        st.session_state["admin_authenticated"] = False
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Round:** {game.current_round} / {game.max_rounds} &nbsp;|&nbsp; **Phase:** `{game.phase.upper()}`")

    # Round Management
    st.sidebar.markdown("### 🕹️ Round Management")
    if game.phase == "lobby":
        game.max_rounds = st.sidebar.radio("Session Round Count", options=[2, 3], index=[2, 3].index(game.max_rounds))
        if st.sidebar.button("🚀 Start Round 1 (Launch Infiltration)", type="primary", use_container_width=True):
            game.start_phase("hacker")
            st.rerun()
    elif game.phase == "recap":
        next_label = "🏁 Conclude Game" if game.current_round >= game.max_rounds else f"Start Round {game.current_round + 1}"
        if st.sidebar.button(f"➡️ {next_label}", type="primary", use_container_width=True):
            game.advance_to_next_round()
            st.rerun()
    elif game.phase == "game_over":
        st.sidebar.success("🏁 Simulation Finished!")
    else:
        st.sidebar.info(f"Awaiting team inputs for: **{game.phase.upper()}**")

    # Threat Multiplier
    game.multiplier = st.sidebar.selectbox(
        "⚡ Threat Severity Multiplier",
        options=[1.0, 1.2, 1.5, 2.0],
        index=[1.0, 1.2, 1.5, 2.0].index(game.multiplier) if game.multiplier in [1.0, 1.2, 1.5, 2.0] else 0,
        format_func=lambda x: f"{x}x Intensity"
    )

    # Timer Controls (Pause / Resume / Reset)
    st.sidebar.markdown("### ⏱️ Timer Controls")
    col_t1, col_t2 = st.sidebar.columns(2)
    with col_t1:
        if game.timer_paused:
            if st.button("▶️ Resume", use_container_width=True):
                game.resume_timer()
                st.rerun()
        else:
            if st.button("⏸️ Pause", use_container_width=True):
                game.pause_timer()
                st.rerun()
    with col_t2:
        if st.button("🔄 Reset Timer", use_container_width=True):
            game.reset_timer()
            st.rerun()

    # Undo & Reset
    st.sidebar.markdown("---")
    col_u, col_r = st.sidebar.columns(2)
    with col_u:
        if st.button("↩️ Undo", use_container_width=True, disabled=len(game.snapshots) == 0):
            if game.undo_last_round():
                st.success("Rolled back.")
                st.rerun()
    with col_r:
        if st.button("🔄 Reset Sim", use_container_width=True):
            game.reset(max_rounds=game.max_rounds)
            st.rerun()

    # Shareable Team URLs
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔗 Shareable Team URLs")
    st.sidebar.caption("Distribute one link per team. Students join as Viewers; Captains unlock via passcode:")

    base_url = "https://cyberattacksim.streamlit.app"
    team_links = {
        f"💀 Threat Actors (Passcode: {TEAM_CODES['hackers']})": f"{base_url}/?team=hackers",
        f"🛡️ IT Defense (Passcode: {TEAM_CODES['it']})": f"{base_url}/?team=it",
        f"💼 Executive Board (Passcode: {TEAM_CODES['exec']})": f"{base_url}/?team=exec",
        f"🎤 Media & PR (Passcode: {TEAM_CODES['media']})": f"{base_url}/?team=media",
        f"🎮 GM Projector": f"{base_url}/?team=main"
    }

    for label, link in team_links.items():
        with st.sidebar.expander(label, expanded=False):
            st.code(link, language="text")

    # Terminal Preview Switcher
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👁️ Terminal Preview")
    preview_mode = st.sidebar.selectbox(
        "View As:",
        options=["Main Dashboard", "Threat Actor Terminal", "IT Defense Terminal", "Executive Terminal", "Media Terminal"]
    )

    if st.sidebar.button("🔄 Force Refresh All", use_container_width=True):
        st.rerun()

    if preview_mode == "Main Dashboard":
        render_main_dashboard(game)
    elif preview_mode == "Threat Actor Terminal":
        render_hacker_terminal(game, True, voter_id)
    elif preview_mode == "IT Defense Terminal":
        render_it_terminal(game, True, voter_id)
    elif preview_mode == "Executive Terminal":
        render_exec_terminal(game, True, voter_id)
    elif preview_mode == "Media Terminal":
        render_media_terminal(game, True, voter_id)

if __name__ == "__main__":
    main()
