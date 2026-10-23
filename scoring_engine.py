"""
scoring_engine.py
Unified Company Health Scoring & Outcome Distribution Engine
for CloudStore Command: Cyber Attack Simulation
"""

import random
from typing import Dict, Any, Tuple

def calculate_round_impact(
    attack: Dict[str, Any],
    it_choice: Dict[str, Any],
    exec_action: str,
    media_headline: Dict[str, Any],
    multiplier: float = 1.0
) -> Dict[str, Any]:
    """
    Calculates the net impact of a round on unified Company Health (starting at 100).
    
    Parameters:
        attack: Dictionary with 'damage' (negative integer, e.g. -20, -25, -30)
        it_choice: Dictionary with 'mitigation_pct' (0.0 to 1.0) and 'disruption_penalty' (negative int)
        exec_action: "approve", "downgrade", or "overrule"
        media_headline: Dictionary with 'health_delta' (-12 to +8)
        multiplier: Threat severity multiplier (1.0, 1.2, 1.5, 2.0)
    
    Returns:
        Dictionary containing net_delta and the itemized audit breakdown.
    """
    raw_hacker_dmg = attack.get("damage", -25) * multiplier
    it_mit = it_choice.get("mitigation_pct", 0.60)
    it_disrupt = it_choice.get("disruption_penalty", -2)

    # Executive Governance Impact on IT Containment
    exec_action_norm = str(exec_action).lower().strip()
    if exec_action_norm == "approve":
        effective_mitigation = abs(raw_hacker_dmg) * it_mit
        effective_disruption = it_disrupt
        exec_summary = "Approved IT Plan (Full Containment, Full Disruption)"
    elif exec_action_norm == "downgrade":
        effective_mitigation = abs(raw_hacker_dmg) * (it_mit * 0.50)
        effective_disruption = int(it_disrupt * 0.50)
        exec_summary = "Downgraded IT Plan (Compromise: 50% Containment, 50% Disruption)"
    else:  # overrule
        effective_mitigation = abs(raw_hacker_dmg) * 0.05
        effective_disruption = 0
        exec_summary = "Overruled IT Plan (Business-As-Usual, Minimal Breach Containment)"

    media_delta = media_headline.get("health_delta", 0)

    # Real-world execution friction roll (stochastic variance ±3)
    friction = random.randint(-3, 3)

    net_delta = round(raw_hacker_dmg + effective_mitigation + effective_disruption + media_delta + friction, 1)

    return {
        "net_delta": net_delta,
        "breakdown": {
            "hacker_damage": round(raw_hacker_dmg, 1),
            "it_mitigated": round(effective_mitigation, 1),
            "disruption_penalty": effective_disruption,
            "exec_action": exec_summary,
            "media_delta": media_delta,
            "friction": friction
        }
    }

def get_outcome_thresholds(total_rounds: int) -> Tuple[int, int]:
    """
    Returns (bankrupt_cutoff, win_cutoff) calibrated for target distribution:
    Scores < bankrupt_cutoff -> Bankrupt (~30%)
    Scores >= win_cutoff -> Win (~10%)
    Scores in between -> Survive (~60%)
    Calibrated for 2 rounds of incident response followed by the Adversary Final Gambit.
    """
    if total_rounds == 2:
        return 39, 76
    else:
        return 30, 62

def evaluate_final_outcome(final_health: float, total_rounds: int) -> Tuple[str, str, str]:
    """
    Evaluates final score against the calibrated distribution curve:
    Target: 10% Win | 60% Survive | 30% Bankrupt
    """
    bankrupt_cutoff, win_cutoff = get_outcome_thresholds(total_rounds)

    if final_health >= win_cutoff:
        return (
            "Win",
            "🏆 Exceptional Cyber Resilience & Leadership",
            "The organization successfully thwarted the attack lifecycle, maintained operational integrity, "
            "and preserved shareholder and customer trust through disciplined crisis governance."
        )
    elif final_health >= bankrupt_cutoff:
        return (
            "Survive",
            "🛡️ Damaged but Solvent & Operational",
            "The organization suffered painful downtime, remediation costs, and negative press, "
            "but effective containment and executive crisis leadership averted enterprise liquidation."
        )
    else:
        return (
            "Bankrupt",
            "💥 Catastrophic Failure & Insolvency",
            "Uncontained lateral spread, compounding service disruptions, and devastating public disclosure "
            "depleted capital reserves and forced the enterprise into Chapter 11 bankruptcy."
        )
