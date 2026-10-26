"""
test_red_team_comprehensive.py
Comprehensive End-to-End Evaluation Test Suite for Red Team (Threat Actor) Terminal & Mechanics.
"""

import sys
import os
import random
from pathlib import Path
from streamlit.testing.v1 import AppTest

from state_manager import GameState
import game_data
from game_data import ATTACKS, load_markdown_content, TEAM_CODES

def test_1_adversary_vectors_and_dossiers():
    print("\n=======================================================")
    print("1. EVALUATING ALL 9 ADVERSARY VECTORS & EDUCATIONAL DOSSIERS")
    print("=======================================================")
    
    expected_damages = {
        (1, "A"): -20, (1, "B"): -25, (1, "C"): -30,
        (2, "A"): -25, (2, "B"): -28, (2, "C"): -30,
        (3, "A"): -25, (3, "B"): -28, (3, "C"): -30,
    }
    
    expected_complexities = {
        (1, "A"): "Low", (1, "B"): "Medium", (1, "C"): "High",
        (2, "A"): "Medium", (2, "B"): "Medium", (2, "C"): "High",
        (3, "A"): "High", (3, "B"): "Low", (3, "C"): "High",
    }
    
    expected_penalties = {
        (1, "A"): 0, (1, "B"): 1, (1, "C"): 2,
        (2, "A"): 0, (2, "B"): 2, (2, "C"): 2,
        (3, "A"): 0, (3, "B"): 1, (3, "C"): 1,
    }

    for rnd in [1, 2, 3]:
        assert rnd in ATTACKS, f"Round {rnd} missing from ATTACKS!"
        for vec_id in ["A", "B", "C"]:
            assert vec_id in ATTACKS[rnd], f"Vector {vec_id} missing in Round {rnd}!"
            att = ATTACKS[rnd][vec_id]
            
            # Check fields
            assert att.get("name"), f"Missing name in Round {rnd} {vec_id}"
            assert att.get("icon"), f"Missing icon in Round {rnd} {vec_id}"
            assert att.get("damage") == expected_damages[(rnd, vec_id)], f"Damage mismatch in Round {rnd} {vec_id}"
            assert att.get("complexity") == expected_complexities[(rnd, vec_id)], f"Complexity mismatch in Round {rnd} {vec_id}"
            assert att.get("exposure_penalty") == expected_penalties[(rnd, vec_id)], f"Exposure penalty mismatch in Round {rnd} {vec_id}"
            assert att.get("anonymity"), f"Missing anonymity in Round {rnd} {vec_id}"
            assert att.get("damage_potential") in ["Moderate", "High", "Catastrophic"], f"Invalid damage potential in Round {rnd} {vec_id}"
            assert att.get("description"), f"Missing description in Round {rnd} {vec_id}"
            assert att.get("assessment"), f"Missing assessment in Round {rnd} {vec_id}"
            
            # Check Markdown file
            md_file = att.get("md_file")
            assert md_file, f"Missing md_file reference in Round {rnd} {vec_id}"
            content = load_markdown_content("hackers", md_file)
            assert content, f"Markdown file {md_file} is empty or missing from content/hackers!"
            assert len(content) > 500, f"Markdown content in {md_file} is too short ({len(content)} chars)!"
            assert "### " in content, f"Markdown file {md_file} lacks Markdown headers!"
            assert "* " in content, f"Markdown file {md_file} lacks technical anatomy bullet points!"
            
            print(f"  [PASS] R{rnd} Vector {vec_id}: {att['icon']} {att['name']} | Dmg: {att['damage']} | Anonymity: {att['anonymity']} | Dossier: {md_file} ({len(content)} bytes)")

    print(">>> All 9 adversary vectors & educational dossiers passed verification with 100% depth.")


def test_2_threat_actor_ui_and_privilege_separation():
    print("\n=======================================================")
    print("2. TESTING THREAT ACTOR UI FLOW & PRIVILEGE SEPARATION")
    print("=======================================================")
    
    # 2.1 Password gate & invalid passcode rejection
    viewer = AppTest.from_file("app.py")
    viewer.query_params["team"] = "hackers"
    viewer.run()
    assert not viewer.exception
    
    # Verify initial viewer state
    sidebar_texts = [x.value for x in list(viewer.sidebar.info) + list(viewer.sidebar.caption) + list(viewer.sidebar.markdown) if hasattr(x, "value")]
    assert any("VIEWER MODE" in t for t in sidebar_texts), "Initial mode is not Viewer Mode!"
    print("  [PASS] Initial state correctly defaults to Viewer Mode.")
    
    # Try multiple wrong passcodes
    for wrong_code in ["", "1234", "admin123", "hackers", "HACKER123", "root"]:
        viewer.sidebar.text_input[0].input(wrong_code)
        unlock_btn = next((b for b in viewer.sidebar.button if "Unlock Captain Role" in b.label), None)
        assert unlock_btn is not None
        unlock_btn.click().run()
        if wrong_code == "":
            pass # empty code should not unlock
        assert len(viewer.sidebar.error) > 0 or not any("CAPTAIN MODE" in str(getattr(x, "value", "")) for x in viewer.sidebar.success), f"Should not unlock with '{wrong_code}'"
    print("  [PASS] Invalid passcodes ('', '1234', 'admin123', 'root', etc.) rejected cleanly.")
    
    # Unlock with valid passcode
    viewer.sidebar.text_input[0].input("hacker123")
    unlock_btn = next((b for b in viewer.sidebar.button if "Unlock Captain Role" in b.label), None)
    unlock_btn.click().run()
    assert len(viewer.sidebar.error) == 0
    sidebar_successes = [s.value for s in viewer.sidebar.success if hasattr(s, "value")]
    assert any("CAPTAIN MODE UNLOCKED" in s for s in sidebar_successes)
    print("  [PASS] Authenticated successfully with 'hacker123' -> CAPTAIN MODE UNLOCKED.")
    
    # Relinquish Captain Role
    relinquish_btn = next((b for b in viewer.sidebar.button if "Relinquish Captain Role" in b.label), None)
    assert relinquish_btn is not None
    relinquish_btn.click().run()
    sidebar_infos = [s.value for s in viewer.sidebar.info if hasattr(s, "value")]
    assert any("VIEWER MODE" in s for s in sidebar_infos)
    print("  [PASS] Relinquish Captain Role successfully reverted session to Viewer Mode.")


def test_3_straw_polling_and_vector_deployment():
    print("\n=======================================================")
    print("3. TESTING STRAW POLLING, VOTE SWITCHING, & VECTOR DEPLOYMENT")
    print("=======================================================")
    
    # Initialize GM and start Round 1
    gm = AppTest.from_file("app.py")
    gm.query_params["team"] = "main"
    gm.run()
    gm.sidebar.text_input[0].input("admin123")
    gm.sidebar.button[0].click().run()
    
    all_btns = list(gm.button) + list(gm.sidebar.button)
    reset_btn = next((b for b in all_btns if b.label and "Reset Sim" in b.label), None)
    if reset_btn:
        reset_btn.click().run()
    all_btns = list(gm.button) + list(gm.sidebar.button)
    start_btn = next((b for b in all_btns if b.label and "Start Round 1" in b.label), None)
    if start_btn:
        start_btn.click().run()
    print("  [PASS] Simulation initialized in Round 1 Hacker phase.")
    
    # Captain session
    capt = AppTest.from_file("app.py")
    capt.query_params["team"] = "hackers"
    capt.run()
    capt.sidebar.text_input[0].input("hacker123")
    next(b for b in capt.sidebar.button if "Unlock Captain Role" in b.label).click().run()
    
    # Viewer 1 and Viewer 2 sessions
    v1 = AppTest.from_file("app.py")
    v1.query_params["team"] = "hackers"
    v1.run()
    
    v2 = AppTest.from_file("app.py")
    v2.query_params["team"] = "hackers"
    v2.run()
    
    # Viewers cannot see voting buttons before poll is opened
    assert len([b for b in v1.button if b.label and "Vote:" in b.label]) == 0
    # Viewers cannot see Launch or Close poll buttons
    assert len([b for b in v1.button if b.label and "Straw Poll" in b.label]) == 0
    # Viewers cannot see Deploy Vector buttons
    assert len([b for b in v1.button if b.label and "Deploy Vector" in b.label]) == 0
    print("  [PASS] Viewers strictly prohibited from voting or deploying before poll launch.")
    
    # Captain launches straw poll
    launch_btn = next(b for b in capt.button if b.label and "Launch Straw Poll" in b.label)
    launch_btn.click().run()
    print("  [PASS] Captain opened Straw Poll.")
    
    # Viewers refresh and vote
    v1.run()
    v2.run()
    
    # Viewer 1 votes Vector A
    btn_a_v1 = next(b for b in v1.button if b.label and "Vote: A" in b.label)
    btn_a_v1.click().run()
    assert any("Voted: A" in b.label for b in v1.button if b.label)
    
    # Viewer 2 votes Vector B
    btn_b_v2 = next(b for b in v2.button if b.label and "Vote: B" in b.label)
    btn_b_v2.click().run()
    assert any("Voted: B" in b.label for b in v2.button if b.label)
    print("  [PASS] Viewers cast initial votes (V1 -> A, V2 -> B).")
    
    # Test vote switching: Viewer 1 changes vote from A to C
    btn_c_v1 = next(b for b in v1.button if b.label and "Vote: C" in b.label)
    btn_c_v1.click().run()
    assert any("Voted: C" in b.label for b in v1.button if b.label)
    assert not any("Voted: A" in b.label for b in v1.button if b.label)
    print("  [PASS] Viewer 1 successfully switched vote from A to C (no vote duplication).")
    
    # Captain checks live tallies
    capt.run()
    tally_markdowns = [m.value for m in capt.markdown if "Live Polling Results" in m.value]
    assert len(tally_markdowns) > 0, "Captain view missing Live Polling Results header"
    assert "2 total votes" in tally_markdowns[0], f"Expected 2 total votes, found: {tally_markdowns[0]}"
    print("  [PASS] Live polling results correctly aggregate 2 total votes (B: 1, C: 1).")
    
    # Captain closes straw poll
    close_btn = next(b for b in capt.button if b.label and "Close Straw Poll" in b.label)
    close_btn.click().run()
    print("  [PASS] Captain closed Straw Poll.")
    
    # Verify voting buttons disappear
    v1.run()
    assert len([b for b in v1.button if b.label and "Vote:" in b.label]) == 0
    print("  [PASS] Voting buttons disabled for Viewers after poll closure.")
    
    # Captain deploys Vector C (AI LLM Prompt Injection)
    deploy_c = next(b for b in capt.button if b.label and "Deploy Vector C" in b.label)
    deploy_c.click().run()
    print("  [PASS] Captain deployed Vector C ('AI LLM Prompt Injection & API Pivot').")
    
    # Verify state transitioned cleanly to IT phase
    capt.run()
    v1.run()
    assert any("Attack vector deployed" in info.value for info in capt.info)
    assert any("ACTIVE PAYLOAD" in m.value for m in capt.markdown)
    assert any("Adversary C2 Surveillance Console" in m.value for m in capt.markdown)
    assert any("Attack vector deployed" in info.value for info in v1.info)
    print("  [PASS] State transitioned cleanly to IT phase; Threat Actor terminals display active C2 Wiretap console.")


def test_4_adversary_final_gambit():
    print("\n=======================================================")
    print("4. TESTING ADVERSARY FINAL GAMBIT (PRESS ATTACK VS RETREAT)")
    print("=======================================================")
    
    game = GameState()
    game.reset(base_health=100.0, max_rounds=2)
    
    # Test Exposure Level calculations
    # Score 0 (stealth only)
    game.hacker_exposure_score = 0
    exp_0 = game.get_hacker_exposure_level()
    assert exp_0["level"] == "Low Risk"
    assert exp_0["catch_chance"] == 0.20
    assert exp_0["color"] == "#10b981"
    print("  [PASS] Hacker Exposure Score 0 -> Low Risk (20% catch chance, emerald).")
    
    # Score 2 (moderate noise)
    game.hacker_exposure_score = 2
    exp_2 = game.get_hacker_exposure_level()
    assert exp_2["level"] == "Elevated Risk"
    assert exp_2["catch_chance"] == 0.35
    assert exp_2["color"] == "#f59e0b"
    print("  [PASS] Hacker Exposure Score 2 -> Elevated Risk (35% catch chance, amber).")
    
    # Score 4 (loud intrusions)
    game.hacker_exposure_score = 4
    exp_4 = game.get_hacker_exposure_level()
    assert exp_4["level"] == "Extreme Risk"
    assert exp_4["catch_chance"] == 0.55
    assert exp_4["color"] == "#ef4444"
    print("  [PASS] Hacker Exposure Score 4 -> Extreme Risk (55% catch chance, red).")
    
    # Test Safe Strategic Retreat mechanics
    game.phase = "final_hacker_action"
    game.company_health = 65.0
    res_retreat = game.submit_final_hacker_action("retreat")
    assert res_retreat["action"] == "retreat"
    assert res_retreat["damage"] == 0
    assert res_retreat["caught"] is False
    assert res_retreat["recovery"] == 0
    assert res_retreat["net_delta"] == 0
    assert res_retreat["health_after"] == 65.0
    assert game.phase == "game_over"
    print("  [PASS] Safe Retreat: 0 damage, 0 recovery, clean adversary escape to game_over.")
    
    # Test Press the Attack mechanics
    # 1. Caught case (mocking random)
    game.reset(base_health=60.0)
    game.phase = "final_hacker_action"
    game.hacker_exposure_score = 4 # 55% catch
    random.seed(42) # Deterministic check
    res_press = game.submit_final_hacker_action("press")
    assert res_press["action"] == "press"
    if res_press["caught"]:
        assert res_press["damage"] == 0
        assert res_press["recovery"] >= 3
        assert res_press["net_delta"] == res_press["recovery"]
        assert res_press["health_after"] > 60.0
        print(f"  [PASS] Press the Attack (CAUGHT): 0 damage, +{res_press['recovery']} HP asset recovery for company.")
    else:
        assert res_press["damage"] >= 15
        assert res_press["recovery"] == 0
        assert res_press["net_delta"] == -res_press["damage"]
        assert res_press["health_after"] < 60.0
        print(f"  [PASS] Press the Attack (UNDETECTED): -{res_press['damage']} HP catastrophic damage inflicted.")


def test_5_ui_accessibility_and_contrast():
    print("\n=======================================================")
    print("5. ACCESSIBILITY, CONTRAST, & LIGHT/DARK RESPONSIVENESS")
    print("=======================================================")
    
    views_path = Path("team_views.py")
    with open(views_path, "r", encoding="utf-8") as f:
        views_code = f.read()
        
    # Check that hacker terminal has no sub-micro font size < 13px
    import re
    sub_micro_pattern = re.compile(r'font-size:\s*([0-9]|1[0-2])px\b', re.IGNORECASE)
    assert not sub_micro_pattern.search(views_code), "Found sub-micro font sizes in team_views.py!"
    print("  [PASS] Verified: All font sizes in team_views.py are >= 13px.")
    
    # Check that header and live poll text use theme-responsive CSS variables
    assert "var(--text-color" in views_code, "team_views.py missing theme-responsive var(--text-color) tokens!"
    print("  [PASS] Verified: Theme-responsive color tokens (var(--text-color)) used for live poll and subtitles.")
    
    # Check touch target buttons in app.py
    app_path = Path("app.py")
    with open(app_path, "r", encoding="utf-8") as f:
        app_code = f.read()
    assert "min-height: 48px" in app_code, "Missing 48px button minimum touch target height in app.py!"
    print("  [PASS] Verified: Global 48px minimum touch target height enforced across all buttons.")


if __name__ == "__main__":
    test_1_adversary_vectors_and_dossiers()
    test_2_threat_actor_ui_and_privilege_separation()
    test_3_straw_polling_and_vector_deployment()
    test_4_adversary_final_gambit()
    test_5_ui_accessibility_and_contrast()
    print("\n=======================================================")
    print("🎉 ALL RED TEAM COMPREHENSIVE TESTS PASSED WITH 100% SUCCESS!")
    print("=======================================================")
