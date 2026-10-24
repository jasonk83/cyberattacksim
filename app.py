"""
CloudStore Command: Mission Control
Multiplayer Cyber Incident Response Tabletop Simulation
Streamlit Application
"""

import sys
import os
from pathlib import Path
import importlib
import uuid
from typing import Dict, Any, Optional
import streamlit as st

# Ensure repository root directory is prioritized in sys.path (critical for Streamlit Cloud)
ROOT_DIR = str(Path(__file__).resolve().parent)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Invalidate stale in-memory module caches on Streamlit Cloud hot-reloads
importlib.invalidate_caches()
if "game_data" in sys.modules and not hasattr(sys.modules["game_data"], "PHASE_DURATIONS"):
    del sys.modules["game_data"]

from state_manager import GameState
from game_data import TEAM_CODES
from scoring_engine import evaluate_final_outcome, get_outcome_thresholds
from ui_components import (
    render_threatening_clock,
    render_health_gauge,
    render_final_hacker_action_card,
    render_round_recap_card,
    render_acronym_glossary
)
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
# DEDICATED CLASS PROJECTOR VIEW (?team=projector)
# ---------------------------------------------------------
def render_projector_view(game: GameState):
    """
    Renders an uncluttered, read-only big-screen presentation dashboard for screensharing.
    Completely suppresses the sidebar and all interactive mission control buttons,
    displaying real-time synchronized telemetry, health gauges, and incident cards.
    """
    st.markdown(
        """
        <style>
        /* Suppress sidebar, collapsed chevron, and header toolbar for clean projector presentation */
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {
            display: none !important;
        }
        section.main > div {
            max-width: 100% !important;
            padding-top: 1.5rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    render_main_dashboard(game, is_admin=False, is_projector=True)

# ---------------------------------------------------------
# GM PROJECTOR & MISSION CONTROL SCOREBOARD
# ---------------------------------------------------------
@st.fragment(run_every=2)
def render_main_dashboard(game: GameState, is_admin: Optional[bool] = None, is_projector: bool = False):
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🛡️ CloudStore Command: Mission Control")
        st.caption("Live Operational Cyber Incident Response Tabletop Simulation")
    with col2:
        st.write("")
        if is_projector:
            st.markdown(
                """
                <div style="text-align: right; margin-top: 10px;">
                    <span style="display: inline-flex; align-items: center; gap: 8px; background-color: #0f172a; border: 1px solid #10b981; border-radius: 9999px; padding: 6px 16px; font-size: 13px; font-weight: 700; color: #34d399;">
                        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background-color: #10b981;"></span>
                        Live Telemetry Auto-Sync
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            if st.button("🔄 Refresh Scoreboard", key="top_refresh_main", use_container_width=True):
                st.rerun()

    # ---------------------------------------------------------
    # GM QUICK OPERATIONAL COMMAND BAR (Hidden on Projector)
    # ---------------------------------------------------------
    if not is_projector:
        # Determine whether GM admin privileges are active
        if is_admin is None:
            is_admin = st.session_state.get("admin_authenticated", False) or st.session_state.get("instructor_authenticated", False)

        st.markdown("### 🎛️ Game Master Mission Controls")
        col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2, 1, 1])

        with col_ctrl1:
            if game.phase == "lobby":
                if st.button("🚀 Start Round 1 (Launch Infiltration)", key="main_btn_start_r1", type="primary", use_container_width=True):
                    game.start_phase("hacker")
                    st.rerun()
            elif game.phase == "recap":
                if game.current_round < game.max_rounds:
                    if st.button(f"➡️ Advance to Round {game.current_round + 1}", key="main_btn_adv_r", type="primary", use_container_width=True):
                        game.advance_to_next_round()
                        st.rerun()
                else:
                    if st.button("💀 Advance to Adversary Final Action", key="main_btn_adv_gambit", type="primary", use_container_width=True):
                        game.advance_to_next_round()
                        st.rerun()
            elif game.phase == "final_hacker_action":
                if st.button("⚡ Fast-Conclude Simulation (Retreat)", key="main_btn_bypass_final", use_container_width=True):
                    game.submit_final_hacker_action("retreat")
                    st.rerun()
            elif game.phase == "game_over":
                if st.button("🔄 Reset Simulation for New Session", key="main_btn_reset_game", type="primary", use_container_width=True):
                    game.reset(max_rounds=game.max_rounds)
                    st.rerun()
            else:
                next_phase_map = {"hacker": "it", "it": "exec", "exec": "media", "media": "recap"}
                if st.button(f"⏭️ Force Advance ({game.phase.upper()})", key="main_btn_force_adv", use_container_width=True):
                    if game.phase == "media":
                        game.evaluate_round()
                    else:
                        game.start_phase(next_phase_map.get(game.phase, "recap"))
                    st.rerun()

        with col_ctrl2:
            if game.timer_paused:
                if st.button("▶️ Resume Timer", key="main_btn_resume_timer", use_container_width=True):
                    game.resume_timer()
                    st.rerun()
            else:
                if st.button("⏸️ Pause Timer", key="main_btn_pause_timer", use_container_width=True):
                    game.pause_timer()
                    st.rerun()

        with col_ctrl3:
            if st.button("⏱️ Reset Phase Timer", key="main_btn_reset_timer", use_container_width=True):
                game.reset_timer()
                st.rerun()

        # Manual Company HP Adjustments (Authorized GM / Admin Only)
        if is_admin:
            st.markdown(
                "<div style='font-size: 13px; font-weight: 700; color: #94a3b8; margin: 10px 0 4px 0; letter-spacing: 0.05em;'>"
                "⚖️ MANUAL COMPANY HP ADJUSTMENT (PENALTY / BONUS)"
                "</div>",
                unsafe_allow_html=True
            )
            col_hp1, col_hp2 = st.columns(2)
            with col_hp1:
                if st.button(
                    "➕ Add +10 HP (Penalize Hackers / Media)",
                    key="main_btn_add_10_hp",
                    use_container_width=True,
                    help="Add 10 HP to Company Vitality. Use to penalize Threat Actors or Media if they fail to submit a response before the timer expires."
                ):
                    game.adjust_company_health(10.0, reason="GM Penalty to Hackers/Media (+10 HP)")
                    st.toast(f"⚖️ Applied +10 HP adjustment. Enterprise Health: {game.company_health:.1f} HP")
                    st.rerun()
            with col_hp2:
                if st.button(
                    "➖ Subtract -10 HP (Penalize IT / Exec)",
                    key="main_btn_sub_10_hp",
                    use_container_width=True,
                    help="Subtract 10 HP from Company Vitality. Use to penalize IT Defense or Executive Board if they fail to submit a response before the timer expires."
                ):
                    game.adjust_company_health(-10.0, reason="GM Penalty to IT/Exec (-10 HP)")
                    st.toast(f"⚖️ Applied -10 HP penalty. Enterprise Health: {game.company_health:.1f} HP")
                    st.rerun()

        st.markdown("---")

    # Threatening Countdown Clock
    rem_secs = game.get_remaining_seconds()
    phase_labels = {
        "lobby": "Lobby Briefing",
        "hacker": "Threat Actor Infiltration",
        "it": "IT Containment Deliberation",
        "exec": "Executive Crisis Governance",
        "media": "Press Scrum & Media Spin",
        "recap": "Round Assessment",
        "final_hacker_action": "Adversary Final Gambit",
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

        render_final_hacker_action_card(game)

    # Adversary Final Action In Progress Alert
    if game.phase == "final_hacker_action":
        st.markdown("""
        <div style="background-color: #3b0764; border: 2px solid #a855f7; border-radius: 12px; padding: 18px; margin: 12px 0;">
            <div style="font-size: 11px; font-weight: 800; color: #f3e8ff; text-transform: uppercase; letter-spacing: 0.1em;">ADVERSARY FINAL GAMBIT IN PROGRESS</div>
            <div style="font-size: 22px; font-weight: 800; color: #ffffff; margin-top: 4px;">💀 Threat Actors Deliberating: Press Attack or Retreat</div>
            <div style="font-size: 14px; color: #e9d5ff; margin-top: 6px;">The Threat Actor group is deciding whether to press their attack deeper into secondary payment systems (75% chance of inflicting 15–30 HP damage, or a 1-in-4 chance of being caught inflicting 0 damage while company recovers 3–15 HP) or execute a clean retreat into the shadows.</div>
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

    # Student Cybersecurity Vocabulary Glossary
    render_acronym_glossary()

# ---------------------------------------------------------
# SINGLE-PLAYER INSTRUCTOR TESTING MODE
# ---------------------------------------------------------
def render_instructor_mode(voter_id: str):
    """
    Dedicated single-player instructor test experience.
    Runs on an isolated GameState instance so testing does not affect live multiplayer games.
    Renders the Game Master Console above a divider and walks the instructor
    through each team's Captain terminal sequentially as choices are made.
    """
    # 1. Initialize isolated private game state for instructor
    if "instructor_game" not in st.session_state:
        st.session_state["instructor_game"] = GameState()
    solo_game = st.session_state["instructor_game"]

    if "instructor_authenticated" not in st.session_state:
        st.session_state["instructor_authenticated"] = False

    st.sidebar.title("🧑‍🏫 Instructor Testing Mode")

    # 2. Passcode gate (tryit123)
    correct_pwd = TEAM_CODES.get("instructor", "tryit123")
    if not st.session_state["instructor_authenticated"]:
        st.sidebar.caption("🔒 Instructor Passcode Required")
        pwd_sidebar = st.sidebar.text_input("Instructor Passcode", type="password", key="pwd_solo_sidebar")
        if st.sidebar.button("🔓 Unlock Instructor Sandbox", type="primary", key="btn_unlock_solo_sidebar", use_container_width=True):
            if pwd_sidebar == correct_pwd:
                st.session_state["instructor_authenticated"] = True
                st.rerun()
            else:
                st.sidebar.error("❌ Invalid Passcode. Please enter tryit123.")

        st.title("🧑‍🏫 Instructor Testing Sandbox")
        st.caption("Full Single-Player Tabletop Incident Response Simulation Environment")
        st.info("🔒 **Access Restricted:** Enter the instructor passcode (`tryit123`) to unlock single-player simulation testing.")

        col1, col2 = st.columns([3, 1])
        with col1:
            pwd_main = st.text_input("Instructor Passcode", type="password", key="pwd_solo_main", placeholder="Enter tryit123")
        with col2:
            st.write("")
            if st.button("🔓 Unlock Sandbox", type="primary", key="btn_unlock_solo_main", use_container_width=True):
                if pwd_main == correct_pwd:
                    st.session_state["instructor_authenticated"] = True
                    st.rerun()
                else:
                    st.error("❌ Invalid Passcode. Please enter tryit123.")
        return

    # 3. Authenticated Instructor Sidebar Controls
    st.sidebar.success("⭐ **CAPTAIN ACCESS UNLOCKED**")
    st.sidebar.caption("You control decisions across all 4 teams sequentially as the scenario unfolds.")
    st.sidebar.markdown(f"**Round:** {solo_game.current_round} / {solo_game.max_rounds} &nbsp;|&nbsp; **Phase:** `{solo_game.phase.upper()}`")

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🕹️ Sandbox Controls")
    if st.sidebar.button("🔄 Reset Test Simulation", key="solo_reset_sidebar", use_container_width=True):
        solo_game.reset(max_rounds=solo_game.max_rounds)
        st.rerun()

    if st.sidebar.button("🎮 Switch to GM Projector", key="solo_switch_gm", use_container_width=True):
        st.query_params["team"] = "main"
        st.rerun()

    if st.sidebar.button("🔒 Lock Sandbox", key="solo_lock_sidebar", use_container_width=True):
        st.session_state["instructor_authenticated"] = False
        st.rerun()

    # ---------------------------------------------------------
    # TOP: GAME MASTER CONSOLE & MISSION CONTROL SCOREBOARD
    # ---------------------------------------------------------
    render_main_dashboard(solo_game)

    # ---------------------------------------------------------
    # DIVIDER LINE
    # ---------------------------------------------------------
    st.markdown("---")
    st.markdown("## 🧑‍🏫 Active Captain Command Console")

    phase = solo_game.phase

    # Sequence indicator and active guidance
    step_descriptions = {
        "lobby": "Simulation in Lobby. Click **🚀 Start Round 1 (Launch Infiltration)** in the Mission Controls above to launch.",
        "hacker": "Active Step: **💀 Threat Actor Captain** — Select and deploy an attack vector below.",
        "it": "Active Step: **🛡️ IT Defense Captain** — Deliberate containment options and recommend a plan to the Board.",
        "exec": "Active Step: **💼 Executive Boardroom Captain** — Review IT's proposal and issue a binding corporate governance directive.",
        "media": "Active Step: **🎤 Media & PR Captain** — Select and publish the breaking front-page headline.",
        "recap": f"Active Step: **📊 Round {solo_game.current_round} Debrief** — Review incident metrics above and advance when ready.",
        "final_hacker_action": "Active Step: **💀 Threat Actor Captain (Final Gambit)** — Decide whether to Press Attack further or safely Retreat.",
        "game_over": "🏁 **Simulation Concluded** — Final enterprise outcome and score evaluated above."
    }
    st.info(f"👉 {step_descriptions.get(phase, 'Proceed with team decisions below.')}")

    # ---------------------------------------------------------
    # BOTTOM: ACTIVE TEAM CAPTAIN TERMINAL
    # ---------------------------------------------------------
    if phase == "lobby":
        st.write("Ready to test the scenario? Click **🚀 Start Round 1 (Launch Infiltration)** in the Game Master Mission Controls above to begin.")
    elif phase == "hacker":
        render_hacker_terminal(solo_game, is_captain=True, voter_id=voter_id)
    elif phase == "it":
        render_it_terminal(solo_game, is_captain=True, voter_id=voter_id)
    elif phase == "exec":
        render_exec_terminal(solo_game, is_captain=True, voter_id=voter_id)
    elif phase == "media":
        render_media_terminal(solo_game, is_captain=True, voter_id=voter_id)
    elif phase == "recap":
        render_round_recap_card(solo_game)
        next_label = "💀 Advance to Final Threat Actor Gambit" if solo_game.current_round >= solo_game.max_rounds else f"➡️ Start Round {solo_game.current_round + 1}"
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            if st.button(next_label, key="solo_adv_recap_btn", type="primary", use_container_width=True):
                solo_game.advance_to_next_round()
                st.rerun()
        with col_r2:
            if st.button("🔄 Reset Test Simulation", key="solo_reset_recap_btn", use_container_width=True):
                solo_game.reset(max_rounds=solo_game.max_rounds)
                st.rerun()
    elif phase == "final_hacker_action":
        render_hacker_terminal(solo_game, is_captain=True, voter_id=voter_id)
    elif phase == "game_over":
        st.success("🏁 You have completed the tabletop simulation scenario!")
        if st.button("🔄 Start New Playthrough (Reset Test Sim)", key="solo_reset_gameover_btn", type="primary", use_container_width=True):
            solo_game.reset(max_rounds=solo_game.max_rounds)
            st.rerun()

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
    is_instructor_url = url_role in ["instructor", "solo"]
    is_projector_url = url_role in ["projector", "display", "screen"]

    # ---------------------------------------------------------
    # DEDICATED CLASS PROJECTOR VIEW (?team=projector)
    # ---------------------------------------------------------
    if is_projector_url:
        render_projector_view(game)
        return

    # ---------------------------------------------------------
    # SINGLE-PLAYER INSTRUCTOR TESTING MODE (?team=instructor)
    # ---------------------------------------------------------
    if is_instructor_url:
        render_instructor_mode(voter_id)
        return

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
        next_label = "💀 Advance to Final Threat Actor Gambit" if game.current_round >= game.max_rounds else f"Start Round {game.current_round + 1}"
        if st.sidebar.button(f"➡️ {next_label}", type="primary", use_container_width=True):
            game.advance_to_next_round()
            st.rerun()
    elif game.phase == "final_hacker_action":
        st.sidebar.warning("💀 Adversary Final Gambit in Progress")
        if st.sidebar.button("⚡ Fast-Conclude Simulation (Retreat)", use_container_width=True):
            game.submit_final_hacker_action("retreat")
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

    default_base_url = "https://cyberattacksim.streamlit.app"
    base_url_input = st.sidebar.text_input("App Base URL", value=default_base_url, help="Change if your app is hosted under a different domain or on localhost.")
    base_url = base_url_input.rstrip("/")

    team_links = [
        ("💀 Threat Actors", TEAM_CODES['hackers'], "hackers"),
        ("🛡️ IT Defense", TEAM_CODES['it'], "it"),
        ("💼 Executive Board", TEAM_CODES['exec'], "exec"),
        ("🎤 Media & PR", TEAM_CODES['media'], "media"),
        ("📽️ Class Projector (Clean Display)", None, "projector"),
        ("🎮 GM Mission Control (Console)", None, "main"),
        ("🧑‍🏫 Instructor Testing Mode", TEAM_CODES['instructor'], "instructor"),
    ]

    for title, code, param in team_links:
        header = f"{title} (Passcode: {code})" if code else title
        with st.sidebar.expander(header, expanded=False):
            full_link = f"{base_url}/?team={param}"
            st.code(full_link, language="text")
            st.markdown(f"🔗 [Open Link (Relative)](/?team={param})")

    st.sidebar.caption("💡 **Tip:** In any browser tab, you can append `/?team=projector` directly to your active URL for the clean class display, or use the **👁️ Terminal Preview** dropdown below.")

    # Terminal Preview Switcher
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👁️ Terminal Preview")
    preview_mode = st.sidebar.selectbox(
        "View As:",
        options=[
            "Main Dashboard",
            "Class Projector (Clean Display)",
            "Threat Actor Terminal",
            "IT Defense Terminal",
            "Executive Terminal",
            "Media Terminal",
            "Instructor Testing Mode"
        ]
    )

    if st.sidebar.button("🔄 Force Refresh All", use_container_width=True):
        st.rerun()

    if preview_mode == "Main Dashboard":
        render_main_dashboard(game)
    elif preview_mode == "Class Projector (Clean Display)":
        render_projector_view(game)
    elif preview_mode == "Threat Actor Terminal":
        render_hacker_terminal(game, True, voter_id)
    elif preview_mode == "IT Defense Terminal":
        render_it_terminal(game, True, voter_id)
    elif preview_mode == "Executive Terminal":
        render_exec_terminal(game, True, voter_id)
    elif preview_mode == "Media Terminal":
        render_media_terminal(game, True, voter_id)
    elif preview_mode == "Instructor Testing Mode":
        render_instructor_mode(voter_id)

if __name__ == "__main__":
    main()
