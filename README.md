# 🛡️ CloudStore Command: Cyber Incident Response Tabletop Simulation

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cyberattacksim-ksb113.streamlit.app/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Educational Tool](https://img.shields.io/badge/Pedagogy-Cybersecurity%20%26%20IT%20Education-emerald.svg)](#-university-instructor--facilitator-package)

> **Live Simulation Link:** [https://cyberattacksim-ksb113.streamlit.app/](https://cyberattacksim-ksb113.streamlit.app/)  
> *(No installation required — runs directly in modern mobile and desktop web browsers)*

---

**CloudStore Command** is an interactive, role-based multiplayer cyber incident tabletop simulation developed specifically for **undergraduate Information Technology, Cybersecurity, and Business Information Systems courses**. 

Moving beyond traditional static quizzes and isolated technical labs, CloudStore Command simulates the true friction of an enterprise breach: **asymmetric information**, **siloed inter-departmental communication**, **compounding business disruption**, and **high-stakes executive trade-offs** under a ticking clock.

```
                           ┌──────────────────────────────┐
                           │   📽️ CLASSROOM PROJECTOR     │
                           │   (?team=projector)          │
                           │   Live Telemetry & Teleprompter│
                           └──────────────┬───────────────┘
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │    👑 GAME MASTER MISSION CONTROL     │
                      │    (?team=main | Passcode: admin123)  │
                      └───────────────────┬───────────────────┘
                                          │
       ┌──────────────────┬───────────────┴───────────────┬──────────────────┐
       │                  │                               │                  │
       ▼                  ▼                               ▼                  ▼
┌──────────────┐   ┌──────────────┐                ┌──────────────┐   ┌──────────────┐
│  💀 THREAT   │   │    🛡️ IT     │                │ 💼 EXECUTIVE │   │   🎤 MEDIA   │
│   ACTORS     │   │   DEFENSE    │                │  BOARDROOM   │   │   & PR DESK  │
│(?team=hackers│   │  (?team=it)  │                │ (?team=exec) │   │(?team=media) │
└──────┬───────┘   └──────┬───────┘                └──────┬───────┘   └──────┬───────┘
       │                  │                               │                  │
       │ Deploys Vector   │ Recommends Technical Plan     │ Issues Directive │ Spins Story
       └─────────────────►└──────────────────────────────►└─────────────────►└───────────► Round Debrief
```

---

## 📑 Table of Contents

1. [🧑‍🏫 University Instructor & Facilitator Package](#-university-instructor--facilitator-package)
   - [Educational Mission & Learning Objectives](#educational-mission--learning-objectives)
   - [The Four Student Roles & Perspectives](#the-four-student-roles--perspectives)
   - [Classroom Architecture & BYOD Setup](#classroom-architecture--byod-setup)
   - [Facilitator Runbook & GM Controls](#facilitator-runbook--gm-controls)
   - [Sample Classroom Lesson Plans (50-Min & 75-Min)](#sample-classroom-lesson-plans)
   - [Post-Simulation Debrief & Discussion Prompts](#post-simulation-debrief--discussion-prompts)
2. [🎲 Gameplay Mechanics & Scoring System](#-gameplay-mechanics--scoring-system)
   - [The Unified Enterprise Health Metric (HP)](#the-unified-enterprise-health-metric-hp)
   - [The Turn-Based Incident Lifecycle](#the-turn-based-incident-lifecycle)
   - [Scoring Engine: Formulas & Reality Check Friction](#scoring-engine-formulas--reality-check-friction)
   - [The Adversary Final Gambit](#the-adversary-final-gambit)
3. [⚙️ Technical Architecture & Cloud Deployment](#️-technical-architecture--cloud-deployment)
   - [Streamlit Community Cloud 1-Click Deployment](#streamlit-community-cloud-1-click-deployment)
   - [URL Parameter Routing & State Architecture](#url-parameter-routing--state-architecture)
   - [Repository Directory Structure](#repository-directory-structure)
   - [Customizing Scenarios via Markdown Files](#customizing-scenarios-via-markdown-files)
   - [Automated Test Suite & Verification](#automated-test-suite--verification)

---

# 🧑‍🏫 University Instructor & Facilitator Package

## Educational Mission & Learning Objectives

In the real world, cyber crisis management rarely fails solely due to technical incompetence; it fails because of **organizational misalignment, poor communication, and conflicting incentives**. 

CloudStore Command places students into authentic operational friction points where:
* **The IT Security Team** wants to isolate networks and wipe systems to guarantee containment, but must answer for crippling business downtime.
* **The Executive Board** is legally bound to SEC materiality disclosures and quarterly revenue targets, often seeking compromises that inadvertently leave systems vulnerable.
* **The Media & PR Team** must shape public trust and stock perception while operating completely blind to the actual technical root causes.
* **The Threat Actors** weigh destructive attacks against their accumulated telemetry exposure, knowing that noisy operations increase law enforcement interception risk.

### Student Learning Outcomes (SLOs)
By completing this simulation, students will be able to:
1. **Analyze Cyber Kill Chain progression** across multi-stage intrusions (Initial Access $\rightarrow$ Lateral Movement $\rightarrow$ Action on Objectives).
2. **Quantify the Recovery Time Objective (RTO) dilemma**, balancing catastrophic network downtime against incomplete threat containment.
3. **Evaluate Corporate Governance & Regulatory Exposure**, including SEC Form 8-K four-day material breach disclosure mandates, GDPR compliance, and class-action liabilities.
4. **Demonstrate Cross-Disciplinary Crisis Communication**, translating technical telemetry into board-level risk assessments and public statements.
5. **Critique the Pitfalls of Passive Defense**, understanding why low-monitoring or "inaction" stances compound attacker entrenchment.

---

## The Four Student Roles & Perspectives

Divide your class into four distinct operational groups. Each team accesses a dedicated terminal URL with customized intelligence dossiers:

| Team Role | Focus & Learning Perspective | Key Dilemma / Decision Space |
| :--- | :--- | :--- |
| **💀 Threat Actors**<br>`?team=hackers` | **Adversary Operations & Kill Chain**<br>Simulates external threat actors targeting CloudStore's cloud e-commerce enterprise. | **Stealth vs. Destructive Impact:** Loud attacks inflict high initial damage but generate telemetry noise, increasing the risk of capture during the Final Gambit. |
| **🛡️ IT Defense Center**<br>`?team=it` | **Technical Incident Response & Containment**<br>First-line SOC defenders analyzing telemetry, isolating subnets, and deploying EDR agents. | **Eradication vs. Downtime:** Aggressive options guarantee containment but cause heavy operational downtime; passive options keep storefronts open but risk unchecked lateral spread. |
| **💼 Executive Boardroom**<br>`?team=exec` | **Business Continuity & Crisis Governance**<br>C-suite leadership balancing legal liabilities, SEC disclosures, customer trust, and quarterly earnings. | **Governance Mandate:** The Board reviews IT's proposal and decides whether to **Agree with IT** (accept downtime), **Compromise** (halve downtime and containment), or **Override IT** (keep systems running, triggering an override penalty). |
| **🎤 Media & PR Desk**<br>`?team=media` | **Public Relations & Crisis Communications**<br>Corporate communications team handling news cycles, social media panic, and customer transparency. | **Spin vs. Reality:** Chooses from 4 breaking headline tiers (Sensationalist, Critical, Balanced, Favorable). Public resonance rolls determine whether the narrative stabilizes or erodes customer trust. |

---

## Classroom Architecture & BYOD Setup

CloudStore Command is built for frictionless classroom execution using a **Bring-Your-Own-Device (BYOD)** model. It supports anywhere from **8 to 100+ students** simultaneously.

```
                              ┌───────────────────────────────────┐
                              │     FRONT OF ROOM PROJECTOR       │
                              │     https://.../?team=projector   │
                              │   (Clean Big-Screen Presentation) │
                              └───────────────────────────────────┘
                                                ▲
                                                │ Global Sync (2s)
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 STUDENT DEVICE BRING-YOUR-OWN-DEVICE                            │
│                                                                                                 │
│  💀 THREAT ACTORS TABLE           🛡️ IT DEFENSE TABLE             💼 EXECUTIVE BOARDROOM TABLE  │
│  https://.../?team=hackers       https://.../?team=it            https://.../?team=exec        │
│  ┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐   │
│  │ Captain: hacker123 ⭐   │     │ Captain: tech456 ⭐     │     │ Captain: board789 ⭐    │   │
│  │ (Submits Official Move) │     │ (Submits Official Move) │     │ (Submits Official Move) │   │
│  ├─────────────────────────┤     ├─────────────────────────┤     ├─────────────────────────┤   │
│  │ Viewers (All Students)  │     │ Viewers (All Students)  │     │ Viewers (All Students)  │   │
│  │ • Read Intel Dossiers   │     │ • Read Intel Dossiers   │     │ • Read Intel Dossiers   │   │
│  │ • Cast Straw Poll Votes │     │ • Cast Straw Poll Votes │     │ • Cast Straw Poll Votes │   │
│  └─────────────────────────┘     └─────────────────────────┘     └─────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 1. Dedicated Class Projector View (`?team=projector`)
* Open this view on the classroom podium computer or projector.
* Completely strips the sidebar and administrative buttons for an immersive broadcast display.
* Displays the **Threatening Countdown Clock**, **Enterprise Health Bar**, **Active Breach Banner**, **Live Team Deliberation Badges**, and the **Student Cybersecurity Vocabulary Glossary**.
* Automatically synchronizes state changes across the room every 2 seconds without requiring manual page reloads.

### 2. Single-URL Captain vs. Viewer Access
* Distribute **one uniform link per team** (e.g., `.../?team=it`).
* **All students join as Viewers by default**: They read intelligence dossiers, review incident data, and participate in real-time **Team Straw Polls**.
* **One designated Team Captain unlocks administrative control**: The student designated as Captain enters their team's 3-digit passcode in the sidebar to launch team polls and submit binding team directives.

### 3. Dedicated Solo Instructor Sandbox (`?team=instructor`)
* Need to rehearse the simulation before class or preview every screen solo?
* Navigate to `?team=instructor` and enter passcode **`tryit123`**.
* Runs on an **isolated, private game state** that does not interfere with live multiplayer games.
* Renders the GM Mission Control Console at the top and walks you sequentially through each team's Captain terminal as decisions are made.

---

## Facilitator Runbook & GM Controls

As the Instructor/Game Master (GM), you orchestrate the pacing from the **GM Mission Control Console** (`?team=main`).

### Authentication & Passcodes
* **Game Master Password**: `admin123`
* **Single-Player Instructor Sandbox**: `tryit123`
* **Team Captain Passcodes**: Generated dynamically at startup with randomized 3-digit suffixes (e.g., `hacker492`, `tech817`, `board305`, `press621`). The GM can view, copy, or distribute these directly from the GM console sidebar.

### Game Master Control Capabilities
* **Session Length Configuration**: Choose between a standard **2-Round Scenario** (recommended for 50-minute lectures) or an extended **3-Round Scenario** (recommended for 75–90 minute labs).
* **Threat Severity Multipliers**: Scale the difficulty on the fly (1.0x Normal, 1.2x Elevated, 1.5x Severe, 2.0x Catastrophic).
* **Timer Controls**: Pause, Resume, or Reset the phase countdown timer if class debate requires more time.
* **Manual Enterprise HP Adjustments (Penalties / Bonuses)**:
  * **➕ Add +10 HP (Penalize Hackers / Media)**: Grant +10 HP to Enterprise Vitality if Threat Actors or Media stall past the countdown timer.
  * **➖ Subtract -10 HP (Penalize IT / Exec)**: Deduct -10 HP from Enterprise Vitality if IT or Executives miss their deliberation window.
* **Instant Round Rollback (Undo)**: Revert the previous turn immediately if a team misclicks or wishes to re-examine a decision branch.

---

## Sample Classroom Lesson Plans

### ⏱️ 50-Minute Standard Lecture Agenda

| Time Window | Phase / Activity | Facilitator Action & Classroom Dynamic |
| :---: | :--- | :--- |
| **00:00 – 00:08** | **Mission Briefing & Team Setup** | Project `?team=projector`. Display team URLs on whiteboard. Assign students into 4 groups. Announce Captain passcodes to designated group leaders. |
| **00:08 – 00:10** | **Simulation Launch** | GM clicks **Start Round 1** on `?team=main`. Countdown begins. |
| **00:10 – 00:22** | **Round 1 (Initial Infiltration)** | • **Hackers (3-5 min)** select entry vector (Phishing, CVE Exploit, AI Prompt Injection).<br>• **IT Defense (4 min)** reviews incident alert and submits technical containment plan.<br>• **Executive Board (3 min)** debates IT's proposal and issues corporate governance directive.<br>• **Media & PR (2 min)** publishes breaking front-page headline. |
| **00:22 – 00:26** | **Round 1 Debrief & Reality Check** | Projector updates with Net HP change. Facilitator highlights the **Surprise & Reality Check** callout (e.g., why passive monitoring backfired or why board overrides triggered penalties). |
| **00:26 – 00:38** | **Round 2 (Execution & Lateral Movement)** | • **Hackers** deploy secondary payload (PII Exfiltration, Database Sabotage, Ransomware Lockout).<br>• **IT Defense** deliberates aggressive bare-metal rebuild vs. partial isolation.<br>• **Exec Board** faces SEC materiality and legal liabilities.<br>• **Media** releases follow-up investigative coverage. |
| **00:38 – 00:41** | **Round 2 Debrief & Trajectory** | Review updated Enterprise Health gauge. Gauge whether the company is trending toward Solvency or Bankruptcy. |
| **00:41 – 00:44** | **Adversary Final Gambit** | Red Team deliberates live: **Press Attack** into secondary payment gateways or **Safely Retreat**. If they press, detection probability scales against their past attack noise! |
| **00:44 – 00:50** | **Final Outcome Evaluation & Debrief** | The final outcome screen renders (Win, Survive, or Bankrupt). Facilitator leads a 6-minute targeted debrief. |

### ⏱️ 75-Minute Seminar / Laboratory Agenda

| Time Window | Focus Area | Pedagogical Highlights |
| :---: | :--- | :--- |
| **00:00 – 00:15** | **Pre-Flight Case Study & Regulatory Framing** | Discuss real-world incidents (e.g., MGM Resorts, Colonial Pipeline, SolarWinds). Review SEC Form 8-K 4-day disclosure rules and the glossary. |
| **00:15 – 00:30** | **Round 1 Deliberation with Intra-Team Straw Polls** | Encourage vigorous intra-team debate. Viewers cast straw poll votes on their phones before Captains commit decisions. |
| **00:30 – 00:45** | **Round 2 Deep Incident Containment** | IT and Executives engage in cross-table negotiations. The Board challenges IT on customer outage costs. |
| **00:45 – 00:55** | **Round 3 Advanced Persistence (Optional)** | (If running a 3-Round scenario): Supply Chain API Poisoning, Volumetric DDoS, and UEFI Firmware persistence. |
| **00:55 – 01:03** | **Adversary Final Gambit Finale** | Red Team debates risk vs. reward on the big screen. Detection checks detonate or resolve. |
| **01:03 – 01:15** | **Comprehensive Post-Mortem & Written Reflection** | Guided whole-class retrospective connecting tabletop events to course textbook concepts. |

---

## Post-Simulation Debrief & Discussion Prompts

Facilitating an effective post-mortem turns gameplay tension into lasting conceptual retention. Use these targeted discussion prompts:

### 1. The IT vs. Boardroom Disconnect
> *"When the IT Department proposed a 24-hour total network lockout to stop lateral movement, why did the Executive Board hesitate or override? If the Board overruled IT, what was the financial and regulatory consequence?"*
* **Core Takeaway:** Security does not operate in a vacuum. Disabling business operations to achieve 100% security can destroy business viability just as quickly as malware, yet ignoring technical advice invites catastrophic override penalties.

### 2. The Illusion of Zero-Downtime Defense (Inaction Backfire)
> *"In several rounds, IT had the option to perform 'Passive Monitoring' or 'Live Hotpatching' with 0 hours of downtime. Did your team select this? What happened during the round recap?"*
* **Core Takeaway:** Inactive or overly timid defense often backfires. Threat actors use the lack of friction to entrench themselves deeper, leading to compound damage multipliers (+5% to +25%).

### 3. Information Asymmetry & The Fog of War
> *"To the Media & PR team: When you wrote your breaking headlines, what technical details did you actually know? How did executive communication affect your ability to reassure the public?"*
* **Core Takeaway:** Corporate communications during an active breach operate under incomplete and conflicting intelligence. Overpromising security before forensic validation destroys brand equity when secondary leaks occur.

### 4. Adversary Economics & Operational Security (OPSEC)
> *"To the Threat Actors: Why did your detection probability during the Final Gambit rise or fall? How did your choice of early attack vectors dictate your final escape risk?"*
* **Core Takeaway:** Cyber adversaries face economic and operational trade-offs. Noisy, destructive exploits leave substantial digital fingerprints across EDR and network sensors, while stealthy campaigns preserve escape avenues.

---

# 🎲 Gameplay Mechanics & Scoring System

## The Unified Enterprise Health Metric (HP)

The survival of CloudStore is tracked through a single, responsive **Enterprise Health (HP)** score starting at **100.0 HP**. 

Rather than treating reputation, technology, and finances as disconnected silos, all departmental decisions and real-world friction feed into this unified vitality index:

```
                  ┌────────────────────────────────────────────────────────┐
                  │          ENTERPRISE HEALTH VITALITY (100 HP)           │
                  └───────────────────────────┬────────────────────────────┘
                                              │
           ┌──────────────────────────────────┼──────────────────────────────────┐
           ▼                                  ▼                                  ▼
┌──────────────────────┐           ┌──────────────────────┐           ┌──────────────────────┐
│   💥 BANKRUPTCY      │           │      🛡️ SURVIVED     │           │       🏆 WIN         │
│   Health < 32.0 HP   │           │   32.0 HP – 70.9 HP  │           │   Health ≥ 71.0 HP   │
│   (Target: ~30%)     │           │    (Target: ~60%)    │           │    (Target: ~10%)    │
│ Chapter 11 insolvency│           │ Enterprise damaged   │           │ Exceptional resilience│
│ & liquidation        │           │ but solvent & viable │           │ and governance       │
└──────────────────────┘           └──────────────────────┘           └──────────────────────┘
*(Thresholds calibrated for 2-Round Scenarios; 3-Round Scenarios calibrate to: Bankrupt < 17 HP, Win ≥ 54 HP)*
```

---

## The Turn-Based Incident Lifecycle

Each round follows a strict sequential progression representing the real-world escalation of a cyber crisis:

```
[ LOBBY BRIEFING ]
       │
       ▼
1. THREAT ACTOR INFILTRATION (5 Min)
   Adversaries select attack vector: Complexity, Anonymity, and Damage Potential.
       │
       ▼
2. IT CONTAINMENT DELIBERATION (5 Min)
   SOC receives incident alert; deliberates RTO downtime trade-offs and recommends plan.
       │
       ▼
3. EXECUTIVE CRISIS GOVERNANCE (3 Min)
   Boardroom reviews IT proposal; issues binding directive (Agree, Compromise, or Override).
       │
       ▼
4. PRESS SCRUM & MEDIA SPIN (5 Min)
   PR team reviews public posture; selects breaking news headline across 4 editorial tiers.
       │
       ▼
5. ROUND ASSESSMENT & RECAP (2 Min)
   Stochastic engine computes net impact, execution friction, and surprise reality checks.
       │
       ├──► If more rounds remain: Advance to Next Round Infiltration
       └──► If final round complete: Advance to Adversary Final Gambit
                                                 │
                                                 ▼
                                     [ ADVERSARY FINAL GAMBIT ]
                                                 │
                                                 ▼
                                       [ GAME OVER: ASSESSMENT ]
```

---

## Scoring Engine: Formulas & Reality Check Friction

The net shift in Enterprise Health ($\Delta \text{HP}$) for each round is computed dynamically by `scoring_engine.py`:

$$\Delta \text{HP} = \text{Damage}_{\text{scaled}} + \text{Mitigation}_{\text{effective}} + \text{Disruption}_{\text{penalty}} + \text{Media}_{\text{delta}} + \text{Friction}$$

### 1. Attacker Damage & Severity Multiplier
$$\text{Damage}_{\text{raw}} = \text{Attack Damage Base} \times \text{GM Multiplier}$$
*(Base damage ranges from $-20$ to $-30$ HP depending on vector complexity).*

### 2. IT Defense Mitigation
* **Option 1 (Aggressive Lockdown)**: High mitigation range ($75\% - 95\%$), Disruption penalty $-4$ HP (24–36h downtime).
* **Option 2 (Targeted Quarantine)**: Moderate mitigation range ($45\% - 70\%$), Disruption penalty $-2$ HP (6–8h downtime).
* **Option 3 (Passive Monitoring)**: Low mitigation range ($15\% - 35\%$), Disruption penalty $0$ HP (Zero downtime).

### 3. The Executive Governance Triad & Override Penalties
* **✅ Agree with IT**: Authorizes $100\%$ of IT's proposed mitigation and absorbs the disruption penalty.
* **⚖️ Compromise**: Cuts operational downtime in half, but halves defensive mitigation ($50\% \times \text{Mitigation}$).
* **🚫 Override IT**: Prioritizes short-term revenue, reducing technical mitigation to **$0\%$** and triggering an **Executive Override Penalty** of $+10\%$ to $+35\%$ additional damage for dismissing technical advice.

### 4. The Inaction Backfire Penalty
If IT chooses a low-monitoring stance (Option 3), uncontained attacker activity triggers an **Inaction Backfire Penalty** ($+5\%$ to $+25\%$ additional damage).

> [!NOTE]
> Additive penalties ($\text{Override} + \text{Backfire}$) are safely capped at a maximum of $+45\%$ to preserve realistic game balance.

### 5. Media Resonance & Real-World Friction
* **Media Resonance**: PR headlines roll across a stochastic resonance range (Sensationalist: $-15$ to $-4$ HP; Favorable: $+1$ to $+12$ HP).
* **Execution Friction**: A stochastic roll of $\pm 3$ HP simulates the real-world operational friction inherent to live technical triage.

---

## The Adversary Final Gambit

At the conclusion of the simulation, the Threat Actors face a high-stakes "Press Your Luck" finale:

```
                                  ┌───────────────────────────┐
                                  │   ADVERSARY FINAL GAMBIT  │
                                  └─────────────┬─────────────┘
                                                │
                       ┌────────────────────────┴────────────────────────┐
                       ▼                                                 ▼
            [ OPTION 1: RETREAT ]                             [ OPTION 2: PRESS ATTACK ]
            • Clean escape into shadows                       • Attack secondary payment APIs
            • 0 Additional Damage                             • Risk vs. Reward calculation
            • 0 Asset Recovery                                • Catch probability based on past OPSEC:
                                                                - Low Exposure: 20% catch chance
                                                                - Elevated Exposure: 35% catch chance
                                                                - Extreme Exposure: 55% catch chance
                                                                                 │
                                                    ┌────────────────────────────┴────────────────────────────┐
                                                    ▼                                                         ▼
                                          [ CAUGHT BY FBI / SOC ]                                     [ UNDETECTED STRIKE ]
                                          • 0 Additional Damage                                       • -15 to -30 HP Catastrophic Damage
                                          • +3 to +15 HP Asset Recovery                               • Enterprise forced to brink
```

---

# ⚙️ Technical Architecture & Cloud Deployment

## Streamlit Community Cloud 1-Click Deployment

CloudStore Command is engineered to run seamlessly on **Streamlit Community Cloud** with zero external databases or infrastructure overhead.

### Step-by-Step Deployment Guide
1. **Fork or Clone this Repository** to your GitHub account:
   ```bash
   git clone https://github.com/<your-username>/Cyber-Attack-Simulation.git
   ```
2. **Sign in to Streamlit Community Cloud**:
   * Navigate to [share.streamlit.io](https://share.streamlit.io).
   * Connect your GitHub account.
3. **Deploy New Application**:
   * Click **New App**.
   * Select your repository and branch (`main`).
   * Set **Main file path** to: `app.py`.
   * (Optional) Specify a custom URL subdomain (e.g., `https://my-university-cyber-sim.streamlit.app`).
4. **Click Deploy**:
   * Streamlit automatically provisions Python and installs `requirements.txt`.
   * Your simulation is live in under 2 minutes.

---

## URL Parameter Routing & State Architecture

CloudStore Command uses URL query parameters (`?team=...`) to route users to role-specific dashboards while maintaining synchronized global state:

```
https://<your-app-domain>.streamlit.app/?team=<parameter>
```

| Parameter (`?team=`) | Interface Rendered | Access Gate | Key Capabilities |
| :--- | :--- | :--- | :--- |
| `?team=projector` | **Class Projector Display** | Open (Read-Only) | Uncluttered feed, no sidebar, auto-refresh telemetry, glossary. |
| `?team=main` | **GM Mission Control** | Passcode (`admin123`) | Start rounds, timer controls, threat multipliers, HP adjustments, undo. |
| `?team=hackers` | **Threat Actor Terminal** | Viewer Open / Captain (`hacker###`) | Attack dossiers, vector selection, straw polling, Final Gambit. |
| `?team=it` | **IT Defense Terminal** | Viewer Open / Captain (`tech###`) | SOC briefings, containment plans, RTO trade-offs, straw polling. |
| `?team=exec` | **Executive Boardroom** | Viewer Open / Captain (`board###`) | SEC/legal dossiers, IT proposal review, governance voting. |
| `?team=media` | **Media & PR Terminal** | Viewer Open / Captain (`press###`) | Press scrum, headline selection across 4 tiers, straw polling. |
| `?team=instructor` | **Solo Instructor Sandbox** | Passcode (`tryit123`) | Isolated rehearsal mode walking sequentially through all roles. |

### Global In-Memory State Synchronization
* **Shared Singleton State**: Instantiated via `@st.cache_resource def get_global_game() -> GameState`. All student browser tabs and projector screens connect to this single shared memory structure.
* **Live Telemetry Fragments**: The dashboard leverages Streamlit fragments (`@st.fragment(run_every=2)`) to auto-sync health telemetry, active timers, and live poll results every 2 seconds without full-page reloads.
* **Zero Database Overhead**: Session state is purely in-memory. Resetting the simulation via the GM console completely clears active runs with zero database migrations or residual locks.

---

## Repository Directory Structure

```text
cyberattacksim/
├── app.py                         # Application entry point, URL routing, GM & Projector dashboards
├── state_manager.py               # Global synchronized GameState, snapshot undo, and straw polling engine
├── game_data.py                   # Attack definitions, IT containment choices, governance options, and timers
├── scoring_engine.py              # Mathematical outcome engine, reality check friction, and distribution curves
├── team_views.py                  # Terminals for Threat Actors, IT, Executives, and Media with Captain/Viewer modes
├── ui_components.py               # Threatening countdown clock, health gauges, round recap cards, and glossary
├── requirements.txt               # Lightweight dependencies (streamlit>=1.35.0)
│
├── content/                       # Modular Markdown Educational Briefings
│   ├── hackers/                   # Adversary mechanics, OSINT, and attack execution guides
│   ├── it/                        # SOC briefings, technical trade-offs, and RTO downtime metrics
│   └── exec/                      # SEC Form 8-K disclosures, GDPR compliance, and governance mandates
│
└── tests/                         # Comprehensive Automated Test Suites
    ├── simulate_full_multiplayer.py  # End-to-end multi-agent simulation test
    ├── test_instructor_mode.py       # Single-player sandbox authentication and flow test
    ├── test_distribution.py          # Monte Carlo distribution calibration test (10/60/30)
    ├── test_exec_governance_*.py     # Executive pushback pressure and override penalty tests
    └── test_accessibility.py         # WCAG contrast, tablet viewports, and touch target tests
```

---

## Customizing Scenarios via Markdown Files

Instructors can customize scenario narratives, company names, technical terminology, and regulatory requirements **without modifying a single line of Python code**.

All briefing dossiers live inside the `content/` folder as standard Markdown files:
* **Edit `content/hackers/<attack>.md`**: Change attack vectors, reconnaissance descriptions, or MITRE ATT&CK references.
* **Edit `content/it/<attack>.md`**: Customize technical recovery actions, system architectures, or recovery time objectives (RTO).
* **Edit `content/exec/<attack>.md`**: Adjust SEC reporting requirements, industry compliance standards (e.g., HIPAA, PCI-DSS, FERPA), or financial stakes.

---

## Automated Test Suite & Verification

The codebase includes an extensive suite of automated tests using Streamlit's native `AppTest` framework to ensure simulation stability, balanced scoring curves, and accessibility compliance.

To run the full end-to-end multi-agent simulation test:
```bash
python simulate_full_multiplayer.py
```

To run the single-player instructor sandbox verification:
```bash
python test_instructor_mode.py
```

To verify the Monte Carlo outcome distribution (calibrated to ~10% Win, ~60% Survive, ~30% Bankrupt):
```bash
python test_distribution.py
```

---

## 📜 License

This project is licensed under the **MIT License**. It is freely available for educators, universities, and commercial organizations conducting cybersecurity awareness training and tabletop exercises.
