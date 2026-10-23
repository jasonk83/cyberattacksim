"""
state_manager.py
Global in-memory synchronized game state across multi-device sessions
for CloudStore Command: Cyber Attack Simulation
"""

import time
import copy
from typing import Dict, Any, Optional, List, Tuple
from game_data import PHASE_DURATIONS, ATTACKS, IT_CHOICES, EXEC_GOVERNANCE_OPTIONS, DYNAMIC_HEADLINES
from scoring_engine import calculate_round_impact, evaluate_final_outcome, get_outcome_thresholds

class GameState:
    def __init__(self):
        self.reset()

    def reset(self, base_health: float = 100.0, max_rounds: int = 3):
        self.company_health = float(base_health)
        self.max_rounds = int(max_rounds)
        self.current_round = 1
        self.multiplier = 1.0
        self.phase = "lobby"  # 'lobby', 'hacker', 'it', 'exec', 'media', 'recap', 'game_over'

        # Timer state
        self.phase_start_time = time.time()
        self.phase_duration = PHASE_DURATIONS.get("hacker", 300)
        self.timer_paused = False
        self.pause_time_remaining = self.phase_duration

        # Polling state per team (voter_id -> option_id)
        self.polls: Dict[str, Dict[str, Any]] = {
            "hackers": {"open": False, "options": [], "votes": {}},
            "it": {"open": False, "options": [], "votes": {}},
            "exec": {"open": False, "options": [], "votes": {}},
            "media": {"open": False, "options": [], "votes": {}}
        }

        # Decisions in active round
        self.selected_attack_key: Optional[str] = None
        self.selected_attack_data: Optional[Dict[str, Any]] = None
        self.it_choice_id: Optional[str] = None
        self.it_choice_data: Optional[Dict[str, Any]] = None
        self.exec_action: Optional[str] = None
        self.media_headline_idx: Optional[int] = None
        self.media_headline_data: Optional[Dict[str, Any]] = None

        # Real-time team status badges
        self.team_status: Dict[str, str] = {
            "hackers": "Standby in Lobby",
            "it": "Standby in Lobby",
            "exec": "Standby in Lobby",
            "media": "Standby in Lobby"
        }

        self.history: List[Dict[str, Any]] = []
        self.snapshots: List[Dict[str, Any]] = []

    def start_phase(self, new_phase: str):
        self.phase = new_phase
        duration = PHASE_DURATIONS.get(new_phase, 300)
        self.phase_duration = duration
        self.phase_start_time = time.time()
        self.timer_paused = False
        self.pause_time_remaining = duration

        # Reset poll state for the active role
        if new_phase in self.polls:
            self.polls[new_phase] = {"open": False, "options": [], "votes": {}}

        # Update team statuses
        if new_phase == "hacker":
            self.team_status["hackers"] = "🔴 Selecting Attack Vector"
            self.team_status["it"] = "🟢 Systems Nominal (Monitoring)"
            self.team_status["exec"] = "🟢 Normal Governance"
            self.team_status["media"] = "📡 Routine News Cycle"
        elif new_phase == "it":
            self.team_status["hackers"] = "🔒 Payload Deployed (Observing)"
            self.team_status["it"] = "🟡 Deliberating Containment"
            self.team_status["exec"] = "⏳ Awaiting IT Technical Proposal"
            self.team_status["media"] = "📡 Tracking Breaking Rumors"
        elif new_phase == "exec":
            self.team_status["hackers"] = "🔒 Payload Active"
            self.team_status["it"] = "✅ Plan Submitted to Board"
            self.team_status["exec"] = "🟠 Reviewing IT Proposal & Voting"
            self.team_status["media"] = "📡 Awaiting Executive Statement"
        elif new_phase == "media":
            self.team_status["hackers"] = "🔒 Payload Active"
            self.team_status["it"] = "✅ Plan Authorized"
            self.team_status["exec"] = "✅ Directive Issued"
            self.team_status["media"] = "🚨 Selecting Breaking Headline"
        elif new_phase == "recap":
            for k in self.team_status:
                self.team_status[k] = "📊 Round Recap Active"
        elif new_phase == "game_over":
            for k in self.team_status:
                self.team_status[k] = "🏁 Simulation Concluded"

    def get_remaining_seconds(self) -> int:
        if self.timer_paused:
            return max(0, int(self.pause_time_remaining))
        elapsed = time.time() - self.phase_start_time
        remaining = self.phase_duration - elapsed
        return max(0, int(remaining))

    def pause_timer(self):
        if not self.timer_paused:
            self.pause_time_remaining = self.get_remaining_seconds()
            self.timer_paused = True

    def resume_timer(self):
        if self.timer_paused:
            self.phase_start_time = time.time() - (self.phase_duration - self.pause_time_remaining)
            self.timer_paused = False

    def reset_timer(self, custom_seconds: Optional[int] = None):
        duration = custom_seconds if custom_seconds else PHASE_DURATIONS.get(self.phase, 300)
        self.phase_duration = duration
        self.phase_start_time = time.time()
        self.timer_paused = False
        self.pause_time_remaining = duration

    # ---------------------------------------------------------
    # STRAW POLLING STATE ENGINE
    # ---------------------------------------------------------
    def open_poll(self, role: str, options: List[Dict[str, Any]]):
        if role in self.polls:
            self.polls[role] = {
                "open": True,
                "options": options,
                "votes": {}
            }
            self.team_status[role] = f"🗳️ Live Straw Poll Open"

    def cast_vote(self, role: str, voter_id: str, option_id: str):
        if role in self.polls and self.polls[role]["open"]:
            self.polls[role]["votes"][str(voter_id)] = str(option_id)

    def close_poll(self, role: str):
        if role in self.polls:
            self.polls[role]["open"] = False
            vote_count = len(self.polls[role]["votes"])
            self.team_status[role] = f"🔒 Poll Closed ({vote_count} votes cast)"

    def get_poll_stats(self, role: str) -> Dict[str, Any]:
        if role not in self.polls:
            return {"total_votes": 0, "tallies": {}}
        poll = self.polls[role]
        votes = poll.get("votes", {})
        total = len(votes)
        tallies = {}
        for opt in poll.get("options", []):
            opt_id = str(opt.get("id"))
            cnt = sum(1 for v in votes.values() if str(v) == opt_id)
            pct = (cnt / total * 100.0) if total > 0 else 0.0
            tallies[opt_id] = {"count": cnt, "percent": pct, "label": opt.get("label", f"Option {opt_id}")}
        return {"total_votes": total, "tallies": tallies}

    # ---------------------------------------------------------
    # DECISION SUBMISSION FLOW
    # ---------------------------------------------------------
    def submit_hacker_attack(self, choice_key: str):
        self.create_snapshot()
        self.close_poll("hackers")
        self.selected_attack_key = choice_key
        round_attacks = ATTACKS.get(self.current_round, {})
        self.selected_attack_data = round_attacks.get(choice_key, {})
        self.team_status["hackers"] = f"✅ Launched {self.selected_attack_data.get('name', 'Attack')}"
        # Advance to IT Defense phase
        self.start_phase("it")

    def submit_it_choice(self, choice_id: str):
        self.create_snapshot()
        self.close_poll("it")
        self.it_choice_id = str(choice_id)
        round_it = IT_CHOICES.get(self.current_round, [])
        self.it_choice_data = next((c for c in round_it if str(c.get("id")) == str(choice_id)), {})
        self.team_status["it"] = f"✅ Submitted Plan: {self.it_choice_data.get('label', 'Plan')}"
        # Advance to Executive Governance phase
        self.start_phase("exec")

    def submit_exec_choice(self, action_id: str):
        self.create_snapshot()
        self.close_poll("exec")
        self.exec_action = str(action_id).lower()
        self.team_status["exec"] = f"✅ Directive: {action_id.upper()}"
        # Advance to Media Scrum phase
        self.start_phase("media")

    def submit_media_choice(self, headline_idx: int):
        self.create_snapshot()
        self.close_poll("media")
        self.media_headline_idx = headline_idx
        headlines = DYNAMIC_HEADLINES.get(self.current_round, [])
        if 0 <= headline_idx < len(headlines):
            self.media_headline_data = headlines[headline_idx]
        else:
            self.media_headline_data = {"headline": "Breaking Report", "health_delta": 0}
        self.team_status["media"] = f"✅ Published Headline"
        # Trigger round evaluation and move to recap
        self.evaluate_round()

    def evaluate_round(self):
        attack = self.selected_attack_data or {"damage": -25}
        it_choice = self.it_choice_data or {"mitigation_pct": 0.5, "disruption_penalty": -2}
        exec_action = self.exec_action or "downgrade"
        media_choice = self.media_headline_data or {"health_delta": 0}

        impact = calculate_round_impact(
            attack=attack,
            it_choice=it_choice,
            exec_action=exec_action,
            media_headline=media_choice,
            multiplier=self.multiplier
        )

        net_delta = impact["net_delta"]
        prev_health = self.company_health
        self.company_health = max(0.0, min(100.0, round(self.company_health + net_delta, 1)))

        record = {
            "round": self.current_round,
            "attack_name": attack.get("name", "Unknown Threat"),
            "attack_key": self.selected_attack_key,
            "attack_damage": impact["breakdown"]["hacker_damage"],
            "it_plan": it_choice.get("label", "Unknown Action"),
            "it_mitigated": impact["breakdown"]["it_mitigated"],
            "disruption_penalty": impact["breakdown"]["disruption_penalty"],
            "exec_decision": impact["breakdown"]["exec_action"],
            "headline": media_choice.get("headline", "News Release"),
            "media_delta": impact["breakdown"]["media_delta"],
            "friction": impact["breakdown"]["friction"],
            "net_delta": net_delta,
            "health_before": prev_health,
            "health_after": self.company_health,
            "multiplier": self.multiplier
        }
        self.history.append(record)
        self.start_phase("recap")

    def advance_to_next_round(self):
        if self.current_round >= self.max_rounds:
            self.start_phase("game_over")
        else:
            self.current_round += 1
            self.selected_attack_key = None
            self.selected_attack_data = None
            self.it_choice_id = None
            self.it_choice_data = None
            self.exec_action = None
            self.media_headline_idx = None
            self.media_headline_data = None
            self.start_phase("hacker")

    def create_snapshot(self):
        snap = {
            "company_health": self.company_health,
            "current_round": self.current_round,
            "max_rounds": self.max_rounds,
            "phase": self.phase,
            "multiplier": self.multiplier,
            "selected_attack_key": self.selected_attack_key,
            "selected_attack_data": copy.deepcopy(self.selected_attack_data),
            "it_choice_id": self.it_choice_id,
            "it_choice_data": copy.deepcopy(self.it_choice_data),
            "exec_action": self.exec_action,
            "media_headline_idx": self.media_headline_idx,
            "media_headline_data": copy.deepcopy(self.media_headline_data),
            "history": copy.deepcopy(self.history),
            "team_status": copy.deepcopy(self.team_status)
        }
        self.snapshots.append(snap)

    def undo_last_round(self) -> bool:
        if not self.snapshots:
            return False
        snap = self.snapshots.pop()
        self.company_health = snap["company_health"]
        self.current_round = snap["current_round"]
        self.max_rounds = snap["max_rounds"]
        self.phase = snap["phase"]
        self.multiplier = snap["multiplier"]
        self.selected_attack_key = snap["selected_attack_key"]
        self.selected_attack_data = copy.deepcopy(snap["selected_attack_data"])
        self.it_choice_id = snap["it_choice_id"]
        self.it_choice_data = copy.deepcopy(snap["it_choice_data"])
        self.exec_action = snap["exec_action"]
        self.media_headline_idx = snap["media_headline_idx"]
        self.media_headline_data = copy.deepcopy(snap["media_headline_data"])
        self.history = copy.deepcopy(snap["history"])
        self.team_status = copy.deepcopy(snap["team_status"])
        self.start_phase(self.phase)
        return True
