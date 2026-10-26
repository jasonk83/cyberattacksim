"""
test_distribution.py
Monte Carlo simulation to verify that the scoring engine adheres to the target distribution:
- 10% Win (±2.5%)
- 60% Survive (±3.0%)
- 30% Bankrupt (±2.5%)
"""

import random
from scoring_engine import calculate_round_impact, evaluate_final_outcome, get_outcome_thresholds

def run_distribution_test(rounds=3, n_trials=20000):
    attacks = [
        {"id": "A", "damage": -20},
        {"id": "B", "damage": -25},
        {"id": "C", "damage": -30}
    ]

    it_choices = [
        {"id": "1", "mitigation_range": (0.75, 0.95), "disruption_penalty": -4},
        {"id": "2", "mitigation_range": (0.45, 0.70), "disruption_penalty": -2},
        {"id": "3", "mitigation_range": (0.15, 0.35), "disruption_penalty": 0}
    ]

    exec_actions = ["approve", "downgrade", "overrule"]

    media_headlines = [
        {"health_delta_range": (1, 12)},
        {"health_delta_range": (-3, 4)},
        {"health_delta_range": (-9, -2)},
        {"health_delta_range": (-15, -4)}
    ]

    outcomes = {"Win": 0, "Survive": 0, "Bankrupt": 0}

    for _ in range(n_trials):
        health = 100.0
        exposure_score = 0
        for _ in range(rounds):
            att = random.choice(attacks)
            it = random.choice(it_choices)
            ex = random.choice(exec_actions)
            m = random.choice(media_headlines)

            # Accumulate exposure penalty based on attack
            exposure_score += 0 if att["id"] == "A" else 1 if att["id"] == "B" else 2

            res = calculate_round_impact(att, it, ex, m)
            health = max(0.0, min(100.0, health + res["net_delta"]))

        if rounds == 2:
            # Adversary Final Gambit: Press Attack (70%) or Retreat (30%)
            if random.random() < 0.70:
                catch_chance = 0.20 if exposure_score <= 1 else 0.35 if exposure_score in [2, 3] else 0.55
                if random.random() < catch_chance:
                    dmg = 0
                    rec = random.randint(3, 15)
                else:
                    dmg = random.randint(15, 30)
                    rec = 0
                health = max(0.0, min(100.0, health - dmg + rec))

        tier, _, _ = evaluate_final_outcome(health, rounds)
        outcomes[tier] += 1

    win_pct = outcomes["Win"] / n_trials * 100
    survive_pct = outcomes["Survive"] / n_trials * 100
    bankrupt_pct = outcomes["Bankrupt"] / n_trials * 100

    b_cutoff, w_cutoff = get_outcome_thresholds(rounds)

    print(f"=== Monte Carlo Test ({rounds} Rounds, {n_trials:,} trials) ===")
    print(f"Cutoffs: Bankrupt < {b_cutoff} | Survive {b_cutoff}..{w_cutoff-1} | Win >= {w_cutoff}")
    print(f"  Win:      {win_pct:.2f}% (Target: ~10%)")
    print(f"  Survive:  {survive_pct:.2f}% (Target: ~60%)")
    print(f"  Bankrupt: {bankrupt_pct:.2f}% (Target: ~30%)")

    assert 7.5 <= win_pct <= 13.5, f"Win rate {win_pct}% out of acceptable range!"
    assert 55.0 <= survive_pct <= 65.0, f"Survive rate {survive_pct}% out of acceptable range!"
    assert 26.0 <= bankrupt_pct <= 34.0, f"Bankrupt rate {bankrupt_pct}% out of acceptable range!"
    print("✅ Distribution Test PASSED!\n")

if __name__ == "__main__":
    run_distribution_test(rounds=2)
    run_distribution_test(rounds=3)
