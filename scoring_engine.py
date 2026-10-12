# scoring_engine.py
import random

def calculate_actual_impact(projected_impact, complexity):
    """
    Calculates the actual point impact of a decision based on complexity.
    Introduces variance so the simulation cannot be perfectly min-maxed.
    """
    roll = random.random()
    
    # Baseline probabilities: 50% As Intended, 25% Messed Up (Worse), 25% Easier (Better)
    # These shift depending on the complexity of the action.
    if complexity == "Low":
        # Low complexity actions are reliable.
        prob_intended = 0.70
        prob_messed_up = 0.15 
    elif complexity == "Medium":
        # Medium complexity follows the baseline perfectly.
        prob_intended = 0.50
        prob_messed_up = 0.25
    elif complexity == "High":
        # High complexity actions are risky and prone to complications.
        prob_intended = 0.30
        prob_messed_up = 0.45
    else:
        prob_intended = 0.50
        prob_messed_up = 0.25

    if roll < prob_intended:
        # Action goes exactly as planned
        return projected_impact
        
    elif roll < (prob_intended + prob_messed_up):
        # Action is messed up: The impact is worse than expected.
        # For hackers (negative points), it means they did more damage.
        # For IT/Execs (positive points), it means they gained less defense/resilience.
        if projected_impact < 0:
            variance = random.uniform(1.2, 1.6) # 20-60% more damage
        else:
            variance = random.uniform(0.4, 0.8) # 20-60% less effectiveness
        return int(projected_impact * variance)
        
    else:
        # Action is easier than expected: The impact is favorable.
        # For hackers, they did less damage. For IT/Execs, they gained more defense.
        if projected_impact < 0:
            variance = random.uniform(0.4, 0.8) # 20-60% less damage
        else:
            variance = random.uniform(1.2, 1.6) # 20-60% more effectiveness
        return int(projected_impact * variance)

def evaluate_final_outcome(final_score, min_possible_score, max_possible_score):
    """
    Evaluates the final score and assigns one of three end states.
    Thresholds are mapped mathematically to enforce a global distribution of:
    15% Bankrupt | 65% Damaged but Resilient | 20% Successful
    """
    # Calculate the player's performance as a percentile (0.0 to 1.0)
    score_range = max_possible_score - min_possible_score
    performance_percentile = (final_score - min_possible_score) / score_range
    
    # 0% - 15% of the curve
    if performance_percentile <= 0.15:
        return "Bankrupt", "The company could not withstand the attack and has filed for bankruptcy."
    # 16% - 80% of the curve (65% spread)
    elif performance_percentile <= 0.80:
        return "Damaged but Resilient", "The company suffered heavy losses and reputation damage, but will survive."
    # 81% - 100% of the curve (20% spread)
    else:
        return "Successful", "The company successfully thwarted the worst of the attack and emerged strong."
