import streamlit as st
import random
import os

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
        "last_changes": {"Trust": 0, "Fiscal": 0, "Op-Eff": 0}, # Tracks round-by-round impacts
        "round": 1,
        "multiplier": 1.2, 
        "history": [],
        "current_phase": "lobby",
        "active_attack": None,
        "hacker_turn_complete": False,
        "it_choice": None,
        "exec_choice": None,
        "latest_headline": None,
        "finale_result": None,
        "team_codes": {
            "hackers": f"hackers{random.randint(100, 999)}",
            "it": f"it{random.randint(100, 999)}",
            "executive": f"executive{random.randint(100, 999)}",
            "media": f"media{random.randint(100, 999)}"
        }
    }

state = get_game_state()

def reset_simulation():
    """Resets the game state back to default values while keeping the same team URLs."""
    state["scores"] = {"Trust": 50, "Fiscal": 100, "Op-Eff": 100}
    state["last_changes"] = {"Trust": 0, "Fiscal": 0, "Op-Eff": 0}
    state["round"] = 1
    state["multiplier"] = 1.2
    state["history"] = []
    state["current_phase"] = "lobby"
    state["active_attack"] = None
    state["hacker_turn_complete"] = False
    state["it_choice"] = None
    state["exec_choice"] = None
    state["latest_headline"] = None
    state["finale_result"] = None

def get_impact_text(metric, change):
    """Converts raw point changes into descriptive impact text."""
    if change >= 0:
        return f"🟢 **{metric}:** No negative impact ({change} pts). Strategy successfully mitigated damage."
    elif change >= -15:
        return f"🟡 **{metric}:** Minor impact ({change} pts). Acceptable operational or reputational friction."
    elif change >= -30:
        return f"🟠 **{metric}:** Moderate damage ({change} pts). Noticeable disruption and loss of value."
    else:
        return f"🔴 **{metric}:** Severe degradation ({change} pts). Critical failure resulting in massive loss."

# --- DYNAMIC MARKDOWN LOADER ---
def load_briefing(role, attack_name):
    slugs = {
        "Spear Phishing": "phishing",
        "AI Prompt Injection": "prompt_injection",
        "DDoS Smokescreen": "ddos_smokescreen",
        "Zero-Day Network Software Exploit": "zero_day",
        "Double Extortion Ransomware": "double_extortion",
        "Supply Chain Pivot": "supply_chain",
        "Database Integrity Sabotage": "database_sabotage",
        "A.P.T. Data Exfiltration": "apt_exfiltration"
    }
    slug = slugs.get(attack_name, "phishing")
    filepath = os.path.join("content", role, f"{slug}.md")
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"*(Error: Briefing document missing at {filepath})*"

# --- ROUND CONFIGURATIONS & SCORING ---
ATTACKS_R1 = ["Spear Phishing", "AI Prompt Injection", "DDoS Smokescreen", "Zero-Day Network Software Exploit"]
ATTACKS_R2 = ["Double Extortion Ransomware", "Supply Chain Pivot", "Database Integrity Sabotage", "A.P.T. Data Exfiltration"]

IT_CHOICES = {
    "Spear Phishing": {
        "Immediate Enterprise-Wide Password Reset (RTO: 6 Hours)": -15,
        "Targeted Quarantine & EDR Deployment (RTO: 2 Hours)": -5,
        "Silent Monitoring (Honeypot) (RTO: 72 Hours)": -10,
        "Do Nothing (RTO: Indefinite)": -25
    },
    "AI Prompt Injection": {
        "Hard Offline & Revert AI Model (RTO: 24 Hours)": -20,
        "Deploy Aggressive Input Sanitization Filter (RTO: 4 Hours)": -10,
        "Rate-Limit and Alert (RTO: 1 Hour)": -5,
        "Do Nothing (RTO: Indefinite)": -25
    },
    "DDoS Smokescreen": {
        "Blackhole External IP Traffic (RTO: 8 Hours)": -15,
        "Route Traffic via DDoS Scrubbing Service (RTO: 2 Hours)": -5,
        "Ignore External Outage & Hunt Internal Logs (RTO: 48 Hours)": -20,
        "Do Nothing (RTO: Indefinite)": -40
    },
    "Zero-Day Network Software Exploit": {
        "Air-Gap the Vulnerable Server (RTO: 12 Hours)": -20,
        "Implement Custom WAF Rules (Virtual Patching) (RTO: 4 Hours)": -5,
        "Migrate Services to a New OS (RTO: 7 Days)": -30,
        "Do Nothing (RTO: Indefinite)": -50
    },
    "Double Extortion Ransomware": {
        "Burn and Rebuild from Bare Metal (RTO: 14 Days)": -40,
        "Pay Ransom and Run Decryptor Tool (RTO: 48 Hours)": -15,
        "Attempt Manual Cryptanalysis (RTO: 6+ Months)": -60
    },
    "Supply Chain Pivot": {
        "Trigger Emergency Global Kill-Switch (RTO: 24 Hours)": -25,
        "Rollback and Push Clean Patch (RTO: 72 Hours)": -15,
        "Isolate Build Servers for Forensics (RTO: 5 Days)": -30
    },
    "Database Integrity Sabotage": {
        "Revert to 30-Day Old Backup (RTO: 4 Days)": -35,
        "Freeze Database and Audit Manually (RTO: 3 Weeks)": -45,
        "Implement 'Failsafe' Logic Moving Forward (RTO: 24 Hours)": -10
    },
    "A.P.T. Data Exfiltration": {
        "Sever Total Internet Connectivity (RTO: 12 Hours)": -25,
        "Implement Strict Egress Port Blocking (RTO: 6 Hours)": -10,
        "Quietly Route Hacker to a Decoy Server (RTO: 48 Hours)": -15
    }
}

EXEC_CHOICES = {
    "Spear Phishing": {
        "Mandatory Executive Security Audit": -5,
        "Quietly Terminate Responsible Employee": -5,
        "Hire Expensive External Consultants": -10,
        "Ignore / Cover It Up": -20
    },
    "AI Prompt Injection": {
        "Temporarily Suspend All AI Features": -10,
        "Publicly Blame the AI Vendor": -5,
        "Quietly Patch and Downplay": -10
    },
    "DDoS Smokescreen": {
        "Admit the Attack & Apologize on Social Media": -5,
        "Post a 'Scheduled Maintenance' Banner": -15,
        "Purchase Platinum Cloud Defense Mid-Attack": -20
    },
    "Zero-Day Network Software Exploit": {
        "Proactive Public Disclosure & Bounty Program": -5,
        "Secretly Patch and Sign NDAs": -15,
        "Halt All Digital Expansion Projects": -20
    },
    "Double Extortion Ransomware": {
        "Refuse to Pay & Notify the Public": -30,
        "Quietly Pay the Ransom via Intermediary": -15,
        "Attempt to Sue the Software Provider": -25
    },
    "Supply Chain Pivot": {
        "Immediate Global Notification & Apology": -35,
        "Quietly Contact Only 'High Value' Clients": -25,
        "Deny Responsibility (Blame Open-Source Code)": -40
    },
    "Database Integrity Sabotage": {
        "Halt All Operations & Offer Blanket Refunds": -25,
        "Keep Operating and Handle Complaints Individually": -15,
        "Request an Emergency SEC Trading Halt": -35
    },
    "A.P.T. Data Exfiltration": {
        "Full GDPR/CCPA Disclosure & Free Identity Theft Protection": -25,
        "Downplay the Sensitivity of the Stolen Data": -15,
        "Resignation of the CEO and CISO": -35
    }
}

# --- AUTOMATIC PROGRESSION CHECKER ---
if state["current_phase"] == "company":
    if state["it_choice"] is not None and state["exec_choice"] is not None:
        o_change = IT_CHOICES[state["active_attack"]][state["it_choice"]]
        f_change = EXEC_CHOICES[state["active_attack"]][state["exec_choice"]]
        
        if state["round"] == 2:
            o_change = int(o_change * state["multiplier"])
            f_change = int(f_change * state["multiplier"])
            
        state["scores"]["Op-Eff"] += o_change
        state["scores"]["Fiscal"] += f_change
        
        # Save changes for the impact report
        state["last_changes"]["Op-Eff"] = o_change
        state["last_changes"]["Fiscal"] = f_change
        
        state["current_phase"] = "media"
        st.rerun()

# --- URL ROUTING ---
query_params = st.query_params
current_team = query_params.get("team")

# ==========================================
# VIEW 1: MAIN LOBBY, GM DASHBOARD & PRACTICE
# ==========================================
if not current_team:
    st.title("🛡️ CLOUDSTORE COMMAND: MISSION CONTROL")
    st.markdown("---")
    
    tab_lobby, tab_gm, tab_practice = st.tabs(["📋 Main Screen", "🔐 GM Access", "🎓 Instructor Practice"])
    
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
            st.info("Mechanics: The Game Master must click 'Start Simulation' below to generate the initial scenario and pass control to the Hacker team.")
            if st.button("🚀 Start Simulation", type="primary"):
                state["current_phase"] = "hacker"
                st.rerun()
        else:
            st.subheader(f"📡 LIVE STATUS: ROUND {state['round']}")
            
            cols = st.columns(3)
            for i, metric in enumerate(state["scores"].keys()):
                val = state["scores"][metric]
                status_icon = "🟢" if val > 85 else "🟡" if val > 49 else "🔴"
                with cols[i]:
                    st.metric(label=f"{status_icon} {metric}", value=f"{val:.1f} pts")
                    st.progress(max(0, min(100, int(val))))
            st.markdown("---")
            
            if state["current_phase"] == "hacker":
                st.warning("⚠️ **Alert:** Unrecognized traffic detected. Awaiting threat actor deployment...")
                st.info("Mechanics: Awaiting Hacker team to select and launch their payload. Refresh screen to check for updates.")
                st.button("🔄 Refresh Screen")
                
            elif state["current_phase"] == "company":
                st.error("🚨 **CRISIS ACTIVE:** IT and Executive teams are deliberating mitigation strategies...")
                st.info("Mechanics: Awaiting IT and Executive teams to submit their respective directives. Refresh screen to check for updates.")
                st.button("🔄 Refresh Screen")
                
            elif state["current_phase"] == "media":
                st.info("📰 **PRESS LEAK:** Awaiting Media & PR publication...")
                st.info("Mechanics: Awaiting Media team to publish their spun headline. Refresh screen to check for updates.")
                st.button("🔄 Refresh Screen")
                
            elif state["current_phase"] == "round_recap":
                st.success("🗞️ **BREAKING NEWS PUBLISHED**")
                st.markdown(f"### 📰 \"{state['latest_headline']}\"")
                
                st.markdown("### 📉 Impact Analysis")
                st.write(get_impact_text("Operational Efficiency", state['last_changes']['Op-Eff']))
                st.write(get_impact_text("Fiscal/Stock Score", state['last_changes']['Fiscal']))
                st.write(get_impact_text("Trust/Reputation Score", state['last_changes']['Trust']))
                
                st.markdown("---")
                st.info("Mechanics: Review the impact above. The Game Master must click the button below to initiate the next phase.")
                
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
                st.info("Mechanics: Awaiting Hacker team to decide whether to extract or press the attack.")
                st.button("🔄 Refresh Screen")

            elif state["current_phase"] == "complete":
                st.header("🏁 FINAL SIMULATION REPORT")
                
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
                
                st.markdown("---")
                st.info("Mechanics: The simulation has concluded. The Game Master can reset the game parameters using the button below. Team URLs will remain unchanged.")
                if st.button("🔄 Restart Sim", type="primary"):
                    reset_simulation()
                    st.rerun()

    with tab_gm:
        st.header("Game Master Terminal")
        st.info("Enter the master password to generate team links.")
        gm_password = st.text_input("Admin Password:", type="password")
        
        if gm_password == "admin123":
            st.success("Authentication successful.")
            st.write("Distribute these specific links to your teams for direct access:")
            
            base_url = "https://cyberattacksim-ksb113.streamlit.app/?team=" 
            
            st.code(f"Hackers URL:   {base_url}{state['team_codes']['hackers']}")
            st.code(f"IT URL:        {base_url}{state['team_codes']['it']}")
            st.code(f"Executive URL: {base_url}{state['team_codes']['executive']}")
            st.code(f"Media URL:     {base_url}{state['team_codes']['media']}")

    with tab_practice:
        st.header("Instructor Practice Terminal")
        st.info("Test the entire simulation flow from a single screen. (Use the same admin password).")
        practice_password = st.text_input("Practice Password:", type="password", key="practice_pwd")
        
        if practice_password == "admin123":
            st.success("Practice Mode Unlocked.")
            st.markdown("---")
            
            if state["current_phase"] == "lobby":
                st.write("Press **Start Simulation** on the Main Screen tab to begin practice.")
                
            elif state["current_phase"] == "hacker":
                st.markdown(f"### 😈 Hacker Turn (Round {state['round']})")
                options_list = ATTACKS_R1 if state["round"] == 1 else ATTACKS_R2
                
                attack_choice = st.selectbox("Select Payload:", options=options_list, key="prac_hack_sel")
                st.markdown(load_briefing("hackers", attack_choice))
                
                if st.button("💥 Launch Attack (Practice)", type="primary", key="prac_hack_btn"):
                    state["active_attack"] = attack_choice
                    state["hacker_turn_complete"] = True
                    state["current_phase"] = "company"
                    st.rerun()
                    
            elif state["current_phase"] == "company":
                st.markdown("### 🏢 Company Turn (IT & Execs)")
                st.error(f"**Active Incident:** {state['active_attack']}")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("#### 💻 IT Department")
                    if state["it_choice"] is None:
                        it_options = list(IT_CHOICES[state["active_attack"]].keys())
                        it_selection = st.selectbox("IT Mitigation:", options=it_options, key="prac_it_sel")
                        if st.button("Submit IT", key="prac_it_btn"):
                            state["it_choice"] = it_selection
                            st.rerun()
                    else:
                        st.success(f"IT Selected: {state['it_choice']}")
                        
                with c2:
                    st.markdown("#### 👔 Executive Board")
                    if state["exec_choice"] is None:
                        exec_options = list(EXEC_CHOICES[state["active_attack"]].keys())
                        exec_selection = st.selectbox("Exec Directive:", options=exec_options, key="prac_exec_sel")
                        if st.button("Submit Exec", key="prac_exec_btn"):
                            state["exec_choice"] = exec_selection
                            st.rerun()
                    else:
                        st.success(f"Execs Selected: {state['exec_choice']}")
                        
            elif state["current_phase"] == "media":
                st.markdown("### 🎤 Media & PR Turn")
                st.warning(f"**Leaked Directive:** {state['exec_choice']}")
                
                DYNAMIC_HEADLINES = {
                    f"⭐ PRAISED: Market Reacts Positively to CloudStore's Decision to {state['exec_choice']}": 15,
                    f"📈 FAVORABLE: CloudStore Navigates Crisis, Opts to {state['exec_choice']}": 5,
                    f"🔲 NEUTRAL: CloudStore Incident Underway, Strategy is to {state['exec_choice']}": 0,
                    f"📉 CRITICAL: Experts Question CloudStore's Move to {state['exec_choice']}": -10,
                    f"💥 DAMNING: Total Backfire as CloudStore Attempts to {state['exec_choice']}": -25
                }
                
                headline = st.selectbox("Select Narrative:", options=list(DYNAMIC_HEADLINES.keys()), key="prac_media_sel")
                if st.button("📰 Publish Headline (Practice)", key="prac_media_btn"):
                    t_change = DYNAMIC_HEADLINES[headline]
                    state["scores"]["Trust"] += t_change
                    state["latest_headline"] = headline
                    state["last_changes"]["Trust"] = t_change
                    state["history"].append(f"R{state['round']}: Exec({state['exec_choice']}) Media Spin({t_change} pts)")
                    state["current_phase"] = "round_recap"
                    st.rerun()
                    
            elif state["current_phase"] == "hacker_finale":
                st.markdown("### 🎲 The Final Gamble")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("🛑 Extract & Disappear", key="prac_ext_btn"):
                        state["finale_result"] = "extract"
                        state["current_phase"] = "complete"
                        st.rerun()
                with c2:
                    if st.button("💥 Press the Attack", type="primary", key="prac_press_btn"):
                        roll = random.random()
                        if roll < 0.25:
                            state["finale_result"] = "caught"
                        else:
                            state["finale_result"] = "success"
                            state["scores"]["Trust"] -= 15
                        state["current_phase"] = "complete"
                        st.rerun()
                        
            elif state["current_phase"] in ["round_recap", "complete"]:
                st.info("Check the **Main Screen** tab to advance the round or view final results.")
                if state["current_phase"] == "complete":
                    if st.button("🔄 Restart Sim (Practice)", key="prac_restart_btn"):
                        reset_simulation()
                        st.rerun()

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
        
        st.info("Mechanics: Click either 'Extract & Disappear' to end the simulation immediately, or 'Press the Attack' to roll the probability engine for a final outcome.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🛑 Extract & Disappear", use_container_width=True):
                state["finale_result"] = "extract"
                state["current_phase"] = "complete"
                st.rerun()
        with c2:
            if st.button("💥 Press the Attack", type="primary", use_container_width=True):
                roll = random.random()
                if roll < 0.25:
                    state["finale_result"] = "caught"
                else:
                    state["finale_result"] = "success"
                    state["scores"]["Trust"] -= 15
                    
                state["current_phase"] = "complete"
                st.rerun()
                
    elif not state["hacker_turn_complete"]:
        
        if state["round"] == 1:
            st.markdown(f"### 🎯 Target: CloudStore (Round 1)")
            st.subheader("🕵️ Infiltration Choice")
            options_list = ATTACKS_R1
        else:
            st.markdown(f"### 🎯 Target: CloudStore (Round 2)")
            st.subheader("💥 Attack Execution")
            options_list = ATTACKS_R2
            
        st.info("Mechanics: Select an option from the dropdown menu and click 'Launch Attack' to finalize your decision and advance the simulation to the Company Phase.")
        attack_choice = st.selectbox("Select Payload:", options=options_list)
        
        st.markdown(load_briefing("hackers", attack_choice))
        
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
        
        st.markdown(load_briefing("it", state["active_attack"]))
        st.markdown("---")
        
        if state["it_choice"] is None:
            st.info("Mechanics: Review the incident details, select a mitigation strategy from the dropdown, and click 'Deploy Technical Response' to submit your choice. The simulation will not advance to the Media phase until both the IT and Executive teams have submitted their decisions.")
            it_options = list(IT_CHOICES[state["active_attack"]].keys())
            it_selection = st.selectbox("Select Technical Mitigation Protocol:", options=it_options)
            
            if st.button("Deploy Technical Response", type="primary"):
                state["it_choice"] = it_selection
                st.rerun()
        else:
            st.info("✅ Technical response deployed. Awaiting Executive Boardroom directive...")
            
    elif state["current_phase"] in ["media", "round_recap", "hacker_finale", "complete"]:
        st.header("⚙️ Mitigation Deployment Status")
        st.success("### ✅ TECHNICAL PROTOCOL EXECUTED")
        st.write(f"**IT Department Action:** {state['it_choice']}")
        st.write(f"**Executive Board Directive:** {state['exec_choice']}")
            
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
        
        st.markdown(load_briefing("exec", state["active_attack"]))
        st.markdown("---")
        
        if state["exec_choice"] is None:
            if state["it_choice"] is not None:
                st.info(f"**IT Department has logged their technical response.**")
            else:
                st.warning("⚠️ IT is currently deliberating their response.")
                
            st.info("Mechanics: Review the incident details, select a corporate directive from the dropdown, and click 'Issue Binding Directive' to submit your choice. The simulation will not advance to the Media phase until both the IT and Executive teams have submitted their decisions.")
            exec_options = list(EXEC_CHOICES[state["active_attack"]].keys())
            exec_selection = st.selectbox("Select Official Corporate Directive:", options=exec_options)
            
            if st.button("Issue Binding Directive", type="primary"):
                state["exec_choice"] = exec_selection
                st.rerun()
        else:
            if state["it_choice"] is None:
                st.info("✅ Directive locked in. Waiting for IT to log their final technical assessment before deployment...")
                
    elif state["current_phase"] in ["media", "round_recap", "hacker_finale", "complete"]:
        st.header("📊 Business Response Status")
        st.success("### ✅ CORPORATE DIRECTIVE ISSUED")
        st.write(f"**Executive Board Directive:** {state['exec_choice']}")
        st.write(f"**IT Department Action:** {state['it_choice']}")
        
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
        st.write("Based on the Executive Team's specific choice, how will you frame this to the public?")
        
        DYNAMIC_HEADLINES = {
            f"⭐ PRAISED: Market Reacts Positively to CloudStore's Decision to {state['exec_choice']}": 15,
            f"📈 FAVORABLE: CloudStore Navigates Crisis, Opts to {state['exec_choice']}": 5,
            f"🔲 NEUTRAL: CloudStore Incident Underway, Strategy is to {state['exec_choice']}": 0,
            f"📉 CRITICAL: Experts Question CloudStore's Move to {state['exec_choice']}": -10,
            f"💥 DAMNING: Total Backfire as CloudStore Attempts to {state['exec_choice']}": -25
        }
        
        st.info("Mechanics: Review the Executive Directive, select a narrative from the dropdown, and click 'Publish Headline' to lock in your decision and advance the simulation to the Round Recap phase.")
        headline = st.selectbox("Select Publication Narrative:", options=list(DYNAMIC_HEADLINES.keys()))
        
        if st.button("📰 Publish Headline", type="primary"):
            t_change = DYNAMIC_HEADLINES[headline]
            state["scores"]["Trust"] += t_change
            state["latest_headline"] = headline
            state["last_changes"]["Trust"] = t_change
            
            state["history"].append(f"R{state['round']}: Exec({state['exec_choice']}) Media Spin({t_change} pts)")
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
