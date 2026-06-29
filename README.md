# 🛡️ CloudStore Command: Cybersecurity Tabletop Simulation

A multiplayer, role-based tabletop cybersecurity simulation built with Python and Streamlit. 

This application is designed specifically as an interactive educational tool for **undergraduate Information Technology (IT) and Cybersecurity students**. It bridges the gap between technical theory and business reality by simulating the friction, siloed communication, and compounding consequences of a live cyber crisis.

---

## 🎯 Simulation Overview

CloudStore Command moves beyond traditional single-player quizzes. It is a live, turn-based multiplayer exercise where participants are divided into distinct departments. Each team operates "blind" from their own devices, receiving only the intelligence appropriate for their role. 

The simulation is anchored by a **Game Master (GM)** who controls the pace of the game via a central "Projector" screen, routing teams to their isolated dashboards using secure URL parameters.

### Scoring Metrics
The organization's survival is tracked across three fragile metrics:
1. **🟢 Trust (Reputation):** Controlled by the Media & PR team's narrative spin.
2. **🟢 Fiscal (Stock Price):** Impacted by the Executive Boardroom's policy decisions.
3. **🟢 Op-Eff (Operational Efficiency):** Impacted by the IT Department's technical downtime.

---

## 👥 The Roles

### 👑 The Game Master (GM)
The GM is required to facilitate the simulation. Logging into the main application unlocks a password-protected terminal (Default password: `admin123`). The GM generates unique, randomized URLs for each team, displays the Main Lobby scoreboard on a projector, and manually advances the simulation through its phases.

### 😈 Threat Actors (Hackers)
Students act as the adversaries, mapping their attacks to the Cyber Kill Chain. They initiate the crisis by selecting specific intrusion methods and follow-on payloads. At the end of the game, they are presented with a "Press Your Luck" finale to either extract safely or risk FBI apprehension for a final devastating blow.

### 💻 IT Operations Center
Focused entirely on technical mitigation and stopping lateral movement. This team must choose how to respond to the threat technically. Their choices directly impact the company's **Operational Efficiency**, balancing rapid remediation against catastrophic system downtime.

### 👔 Executive Boardroom
Focused on business continuity, legal liability, and investor relations. The Execs receive threat intelligence but must make binding corporate directives. Their choices directly impact the **Fiscal** score. *Note: Executive choices overrule IT recommendations!*

### 🎤 Media & PR Desk
Operating completely blind to the technical realities, the PR team only sees the final directive issued by the Executive Board. They must choose how to spin the corporate response to the public, directly controlling the company's **Trust** score.

---

## 🔄 The Turn-Based Gameplay Loop

The simulation takes place across two distinct rounds, mirroring the lifecycle of a real-world breach.

* **Round 1 (Infiltration):** Hackers attempt to establish a foothold (e.g., Spear Phishing, AI Prompt Injection, Zero-Day Exploits).
* **Round 2 (Execution):** Hackers act on their objectives (e.g., Double Extortion Ransomware, Supply Chain Pivots, Data Exfiltration).

**The Phase Cycle:**
1. **Deployment Phase:** Hackers select their attack vector.
2. **Deliberation Phase:** IT and Executives receive tailored incident briefings. IT submits a technical recommendation; Executives submit the binding corporate directive. 
3. **Spin Phase:** The Media team reviews the Executive directive and publishes a front-page headline.
4. **Recap Phase:** The GM's projector flashes the breaking news headline and updates the live scoreboard before advancing to the next round.

---

## 📁 Repository Structure & Customization

This application is highly modular. The core game logic lives in `app.py`, but all educational briefings, attack descriptions, and impact reports are loaded dynamically from Markdown files. 

Instructors can easily update the course material, vocabulary, and scenario details directly in GitHub without altering the Python code.

```text
cyberattacksim/
│
├── app.py                  # Core Streamlit application & routing logic
├── requirements.txt        # Python dependencies (streamlit)
├── .gitignore              # Ignored system files
│
└── content/                # Dynamic Markdown Briefing Files
    ├── hackers/            # Explanations of attack mechanics & impacts
    ├── it/                 # Technical recovery times and system impacts
    └── exec/               # Financial projections and reputation impacts
