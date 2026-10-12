import streamlit as st
import game_data
from scoring_engine import calculate_actual_impact, evaluate_final_outcome

# --- SESSION STATE INITIALIZATION ---
# This keeps track of the game's progress and score as the user clicks buttons
if 'company_health_score' not in st.session_state:
    st.session_state.company_health_score = 0
if 'current_phase' not in st.session_state:
    st.session_state.current_phase = 'Introduction'
if 'turn_feedback_message' not in st.session_state:
    st.session_state.turn_feedback_message = None
if 'turn_feedback_type' not in st.session_state:
    st.session_state.turn_feedback_type = None

# --- HELPER FUNCTIONS ---
def process_turn(selected_option, next_phase):
    """Processes the player's choice, calculates randomized impact, and advances the game."""
    # 1. Calculate actual randomized impact
    actual_impact = calculate_actual_impact(
        selected_option["projected_impact"], 
        selected_option["complexity"]
    )
    
    # 2. Update overall score
    st.session_state.company_health_score += actual_impact
    
    # 3. Generate feedback based on whether things went as planned, better, or worse
    if actual_impact == selected_option["projected_impact"]:
        st.session_state.turn_feedback_type = "info"
        st.session_state.turn_feedback_message = f"Outcome: The action went exactly as planned. (Impact: {actual_impact})"
        
    elif (selected_option["projected_impact"] < 0 and actual_impact < selected_option["projected_impact"]) or \
         (selected_option["projected_impact"] > 0 and actual_impact < selected_option["projected_impact"]):
        st.session_state.turn_feedback_type = "error"
        st.session_state.turn_feedback_message = f"Complication! The execution was botched, resulting in a worse outcome. (Actual Impact: {actual_impact})"
        
    else:
        st.session_state.turn_feedback_type = "success"
        st.session_state.turn_feedback_message = f"Smooth execution! The action was easier than expected and yielded better results. (Actual Impact: {actual_impact})"
    
    # 4. Advance phase and trigger a UI rerun
    st.session_state.current_phase = next_phase
    st.rerun()

def display_feedback():
    """Displays the result of the previous turn at the top of the new screen."""
    if st.session_state.turn_feedback_message:
        if st.session_state.turn_feedback_type == "info":
            st.info(st.session_state.turn_feedback_message)
        elif st.session_state.turn_feedback_type == "error":
            st.error(st.session_state.turn_feedback_message)
        elif st.session_state.turn_feedback_type == "success":
            st.success(st.session_state.turn_feedback_message)
        
        # Clear it so it doesn't persist on the next screen
        st.session_state.turn_feedback_message = None
        st.session_state.turn_feedback_type = None

def reset_game():
    """Resets all session states to start a new simulation."""
    st.session_state.company_health_score = 0
    st.session_state.current_phase = 'Introduction'
    st.session_state.turn_feedback_message = None
    st.session_state.turn_feedback_type = None
    st.rerun()

# --- APP LAYOUT & GAME LOOP ---
st.title("Cyber Attack Simulation")

# Sidebar for real-time tracking
with st.sidebar:
    st.header("Simulation Status")
    st.metric("Company Health Score", st.session_state.company_health_score)
    st.write("---")
    st.write("**Current Phase:**", st.session_state.current_phase)

# PHASE 1: Introduction
if st.session_state.current_phase == 'Introduction':
    st.header("Welcome to the Simulation")
    st.write("In this exercise, you will experience a cyber attack from three different perspectives: the Hackers, the IT Defense Team, and the Executive Team.")
    st.write("Your choices matter, but beware—in the real world, things do not always go according to plan. The complexity of your choices will introduce varying levels of risk and reward.")
    if st.button("Start Simulation", type="primary"):
        st.session_state.current_phase = 'Hackers'
        st.rerun()

# PHASE 2: Hackers
elif st.session_state.current_phase == 'Hackers':
    display_feedback()
    st.header("Phase 1: The Hackers (Red Team)")
    st.write("You have targeted a mid-sized corporation. Choose your method of attack:")
    
    for option in game_data.hacker_options:
        with st.container():
            st.subheader(option["name"])
            st.write(f"**What this does:** {option['description']}")
            st.write(f"**Assessment:** {option['assessment']}")
            st.write(f"**Complexity:** {option['complexity']} | **Projected Impact:** {option['projected_impact']}")
            if st.button(f"Execute: {option['name']}", key=option["id"]):
                process_turn(option, '
