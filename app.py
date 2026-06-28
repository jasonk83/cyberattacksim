import streamlit as st
import random

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="CloudStore Command: Mission Control",
    page_icon="🛡️",
    layout="wide"
)

# --- TRUE MULTIPLAYER STATE MANAGEMENT ---
@st.cache_resource
def get_game_state():
    return {
        "scores": {"Trust": 50, "Fiscal": 100, "Op-Eff": 100},
        "round": 1,
        "multiplier": 1.0,
        "history": [],
        "current_phase": "lobby", # Phases: lobby, hacker, company, media, round_recap, hacker_finale, complete
        "active_attack": None,
        "hacker_turn_complete": False,
        "it_choice": None,
        "exec_choice": None,
        "latest_headline": None,
        "finale_result": None, # Tracks the Hacker's final press-your-luck choice
        "team_codes": {
            "hackers": f"hackers{random.randint(100, 999)}",
            "it": f"it{random.randint(100, 999)}",
            "executive": f"executive{random.randint(100, 999)}",
            "media": f"media{random.randint(100, 999)}"
        }
    }

state = get_game_state()

# --- DICTIONARIES & GAME DATA ---
ATTACKS = {
    "Spear-Phishing (Finance Dept)": {
        "desc": "Send highly targeted emails mimicking the CEO to Finance.",
        "impact": "Stealthy initial access. High probability of acquiring CFO credentials."
    },
    "Ransomware Deployment": {
        "desc": "Inject an encryption worm into the primary customer database.",
        "impact": "Maximum visibility. Will drastically cripple Operational Efficiency."
    },
    "Zero-Day Server Exploit": {
        "desc": "Utilize an unpatched vulnerability in cloud hosting architecture.",
        "impact": "Silent system control. Allows for prolonged data exfiltration."
    },
    "Distributed Denial of Service (DDoS)": {
        "desc": "Command a botnet to flood the storefront with junk traffic.",
        "impact": "Immediate disruption of services. Excellent smokescreen."
    }
}

ATTACK_IMPACTS = {
    "Spear-Phishing (Finance Dept)": {
        "it": "⚠️ **UNAUTHORIZED ACCESS:** An internal Finance account is authenticating from an unrecognized IP. Risk of Active Directory compromise.",
        "exec": "📉 **FINANCIAL RISK:** Immediate risk of wire fraud, stock price volatility if leaked, and moderate reputational damage."
    },
    "Ransomware Deployment": {
        "it": "🚨 **ENCRYPTION WORMS DETECTED:** Database nodes unresponsive. File extensions altered. Immediate isolation required.",
        "exec": "📉 **CRITICAL INTERRUPTION:** Customer services offline. $5M ransom demand issued. Extreme risk to stock valuation."
    },
    "Zero-Day Server Exploit": {
        "it": "⚠️ **ANOMALOUS TRAFFIC:** Unrecognized root-level processes executing on core servers. Possible data exfiltration in progress.",
        "exec": "📉 **MASSIVE DATA BREACH:** High probability of customer data loss. Anticipate severe regulatory fines and brand degradation."
    },
    "Distributed Denial of Service (DDoS)": {
        "it": "🚨 **TRAFFIC SPIKE:** Inbound HTTP requests exceeding 500,000 req/sec. Main storefront returning '503 Service Unavailable'.",
        "exec": "📉 **REVENUE LOSS ACTIVE:** E-commerce platform is completely inaccessible. Direct loss of sales revenue."
    }
}

MITIGATION_STRATEGIES = {
    "Isolate network, reset credentials, deploy backups": "1",
    "Monitor traffic and selectively disable accounts": "2",
    "Hire external forensics before taking action": "3",
    "Send security reminder but keep systems online": "4",
    "Ignore alerts to maintain uptime": "5"
}

TECH_SCORES = {
    1: {"1": (-5, -10), "2": (-10, -5), "3": (-10, 0), "4": (0, -15), "5": (-10, -30)},
    2: {"1": (-15, -20), "2": (-20, -10), "3": (-40, -5), "4": (-10, -30), "5": (-30, -50)}
}

MEDIA_HEADLINES = {
    "⭐ HEROIC: CloudStore Thwarts Major Attack; Customer Data Secured": 10,
    "📈 FAVORABLE: CloudStore Responds to Cyber Incident Predictably": 5,
    "🔲 NEUTRAL: Cyber Event Hits CloudStore, Operations Continue": 0,
    "📉 CRITICAL: CloudStore Scrambles Amidst Ongoing Network Issues": -5,
    "💥 DAMNING: Total Incompetence! CloudStore Botches Major Cyber Crisis": -10
}

# --- AUTOMATIC PROGRESSION CHECKER ---
if state["current_phase"] == "company":
    if state["it_choice"] is not None and state["exec_choice"] is not None:
        strategy_level = MITIGATION_STRATEGIES[state["exec_choice"]]
        f_change, o_change = TECH_SCORES[state["round"]][strategy_level]
        
        if state["round"] == 2:
            f_change *= state["multiplier"]
            o_change *= state["multiplier"]
        if state["round"] == 1 and strategy_level == "5":
            state["multiplier"] = 2.0
            
        state["scores"]["Fiscal"] += f_change
        state["scores"]["Op-Eff"] += o_change
        
        state["current_phase"] = "media"
        st.rerun()

# --- URL ROUTING ---
query_params = st.query_params
current_team = query_params.get("team")

# ==========================================
# VIEW 1: MAIN LOBBY & GM DASHBOARD (Projector View)
# ==========================================
if not current_team:
    st.title("🛡️ CLOUDSTORE COMMAND: MISSION CONTROL")
    st.markdown("---")
    
    tab_lobby, tab_gm = st.tabs(["📋 Main Screen", "🔐 GM Access"])
    
    with tab_lobby:
        if state["current_phase"] == "lobby":
            st.header("Simulation Instructions")
            st.write("""
            Welcome to the CloudStore Command Simulation. 
            
            **Rules of Engagement:**
            1. Wait for your Game Master to provide your team's secure link.
            2. Do not share your URL with other teams.
            3. Once the simulation begins, you will only have access to your department's specific tools and intelligence.
            """)
            if st.button("🚀 Start Simulation", type="primary"):
                state["current_phase"] = "hacker"
                st.rerun()
        else:
            # LIVE SCOREBOARD
            st.subheader(f"📡 LIVE STATUS: ROUND {state['round']}")
            
            cols = st.columns(3)
            for i, metric in enumerate(state["scores"].keys()):
                val = state["scores"][metric]
                status_icon = "🟢" if val > 85 else "🟡" if val > 49 else "🔴"
                with cols[i]:
                    st.metric(label=f"{status_icon} {metric}", value=f"{val:.1f} pts")
                    st.progress(max(0, min(100, int(val))))
            st.markdown("---")
            
            # PHASE INDICATORS
            if state["current_phase"] == "hacker":
                st.warning("⚠️ **Alert:** Unrecognized traffic detected. Awaiting threat actor deployment...")
                st.button("🔄 Refresh Screen")
                
            elif state["current_phase"] == "company":
                st.error("🚨 **CRISIS ACTIVE:** IT and Executive teams are deliberating mitigation strategies...")
                st.button("🔄 Refresh Screen")
                
            elif state["current_phase"] == "media":
                st.info("📰 **PRESS LEAK:** Awaiting Media & PR publication...")
                st.button("🔄 Refresh Screen")
                
            elif state["current_phase"] == "round_recap":
                st.success("🗞️ **BREAKING NEWS PUBLISHED**")
                st.markdown(f"### 📰 \"{state['latest_headline']}\"")
                
                if state["round"] == 1:
                    if st.button("▶️ Advance to Round 2", type="primary"):
                        state["round"] = 2
                        state["current_phase"] = "hacker"
                        state["hacker_turn_complete"] = False
                        state["it_choice"] = None
                        state["exec_choice"] = None
                        state["latest_headline"] = None
                        st.rerun()
                elif state["round"] == 2:
                    if st.button("⚠️ Pass Control to Hackers for Final Move", type="primary"):
                        state["current_phase"] = "hacker_finale"
                        st.rerun()
                        
            elif state["current_phase"] == "hacker_finale":
                st.error("🚨 **CRITICAL WARNING:** Anomalous activity detected. Threat actors are weighing a final strike...")
                st.button("🔄 Refresh Screen")

            elif state["current_phase"] == "complete":
                st.header("🏁 FINAL SIMULATION REPORT")
                
                # Render the Hacker's finale decision
                if state["finale_result"] == "caught":
                    st.success("🚓 **FINAL EVENT:** The hackers pushed their luck with a third attack and were apprehended by the FBI! No further damage sustained.")
                elif state["finale_result"] == "success":
                    st.error("💥 **FINAL EVENT:** The hackers successfully launched a devastating follow-on attack, severely damaging CloudStore's remaining reputation (-15 Trust).")
                elif state["finale_result"] == "extract":
                    st.info("🕵️ **FINAL EVENT:** The hackers quietly extracted their payloads and vanished without a trace.")
                
                st.markdown("---")
                avg_score = sum(state["scores"].values()) / 3
                
                if avg_score > 90:
                    st.success(f"### OUTCOME: RESILIENT (Avg: {avg_score:.1f})\nCloudStore survived with minimal long-term damage.")
                elif avg_score > 60:
                    st.warning(f"### OUTCOME: RECOVERING (Avg: {avg_score:.1f})\nThe company is alive, but reputation is scarred.")
                else:
                    st.error(f"### OUTCOME: BANKRUPT (Avg: {avg_score:.1f})\nLegal fees and loss of trust have forced a shutdown.")
                    
                st.info(f"**Timeline Evolution:** {' ➡️ '.join(state['history'])}")

    with tab_gm:
        st.header("Game Master Terminal")
        st.info("Enter the master password to generate team links.")
        gm_password = st.text_input("Admin Password:", type="password")
        
        if gm_password == "admin123":
            st.success("Authentication successful.")
            st.write("Distribute these specific links to your teams for direct access:")
            
            # The full URL to your live Streamlit Community Cloud app
            base_url = "https://cyberattacksim-ksb113.streamlit.app/?team=" 
            
            # Generates the complete, ready-to-copy URL for each role
            st.code(f"Hackers URL:   {base_url}{state['team_codes']['hackers']}")
            st.code(f"IT URL:        {base_url}{state['team_codes']['it']}")
            st.code(f"Executive URL: {base_url}{state['team_codes']['executive']}")
            st.code(f"Media URL:     {base_url}{state['team_codes']['media']}")

# ==========================================
# VIEW 2: HACKER TERMINAL
# ==========================================
elif current_team == state["team_codes"]["hackers"]:
    st.title("😈 Hacker Terminal")
    st.button("🔄 Refresh Data")
    
    if state["current_phase"] == "lobby":
        st.warning("⏳ Waiting for the Game Master to initialize the simulation...")
        
    elif state["current_phase"] == "hacker_finale":
        st.error("### 🎲 THE FINAL GAMBLE")
        st.write("You have successfully executed two waves of attacks. You can extract your team now and disappear into the shadows, or press your luck for one final devastating blow.")
        st.warning("**The Risks:** A follow-on attack has a 75% chance of crippling their reputation further. However, there is a 25% chance the FBI tracks your connection and shuts you down.")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🛑 Extract & Disappear", use_container_width=True):
                state["finale_result"] = "extract"
                state["current_phase"] = "complete"
                st.rerun()
        with c2:
            if st.button("💥 Press the Attack", type="primary", use_container_width=True):
                # 25% chance to get caught, 75% chance of success
                roll = random.random()
                if roll < 0.25:
                    state["finale_result"] = "caught"
                else:
                    state["finale_result"] = "success"
                    state["scores"]["Trust"] -= 15 # Reputation penalty
                    
                state["current_phase"] = "complete"
                st.rerun()
                
    elif not state["hacker_turn_complete"]:
        st.markdown(f"### 🎯 Target: CloudStore (Round {state['round']})")
        attack_choice = st.selectbox("Select Attack Payload:", options=list(ATTACKS.keys()))
        st.info(f"**Description:** {ATTACKS[attack_choice]['desc']}")
        st.warning(f"**Expected Impact:** {ATTACKS[attack_choice]['impact']}")
        
        if st.button("💥 Launch Attack", type="primary"):
            state["active_attack"] = attack_choice
            state["hacker_turn_complete"] = True
            state["current_phase"] = "company"
            st.rerun()
    else:
        st.success(f"Payload deployed: {state['active_attack']}. Monitoring company response...")

# ==========================================
# VIEW 3: IT OPERATIONS CENTER
# ==========================================
elif current_team == state["team_codes"]["it"]:
    st.title("💻 IT Operations Center")
    st.button("🔄 Refresh Data")
    
    if not state["hacker_turn_complete"]:
        st.info("⏳ Systems are currently stable. Waiting for next steps...")
    elif state["current_phase"] == "company":
        st.error(f"### 🚨 INCIDENT ALERT: {state['active_attack']}")
        st.warning(ATTACK_IMPACTS[state['active_attack']]["it"])
        st.markdown("---")
        
        if state["it_choice"] is None:
            it_selection = st.selectbox("Select recommended mitigation strategy:", options=list(MITIGATION_STRATEGIES.keys()))
            if st.button("Submit Recommendation to Execs", type="primary"):
                state["it_choice"] = it_selection
                st.rerun()
        else:
            st.info("✅ Recommendation submitted. Awaiting Executive Boardroom directive...")
            
    elif state["current_phase"] in ["media", "round_recap", "hacker_finale", "complete"]:
        st.header("⚙️ Mitigation Deployment Status")
        if state["it_choice"] != state["exec_choice"]:
            st.error("### ⚠️ OVERRULED BY LEADERSHIP")
            st.warning(f"**Executive Directive Executing:** {state['exec_choice']}")
        else:
            st.success("### ✅ RECOMMENDATION APPROVED")
            st.write(f"**Executing:** {state['it_choice']}")
            
        if state["current_phase"] == "hacker_finale":
            st.warning("🚨 **SYSTEM ALERT:** Network sensors detecting lingering threat actor presence. Awaiting final resolution...")
        else:
            st.info("⏳ Awaiting public fallout / next phase.")

# ==========================================
# VIEW 4: EXECUTIVE BOARDROOM
# ==========================================
elif current_team == state["team_codes"]["executive"]:
    st.title("👔 Executive Boardroom")
    st.button("🔄 Refresh Data")
    
    if not state["hacker_turn_complete"]:
        st.info("⏳ Business operations are nominal. Waiting for next steps...")
    elif state["current_phase"] == "company":
        st.error(f"### 🚨 CRISIS ALERT: {state['active_attack']}")
        st.warning(ATTACK_IMPACTS[state['active_attack']]["exec"])
        st.markdown("---")
        
        if state["exec_choice"] is None:
            if state["it_choice"] is not None:
                st.info(f"**Incoming IT Recommendation:** {state['it_choice']}")
            else:
                st.warning("⚠️ IT has not yet submitted a recommendation.")
                
            exec_selection = st.selectbox("Select official company response:", options=list(MITIGATION_STRATEGIES.keys()))
            if st.button("Issue Binding Directive", type="primary"):
                state["exec_choice"] = exec_selection
                st.rerun()
        else:
            if state["it_choice"] is None:
                st.info("✅ Directive locked in. Waiting for IT to log their initial assessment before deployment...")
                
    elif state["current_phase"] in ["media", "round_recap", "hacker_finale", "complete"]:
        st.success(f"**Directive Executed:** {state['exec_choice']}")
        if state["current_phase"] == "hacker_finale":
            st.warning("🚨 **SYSTEM ALERT:** Unresolved security vulnerabilities reported. Awaiting final resolution...")
        else:
            st.info("⏳ Awaiting public fallout / next phase.")

# ==========================================
# VIEW 5: MEDIA & PR DESK
# ==========================================
elif current_team == state["team_codes"]["media"]:
    st.title("🎤 Media & PR Desk")
    st.button("🔄 Refresh Data")
    
    if state["current_phase"] in ["lobby", "hacker", "company"]:
        st.info("⏳ Scanning the wire. Waiting for the Executives to finalize their response strategy...")
    elif state["current_phase"] == "media":
        st.error("### 🚨 BREAKING: CYBER INCIDENT CONFIRMED")
        st.warning(f"**Leaked Executive Directive:** {state['exec_choice']}")
        headline = st.selectbox("Select Publication Narrative:", options=list(MEDIA_HEADLINES.keys()))
        
        if st.button("📰 Publish Headline", type="primary"):
            t_change = MEDIA_HEADLINES[headline]
            state["scores"]["Trust"] += t_change
            state["latest_headline"] = headline
            
            tech_val = MITIGATION_STRATEGIES[state["exec_choice"]]
            state["history"].append(f"R{state['round']}: Tech({tech_val}) Media({t_change})")
            
            state["current_phase"] = "round_recap"
            st.rerun()
            
    elif state["current_phase"] in ["round_recap", "hacker_finale", "complete"]:
        st.success("### ✅ Headline Published!")
        if state["current_phase"] == "hacker_finale":
            st.warning("⏳ Monitoring the dark web for follow-up claims from the threat actors...")
        else:
            st.info("Look at the Main Command Center screen to see the live score impact.")

else:
    st.error("🚨 Invalid or Expired Team Link. Please contact the Game Master.")
