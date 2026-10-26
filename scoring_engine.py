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
        it_choice: Dictionary with 'mitigation_range' (tuple of min, max) or 'mitigation_pct', plus 'disruption_penalty'
        exec_action: "approve", "downgrade", or "overrule"
        media_headline: Dictionary with 'health_delta_range' (tuple of min, max) or 'health_delta'
        multiplier: Threat severity multiplier (1.0, 1.2, 1.5, 2.0)
    
    Returns:
        Dictionary containing net_delta, surprise commentary, and itemized breakdown.
    """
    raw_hacker_dmg = attack.get("damage", -25) * multiplier
    
    # Stochastic IT mitigation within qualitative range
    mit_range = it_choice.get("mitigation_range")
    if mit_range and isinstance(mit_range, (tuple, list)):
        it_mit = random.uniform(float(mit_range[0]), float(mit_range[1]))
    else:
        it_mit = float(it_choice.get("mitigation_pct", 0.60))
        
    it_disrupt = it_choice.get("disruption_penalty", -2)

    # Executive Governance Impact on IT Containment
    exec_action_norm = str(exec_action).lower().strip()
    if exec_action_norm == "approve":
        effective_mitigation = abs(raw_hacker_dmg) * it_mit
        effective_disruption = it_disrupt
        exec_summary = "Approved IT Directive (Full Containment Authorized)"
    elif exec_action_norm == "downgrade":
        effective_mitigation = abs(raw_hacker_dmg) * (it_mit * 0.50)
        effective_disruption = int(it_disrupt * 0.50)
        exec_summary = "Downgraded IT Directive (Compromise: 50% Containment, 50% Disruption)"
    else:  # overrule
        effective_mitigation = abs(raw_hacker_dmg) * 0.05
        effective_disruption = 0
        exec_summary = "Overruled IT Directive (Business Continuity Prioritized, 5% Containment)"

    # Randomized Media Resonance Roll
    delta_range = media_headline.get("health_delta_range")
    if delta_range and isinstance(delta_range, (tuple, list)):
        media_delta = random.randint(int(delta_range[0]), int(delta_range[1]))
    else:
        media_delta = int(media_headline.get("health_delta", 0))

    # Real-world execution friction roll (stochastic variance ±3)
    friction = random.randint(-3, 3)

    net_delta = round(raw_hacker_dmg + effective_mitigation + effective_disruption + media_delta + friction, 1)

    # Generate Surprise & Reality Check narrative callouts
    it_pct_display = int(round(it_mit * 100))
    if it_mit >= 0.85:
        it_surprise = f"Containment Success ({it_pct_display}% effective): Decisive isolation neutralized nearly all attacker lateral spread."
    elif it_mit >= 0.60:
        it_surprise = f"Substantial Defense ({it_pct_display}% effective): Containment blocked core threat, but minor persistence survived."
    elif it_mit >= 0.40:
        it_surprise = f"Contingent Mitigation ({it_pct_display}% effective): Partial defenses slowed the adversary, though secondary payloads executed."
    else:
        it_surprise = f"Severe Defense Gap ({it_pct_display}% effective): Minimal barrier; threat actors operated almost unimpeded."

    if media_delta <= -10:
        media_surprise = f"Viral Panic ({media_delta:+d} HP): Headline sparked national outrage, compounding consumer anxiety and market volatility."
    elif media_delta <= -5:
        media_surprise = f"Critical Scrutiny ({media_delta:+d} HP): Investigative reports scrutinized cyber governance, damaging near-term reputation."
    elif media_delta <= 0:
        media_surprise = f"Low Public Resonance ({media_delta:+d} HP): Story was largely overshadowed by daily news, minimizing reputational harm."
    elif media_delta <= 5:
        media_surprise = f"Measured Coverage ({media_delta:+d} HP): Balanced reporting noted prompt containment, reassuring cautious customers."
    else:
        media_surprise = f"PR Triumph ({media_delta:+d} HP): Front-page praise for corporate transparency rallied investor and public confidence."

    return {
        "net_delta": net_delta,
        "breakdown": {
            "hacker_damage": round(raw_hacker_dmg, 1),
            "it_mitigated": round(effective_mitigation, 1),
            "it_mit_pct": it_pct_display,
            "disruption_penalty": effective_disruption,
            "exec_action": exec_summary,
            "media_delta": media_delta,
            "friction": friction,
            "it_surprise": it_surprise,
            "media_surprise": media_surprise
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
        return 39, 75
    else:
        return 30, 60

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
