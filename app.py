"""
CloudStore Command: Mission Control
Multiplayer Cyber Incident Response Simulation
Streamlit Application
"""

import streamlit as st
import time
import copy
from typing import Dict, Any, Optional

# Import modular game data and scoring engine
try:
    from game_data import TEAM_CODES, ATTACKS, IT_CHOICES, EXEC_CHOICES, DYNAMIC_HEADLINES
except ImportError:
    import game_data as gd
    TEAM_CODES = gd.TEAM_CODES
    ATTACKS = gd.ATTACKS
    IT_CHOICES = gd.IT_CHOICES
    EXEC_CHOICES = gd.EXEC_CHOICES
    DYNAMIC_HEADLINES = gd.DYNAMIC_HEADLINES

try:
    from scoring_engine import calculate_round_impact
except ImportError:
    import scoring_engine as se
    calculate_round_impact = se.calculate_round_impact

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
        
        # Current round submissions
        self.selected_attack_key: Optional[str] = None
        self.selected_attack_data: Optional[Dict[str, Any]] = None
        self.it_choice_id: Optional[str] = None
        self.exec_choice_id: Optional[str] = None
        self.media_headline_idx: Optional[int] = None
        
        # Cumulative 4-Quadrant Scorecard
        self.team_scorecard = {
            "IT": 0,
            "Exec": 0,
            "Media": 0,
            "Hacker": 0
        }
        
        # Round history & Undo snapshots
        self.history = []
        self.snapshots = []

    def create_snapshot(self):
        """Saves deep copy of current state for Instructor Undo."""
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
        """Rolls back state to the most recent snapshot."""
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
        self.it_choice_id = choice_id
        self._check_defense_complete()

    def submit_exec_choice(self, choice_id: str):
        self.exec_choice_id = choice_id
        self._check_defense_complete()

    def _check_defense_complete(self):
        if self.it_choice_id and self.exec_choice_id:
            self.phase = "media"

    def submit_media_choice(self, headline_idx: int):
        self.media_headline_idx = headline_idx
        self.evaluate_round()

    def evaluate_round(self):
        """Evaluates round impacts using the modular scoring engine."""
        attack = self.selected_attack_data or {}
        
        # Lookup IT choice
        round_it_options = IT_CHOICES.get(self.current_round, {}).get(self.selected_attack_key, [])
        it_choice = next((c for c in round_it_options if str(c.get("id")) == str(self.it_choice_id)), {})
        
        # Lookup Exec choice
        round_exec_options = EXEC_CHOICES.get(self.current_round, [])
        exec_choice = next((c for c in round_exec_options if str(c.get("id")) == str(self.exec_choice_id)), {})
        
        # Lookup Media choice
        media_choice = None
        if self.media_headline_idx is not None and 0 <= self.media_headline_idx < len(DYNAMIC_HEADLINES):
            media_choice = DYNAMIC_HEADLINES[self.media_headline_idx]

        # Call modular scoring engine
        impact_result = calculate_round_impact(
            attack=attack,
            it_choice=it_choice,
            exec_choice=exec_choice,
            media_headline=media_choice,
            multiplier=self.multiplier
        )

        deltas = impact_result.get("deltas", {})
        team_round_scores = impact_result.get("team_scorecard", {})

        # Apply deltas to organizational scores
        for metric, delta in deltas.items():
            if metric in self.scores:
                self.scores[metric] = max(0.0, min(self.base_score * 1.5, round(self.scores[metric] + delta, 1)))

        # Update cumulative 4-quadrant team scorecard
        for team, score in team_round_scores.items():
            self.team_scorecard[team] = self.team_scorecard.get(team, 0) + score

        # Record round history log
        record = {
            "round": self.current_round,
            "attack": attack.get("name", "Unknown Vector"),
            "attack_key": self.selected_attack_key,
            "it_action": it_choice.get("label", "None"),
            "exec_action": exec_choice.get("label", "None"),
            "headline": media_choice.get("headline", "No press release") if media_choice else "None",
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
            <span style="font-size: 26px; font-weight: 800; color: #f8fafc;">{value:.1f}</span>
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
# ROLE TERMINAL VIEWS
# ---------------------------------------------------------
def render_instructor_view(game: GameState):
    st.title("🛡️ CloudStore Command: Mission Control")
    st.caption("Central Operations Room & Instructor Control Console")

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
        "lobby": "🎮 Simulation Lobby — Waiting for Instructor to Launch",
        "hacker": f"🔴 Round {game.current_round}: Awaiting Threat Actor Attack Vector...",
        "defense": f"🟡 Round {game.current_round}: Incident Active! Defense Teams Deliberating...",
        "media": f"🟠 Round {game.current_round}: Press Scrum in Progress — Awaiting News Headline...",
        "recap": f"🟢 Round {game.current_round}: Assessment Complete — Reviewing Metrics",
        "game_over": "🏁 Simulation Concluded — Final Assessment"
    }
    st.info(phase_descriptions.get(game.phase, f"Phase: {game.phase}"))

    # Active Incident Banner
    if game.selected_attack_data:
        att = game.selected_attack_data
        st.markdown(f"""
        <div style="background-color: #450a0a; border: 2px solid #ef4444; border-radius: 12px; padding: 16px; margin: 12px 0;">
            <div style="font-size: 11px; font-weight: 800; color: #fca5a5; text-transform: uppercase; letter-spacing: 0.1em;">ACTIVE INCIDENT ALERT</div>
            <div style="font-size: 20px; font-weight: 800; color: #ffffff; margin-top: 4px;">{att.get('icon', '🚨')} {att.get('name', 'Cyber Incident')}</div>
            <div style="font-size: 14px; color: #fecaca; margin-top: 6px;">{att.get('description', '')}</div>
        </div>
        """, unsafe_allow_html=True)

    # 4-Quadrant Scorecard
    render_scorecard_quadrant(game.team_scorecard)

    st.markdown("---")

    # Instructor Action Controls
    st.subheader("⚙️ Mission Control Operator Controls")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        if game.phase == "lobby":
            if st.button("🚀 Start Round 1", type="primary", use_container_width=True):
                game.phase = "hacker"
                st.rerun()
        elif game.phase == "recap":
            next_label = "🏁 Conclude Game" if game.current_round >= game.max_rounds else f"Start Round {game.current_round + 1}"
            if st.button(f"➡️ {next_label}", type="primary", use_container_width=True):
                game.advance_to_next_round()
                st.rerun()

    with c2:
        game.multiplier = st.selectbox(
            "Difficulty Multiplier",
            options=[1.0, 1.2, 1.5, 2.0],
            index=[1.0, 1.2, 1.5, 2.0].index(game.multiplier) if game.multiplier in [1.0, 1.2, 1.5, 2.0] else 0,
            format_func=lambda x: f"{x}x Threat Intensity"
        )

    with c3:
        if st.button("↩️ Undo Last Round", use_container_width=True, disabled=len(game.snapshots) == 0):
            if game.undo_last_round():
                st.success("Rolled back to previous state snapshot.")
                st.rerun()

    with c4:
        if st.button("🔄 Reset Entire Simulation", type="secondary", use_container_width=True):
            game.reset()
            st.rerun()

    # Timeline Log
    if game.history:
        st.markdown("### 📜 Mission Incident Timeline")
        for entry in reversed(game.history):
            with st.expander(f"Round {entry['round']}: {entry['attack']} ({entry['multiplier']}x Multiplier)", expanded=False):
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
    st.error(f"🚨 **ACTIVE BREACH:** {att.get('icon', '')} {att.get('name')} — {att.get('description')}")

    if game.it_choice_id:
        st.success(f"✅ Technical mitigation submitted! Standing by for Executive and Media directives.")
        return

    st.subheader("Select Technical Containment Action")
    st.caption("Review simplified containment options below:")

    it_options = IT_CHOICES.get(game.current_round, {}).get(game.selected_attack_key, [])
    if not it_options:
        st.warning("No IT options defined for this scenario.")
        return

    for opt in it_options:
        with st.container():
            st.markdown(f"""
            <div style="background-color: #0f172a; padding: 12px; border-radius: 10px; border-left: 4px solid #38bdf8; margin-bottom: 8px;">
                <div style="font-weight: 700; color: #f8fafc; font-size: 15px;">Option {opt['id']}: {opt['label']}</div>
                <div style="color: #94a3b8; font-size: 13px; margin-top: 4px;">{opt['desc']}</div>
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
    st.error(f"🚨 **CRITICAL INCIDENT:** {att.get('icon', '')} {att.get('name')} — {att.get('description')}")

    if game.exec_choice_id:
        st.success("✅ Executive directive confirmed! Waiting for IT and Media finalization.")
        return

    st.subheader("Select Strategic Directive")
    st.caption("Review simplified policy options below:")

    exec_options = EXEC_CHOICES.get(game.current_round, [])
    if not exec_options:
        st.warning("No Executive options defined for this round.")
        return

    for opt in exec_options:
        with st.container():
            st.markdown(f"""
            <div style="background-color: #0f172a; padding: 12px; border-radius: 10px; border-left: 4px solid #818cf8; margin-bottom: 8px;">
                <div style="font-weight: 700; color: #f8fafc; font-size: 15px;">Directive {opt['id']}: {opt['label']}</div>
                <div style="color: #94a3b8; font-size: 13px; margin-top: 4px;">{opt['desc']}</div>
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

    for idx, item in enumerate(DYNAMIC_HEADLINES):
        delta = item["trust_delta"]
        delta_str = f"+{delta}" if delta > 0 else f"{delta}"
        badge_color = "#10b981" if delta > 0 else "#64748b" if delta == 0 else "#ef4444"

        st.markdown(f"""
        <div style="background-color: #0f172a; padding: 12px; border-radius: 10px; border: 1px solid #1e293b; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 15px; font-weight: 700; color: #f8fafc;">"{item['headline']}"</span>
            <span style="background-color: {badge_color}; color: white; padding: 2px 8px; border-radius: 999px; font-size: 12px; font-weight: 800;">Trust {delta_str}</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Publish Headline #{idx + 1}", key=f"btn_media_{idx}", use_container_width=True):
            game.submit_media_choice(idx)
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

    # Sidebar: Terminal Authentication & Routing
    st.sidebar.title("🔐 Terminal Access")
    role_options = {
        "Mission Control (Instructor)": "main",
        "Threat Actor (Hacker)": "hackers",
        "IT Defense Command": "it",
        "Executive Board": "exec",
        "Media & PR Scrum": "media"
    }

    selected_role_label = st.sidebar.selectbox("Select Role", options=list(role_options.keys()))
    role_key = role_options[selected_role_label]
    correct_passcode = TEAM_CODES.get(role_key, "admin123")

    passcode = st.sidebar.text_input("Enter Passcode", type="password", key=f"pwd_{role_key}")

    # Check Passcode (allows quick bypass if passcode matches or left blank in dev mode)
    authenticated = (passcode == correct_passcode) or (passcode == "admin")

    st.sidebar.markdown("---")
    st.sidebar.caption(f"Current Simulation Round: **{game.current_round} / {game.max_rounds}**")
    st.sidebar.caption(f"Active Phase: **{game.phase.upper()}**")

    if st.sidebar.button("🔄 Force Refresh View", use_container_width=True):
        st.rerun()

    if not authenticated and passcode:
        st.error("❌ Invalid Access Passcode for this Terminal.")
        st.stop()
    elif not authenticated and not passcode:
        st.sidebar.info(f"💡 Enter team passcode for {selected_role_label} to access controls.")
        # Allow view-only instructor dashboard if no password entered yet
        if role_key == "main":
            render_instructor_view(game)
        else:
            st.warning("Please enter your team passcode in the sidebar to activate this terminal.")
        st.stop()

    # Route to authenticated view
    if role_key == "main":
        render_instructor_view(game)
    elif role_key == "hackers":
        render_hacker_terminal(game)
    elif role_key == "it":
        render_it_terminal(game)
    elif role_key == "exec":
        render_exec_terminal(game)
    elif role_key == "media":
        render_media_terminal(game)

if __name__ == "__main__":
    main()
