"""
test_deep_media_gm_eval.py
Comprehensive end-to-end evaluation test suite for Media Scrum, Game Master Console,
Projector View, and Single-Player Instructor Sandbox on development branch.
"""

import sys
from pathlib import Path

_repo = str(Path(__file__).resolve().parent.parent)
if _repo not in sys.path:
    sys.path.insert(0, _repo)

APP_PY = str(Path(_repo) / "app.py")

from streamlit.testing.v1 import AppTest
from game_data import TEAM_CODES, DYNAMIC_HEADLINES, ATTACKS, IT_CHOICES
from scoring_engine import get_outcome_thresholds, evaluate_final_outcome

def run_deep_evaluation():
    print("=====================================================================")
    print("🔍 DEEP EVALUATION: MEDIA SCRUM, GM CONSOLE, PROJECTOR, INSTRUCTOR")
    print("=====================================================================")

    # -------------------------------------------------------------
    # SUITE 1: Media Scrum Terminal Exhaustive Evaluation
    # -------------------------------------------------------------
    print("\n--- [SUITE 1] Media Scrum Terminal Deep Evaluation ---")

    # Step 1.1: Verify phase-based standby messaging using GM flow
    gm = AppTest.from_file(APP_PY)
    gm.query_params["team"] = "main"
    gm.run()
    gm.sidebar.text_input[0].input("admin123")
    gm.sidebar.button[0].click().run()

    # Reset Sim to Lobby
    reset_btn = next(b for b in gm.sidebar.button if "Reset Sim" in b.label)
    reset_btn.click().run()

    # In Lobby: Check Media view
    m_lobby = AppTest.from_file(APP_PY)
    m_lobby.query_params["team"] = "media"
    m_lobby.run()
    assert any("Monitoring live news wires" in i.value for i in m_lobby.info), "Lobby should show monitoring wire"
    print("  ✓ Media standby: Lobby phase wire monitoring verified.")

    # GM starts Round 1 -> Hacker phase
    start_r1 = next(b for b in gm.sidebar.button if "Start Round 1" in b.label)
    start_r1.click().run()

    m_hacker = AppTest.from_file(APP_PY)
    m_hacker.query_params["team"] = "media"
    m_hacker.run()
    assert any("Monitoring live news wires" in i.value for i in m_hacker.info), "Hacker phase should show monitoring wire"
    print("  ✓ Media standby: Hacker phase wire monitoring verified.")

    # Hacker deploys Vector A -> IT phase
    h = AppTest.from_file(APP_PY)
    h.query_params["team"] = "hackers"
    h.run()
    h.sidebar.text_input[0].input("hacker123")
    h.sidebar.button[0].click().run()
    dep_a = next(b for b in h.button if "Deploy Vector A" in b.label)
    dep_a.click().run()

    m_it = AppTest.from_file(APP_PY)
    m_it.query_params["team"] = "media"
    m_it.run()
    assert any("Monitoring live news wires" in i.value for i in m_it.info), "IT phase should show monitoring wire"
    print("  ✓ Media standby: IT phase wire monitoring verified.")

    # IT deploys Option 1 -> Exec phase
    it = AppTest.from_file(APP_PY)
    it.query_params["team"] = "it"
    it.run()
    it.sidebar.text_input[0].input("tech123")
    it.sidebar.button[0].click().run()
    dep_it = next(b for b in it.button if "Deploy & Recommend Option 1" in b.label)
    dep_it.click().run()

    m_exec = AppTest.from_file(APP_PY)
    m_exec.query_params["team"] = "media"
    m_exec.run()
    assert any("Executive Board is currently voting" in w.value for w in m_exec.warning), "Exec phase should show voting alert"
    print("  ✓ Media standby: Exec phase closed-door voting alert verified.")

    # Exec authorizes Directive (Compromise / Downgrade) -> Media phase
    ex = AppTest.from_file(APP_PY)
    ex.query_params["team"] = "exec"
    ex.run()
    ex.sidebar.text_input[0].input("board123")
    ex.sidebar.button[0].click().run()
    auth_down = next(b for b in ex.button if getattr(b, "key", "") == "btn_exec_downgrade" or any(w in b.label for w in ["Compromise", "Downgrade"]))
    auth_down.click().run()

    # Step 1.2: Media Captain Authentication & Wire Briefing
    m_capt = AppTest.from_file(APP_PY)
    m_capt.query_params["team"] = "media"
    m_capt.run()
    # Unlocked view shows breaking wire and headline choices
    m_capt.sidebar.text_input[0].input("press123")
    m_capt.sidebar.button[0].click().run()

    capt_markdown = " ".join(m.value for m in m_capt.markdown)
    assert "BREAKING INTELLIGENCE WIRE" in capt_markdown
    assert "Spear Phishing" in capt_markdown
    assert "DOWNGRADE" in capt_markdown
    print("  ✓ Breaking Intelligence Wire verified: active breach (Spear Phishing) and Executive directive (DOWNGRADE).")

    # Step 1.3: Verify all 4 Headline Tiers & Virality in Captain View
    assert "Headline 1" in capt_markdown and "Sensationalist" in capt_markdown and "Negative Tone" in capt_markdown
    assert "Headline 2" in capt_markdown and "Critical" in capt_markdown and "Negative Tone" in capt_markdown
    assert "Headline 3" in capt_markdown and "Balanced" in capt_markdown and "Neutral Tone" in capt_markdown
    assert "Headline 4" in capt_markdown and "Favorable" in capt_markdown and "Positive Tone" in capt_markdown
    assert "Virality: Unpredictable" in capt_markdown
    print("  ✓ All 4 headline tiers (Sensationalist, Critical, Balanced, Favorable) with tones and virality indicators verified.")

    # Step 1.4: Media Straw Polling & Permission Separation
    m_view1 = AppTest.from_file(APP_PY)
    m_view1.query_params["team"] = "media"
    m_view1.session_state["voter_id"] = "viewer_press_deep_1"
    m_view1.run()

    m_view2 = AppTest.from_file(APP_PY)
    m_view2.query_params["team"] = "media"
    m_view2.session_state["voter_id"] = "viewer_press_deep_2"
    m_view2.run()

    # Viewers cannot launch straw polls or publish
    assert not any("Launch Straw Poll" in b.label for b in m_view1.button)
    assert not any("Publish Headline" in b.label for b in m_view1.button)

    # Captain launches straw poll
    launch_btn = next(b for b in m_capt.button if "Launch Straw Poll" in b.label)
    launch_btn.click().run()

    # Viewer 1 votes Headline 1 (Sensationalist)
    m_view1.run()
    vote_btn1 = next(b for b in m_view1.button if "Vote: Headline 1" in b.label)
    vote_btn1.click().run()

    # Viewer 2 votes Headline 4 (Favorable)
    m_view2.run()
    vote_btn4 = next(b for b in m_view2.button if "Vote: Headline 4" in b.label)
    vote_btn4.click().run()

    # Captain sees 2 votes (50% / 50%)
    m_capt.run()
    capt_text = " ".join(m.value for m in m_capt.markdown)
    assert "2 total votes" in capt_text
    assert "50.0%" in capt_text

    # Captain publishes Headline 4
    pub_h4 = next(b for b in m_capt.button if "Publish Headline 4" in b.label)
    pub_h4.click().run()

    assert any("Breaking story published" in s.value for s in m_capt.success)
    print("  ✓ Media straw polling, vote tallies, viewer voting, and Captain publishing with 'press123' verified.")

    # -------------------------------------------------------------
    # SUITE 2: Game Master Console & Enterprise Health HP Bar
    # -------------------------------------------------------------
    print("\n--- [SUITE 2] Game Master Console & Enterprise Health HP Bar ---")

    # Step 2.1: Enterprise Health HP Bar thresholds
    b2, w2 = get_outcome_thresholds(2)
    assert (b2, w2) == (32, 71)
    b3, w3 = get_outcome_thresholds(3)
    assert (b3, w3) == (17, 54)

    gm.run()
    gm_text = " ".join(m.value for m in gm.markdown)
    assert "Unified Enterprise Health" in gm_text
    assert f"Bankrupt (&lt; {b2})" in gm_text
    assert f"Survive ({b2} - {w2 - 1})" in gm_text
    assert f"Win (&ge; {w2})" in gm_text
    print("  ✓ Unified Enterprise Health HP bar with calibrated thresholds (0–100 HP, bankruptcy, survive, win) verified.")

    # Step 2.2: Manual HP Adjustments (+10 HP / -10 HP) protected behind admin passcode
    # In unauthenticated GM view
    unauth_gm = AppTest.from_file(APP_PY)
    unauth_gm.query_params["team"] = "main"
    unauth_gm.run()
    assert not any("Add +10 HP" in b.label for b in unauth_gm.button)
    assert not any("Subtract -10 HP" in b.label for b in unauth_gm.button)

    # In authenticated GM view
    add_hp_btn = next(b for b in gm.button if "Add +10 HP" in b.label)
    sub_hp_btn = next(b for b in gm.button if "Subtract -10 HP" in b.label)
    assert add_hp_btn is not None and sub_hp_btn is not None
    print("  ✓ Manual HP adjustments (+10 HP / -10 HP) protected behind admin passcode verified.")

    # Step 2.3: Verify Captain console does NOT have advance buttons
    for role in ["hackers", "it", "exec", "media"]:
        t_app = AppTest.from_file(APP_PY)
        t_app.query_params["team"] = role
        t_app.run()
        t_app.sidebar.text_input[0].input(TEAM_CODES[role])
        t_app.sidebar.button[0].click().run()
        # Verify in current recap phase
        advance_btns = [b for b in t_app.button if any(k in b.label for k in ["Advance", "Start Round 2", "Next Round", "Force Advance"])]
        assert len(advance_btns) == 0, f"Role {role} Captain has unauthorized advance button: {[b.label for b in advance_btns]}"
    print("  ✓ Advance simulation restricted STRICTLY to Game Master (Captains have ZERO advance buttons).")

    # -------------------------------------------------------------
    # SUITE 3: Round Recap Card Itemization & Penalty Badges
    # -------------------------------------------------------------
    print("\n--- [SUITE 3] Round Recap Card Itemization ---")
    # Verify the recap card rendered in the Media Terminal
    m_capt.run()
    recap_text = " ".join(m.value for m in m_capt.markdown)
    assert "ROUND 1 INCIDENT DEBRIEF" in recap_text
    assert "IT Defense Mitigated:" in recap_text
    assert "Operational Disruption:" in recap_text
    assert "Breaking Headline:" in recap_text
    assert "Enterprise Health:" in recap_text
    print("  ✓ Round recap card verified: Net health delta, IT defense mitigated %, operational disruption, headline impact.")

    # Test penalty badges specifically with a dedicated scenario
    print("  ... Testing Inaction and Exec Override penalty badges scenario ...")
    reset_btn = next(b for b in gm.sidebar.button if "Reset Sim" in b.label)
    reset_btn.click().run()

    # R1: Hacker A (-20)
    start_r1 = next(b for b in gm.sidebar.button if "Start Round 1" in b.label)
    start_r1.click().run()

    h.run()
    dep_a = next(b for b in h.button if "Deploy Vector A" in b.label)
    dep_a.click().run()

    # IT: Option 3 (Passive Monitoring -> triggers Inaction Backfire)
    it.run()
    dep_it3 = next(b for b in it.button if "Deploy & Recommend Option 3" in b.label)
    dep_it3.click().run()

    # Exec: Overrule (triggers Exec Override Penalty)
    ex.run()
    auth_over = next(b for b in ex.button if getattr(b, "key", "") == "btn_exec_overrule" or "Overrule" in b.label)
    auth_over.click().run()

    # Media: Publish Headline 1
    m_capt.run()
    pub_h1 = next(b for b in m_capt.button if "Publish Headline 1" in b.label)
    pub_h1.click().run()

    # Verify penalty badges in recap card
    m_capt.run()
    recap_with_penalties = " ".join(m.value for m in m_capt.markdown)
    assert "Inaction Backfire" in recap_with_penalties, "Inaction Backfire badge missing in recap card"
    assert "Exec Override Penalty" in recap_with_penalties, "Exec Override Penalty badge missing in recap card"
    print("  ✓ Penalty badges verified: '+X% Inaction Backfire' and '+X% Exec Override Penalty' rendered dynamically.")

    # -------------------------------------------------------------
    # SUITE 4: Class Projector View (?team=projector)
    # -------------------------------------------------------------
    print("\n--- [SUITE 4] Dedicated Class Projector View (?team=projector) ---")
    proj = AppTest.from_file(APP_PY)
    proj.query_params["team"] = "projector"
    proj.run()

    # Clean layout: zero buttons
    assert len(proj.button) == 0, f"Projector must have zero interactive buttons, found: {[b.label for b in proj.button]}"
    assert len(proj.sidebar.button) == 0, f"Projector sidebar must have zero buttons"
    assert len(proj.sidebar.text_input) == 0, f"Projector sidebar must have zero inputs"

    proj_text = " ".join(m.value for m in proj.markdown)
    assert "Live Telemetry Auto-Sync" in proj_text
    assert "Unified Enterprise Health" in proj_text
    assert "Live Team Deliberation Telemetry" in proj_text
    print("  ✓ Class Projector view verified: completely clean, zero interactive buttons, Auto-Sync badge active.")

    # -------------------------------------------------------------
    # SUITE 5: Single-Player Instructor Sandbox (?team=instructor)
    # -------------------------------------------------------------
    print("\n--- [SUITE 5] Single-Player Instructor Sandbox (?team=instructor) ---")
    inst = AppTest.from_file(APP_PY)
    inst.query_params["team"] = "instructor"
    inst.run()

    # Passcode gate
    inst.sidebar.text_input[0].input("tryit123")
    inst.sidebar.button[0].click().run()
    assert any("CAPTAIN ACCESS UNLOCKED" in s.value for s in inst.sidebar.success)

    # State isolation check
    solo_g = inst.session_state["instructor_game"]
    assert solo_g.phase == "lobby"

    # Sequential walk across all 4 roles:
    # 1. Start Round 1 (GM Mission Controls)
    start_btn = next(b for b in inst.button if "Start Round 1" in b.label)
    start_btn.click().run()
    assert solo_g.phase == "hacker"

    # 2. Threat Actor Captain deploys
    dep_btn = next(b for b in inst.button if "Deploy Vector" in b.label)
    dep_btn.click().run()
    assert solo_g.phase == "it"

    # 3. IT Defense Captain deploys
    dep_it = next(b for b in inst.button if "Deploy & Recommend Option" in b.label)
    dep_it.click().run()
    assert solo_g.phase == "exec"

    # 4. Executive Captain authorizes
    auth_ex = next(b for b in inst.button if "Authorize Directive" in b.label)
    auth_ex.click().run()
    assert solo_g.phase == "media"

    # 5. Media Captain publishes
    pub_med = next(b for b in inst.button if "Publish Headline" in b.label)
    pub_med.click().run()
    assert solo_g.phase == "recap"

    # In Recap: Verify Captain area has NO advance button, advance is ONLY in GM Mission Controls
    capt_adv = [b for b in inst.button if b.key and "main_btn" not in b.key and any(k in b.label for k in ["Start Round 2", "Advance"])]
    assert len(capt_adv) == 0, f"Instructor Captain view should NOT have advance buttons: {capt_adv}"

    # Advance to Round 2 via GM controls
    gm_adv = next(b for b in inst.button if getattr(b, "key", "") == "main_btn_adv_r" or "Start Round 2" in b.label)
    gm_adv.click().run()
    assert solo_g.phase == "hacker"
    assert solo_g.current_round == 2
    print("  ✓ Single-Player Instructor Sandbox verified: Passcode gated ('tryit123'), isolated state, sequential 4-role progression.")

    print("\n=====================================================================")
    print("🎉 ALL 5 SPECIALIST EVALUATION SUITES PASSED WITH 100% SUCCESS!")
    print("=====================================================================")

if __name__ == "__main__":
    run_deep_evaluation()
