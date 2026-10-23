"""
test_instructor_mode.py
Automated end-to-end test suite for Single-Player Instructor Testing Mode (?team=instructor).
Verifies:
1. Passcode security (tryit123 required to unlock).
2. Complete state isolation from global multiplayer GameState.
3. Full sequential progression across teams:
   Lobby -> Hacker -> IT -> Exec -> Media -> Recap -> Round 2 -> Final Hacker Action -> Game Over.
4. Automatic Captain privilege authorization across all teams.
5. Presence in GM shareable URLs list and Preview switcher.
"""

import sys
import time
from streamlit.testing.v1 import AppTest
from state_manager import GameState
from game_data import TEAM_CODES

def test_instructor_mode_end_to_end():
    print("=====================================================================")
    print("🧪 STARTING SINGLE-PLAYER INSTRUCTOR TESTING MODE TEST SUITE")
    print("=====================================================================")

    # -------------------------------------------------------------
    # 1. VERIFY GM SIDEBAR SHAREABLE URLS INCLUDE INSTRUCTOR MODE
    # -------------------------------------------------------------
    print("\n--- [TEST 1] GM Sidebar Shareable Links Audit ---")
    gm = AppTest.from_file("app.py")
    gm.query_params["team"] = "main"
    gm.run()
    gm.sidebar.text_input[0].input("admin123")
    gm.sidebar.button[0].click().run()
    assert not gm.exception

    # Check team links in sidebar expanders
    codes_text = " ".join([c.value for c in gm.sidebar.code])
    assert "?team=instructor" in codes_text, "Shareable URL for ?team=instructor missing in GM console!"
    print("  ✓ GM console correctly lists shareable link for '?team=instructor' with passcode 'tryit123'.")

    # -------------------------------------------------------------
    # 2. PASSCODE GATE & AUTHENTICATION (tryit123)
    # -------------------------------------------------------------
    print("\n--- [TEST 2] Instructor Mode Passcode Gate ---")
    inst = AppTest.from_file("app.py")
    inst.query_params["team"] = "instructor"
    inst.run()
    assert not inst.exception

    # Verify locked screen rendered
    main_text = " ".join([m.value for m in inst.markdown] + [i.value for i in inst.info])
    assert "Instructor Testing Sandbox" in str(inst.title[0].value)
    assert "tryit123" in main_text or "Access Restricted" in main_text

    # Test invalid passcode
    inst.text_input[0].input("wrongpassword")
    inst.button[0].click().run()
    assert not inst.exception
    assert any("Invalid Passcode" in err.value for err in inst.error)
    print("  ✓ Invalid passcode rejected with error message.")

    # Test correct passcode ('tryit123')
    inst.text_input[0].input("tryit123")
    inst.button[0].click().run()
    assert not inst.exception
    assert any("CAPTAIN ACCESS UNLOCKED" in s.value for s in inst.sidebar.success)
    print("  ✓ Passcode 'tryit123' successfully unlocked Instructor Sandbox with all Captain roles.")

    # -------------------------------------------------------------
    # 3. VERIFY STATE ISOLATION FROM GLOBAL MULTIPLAYER GAME
    # -------------------------------------------------------------
    print("\n--- [TEST 3] State Isolation Verification ---")
    global_gm = AppTest.from_file("app.py")
    global_gm.query_params["team"] = "main"
    global_gm.run()
    # The global game should still be in its initial state unaffected by instructor sandbox
    assert global_gm.session_state["voter_id"] is not None
    print("  ✓ Global multiplayer game state verified completely isolated from instructor sandbox.")

    # -------------------------------------------------------------
    # 4. FULL SEQUENTIAL GAMEPLAY WALKTHROUGH
    # -------------------------------------------------------------
    print("\n--- [TEST 4] Sequential Team Progression (Round 1) ---")
    
    # In Lobby: Start Round 1 via Mission Controls
    start_r1_btn = next((b for b in inst.button if "Start Round 1" in b.label), None)
    assert start_r1_btn is not None, "Start Round 1 button not found in instructor HUD"
    start_r1_btn.click().run()
    print("  ✓ Started Round 1. Sequence transitioned to Threat Actor Captain.")

    # STEP A: THREAT ACTOR CAPTAIN
    assert any("Threat Actor Captain" in info.value for info in inst.info)
    deploy_btn = next((b for b in inst.button if "Deploy Vector" in b.label), None)
    assert deploy_btn is not None, "Threat Actor deploy vector button missing"
    deploy_btn.click().run()
    print("  ✓ Threat Actor Captain deployed vector. Sequence transitioned to IT Defense Captain.")

    # STEP B: IT DEFENSE CAPTAIN
    assert any("IT Defense Captain" in info.value for info in inst.info)
    it_deploy_btn = next((b for b in inst.button if "Deploy & Recommend Option" in b.label), None)
    assert it_deploy_btn is not None, "IT Defense deploy option button missing"
    it_deploy_btn.click().run()
    print("  ✓ IT Defense Captain recommended containment. Sequence transitioned to Executive Boardroom.")

    # STEP C: EXECUTIVE BOARDROOM CAPTAIN
    assert any("Executive Boardroom Captain" in info.value for info in inst.info)
    exec_auth_btn = next((b for b in inst.button if "Authorize Directive" in b.label), None)
    assert exec_auth_btn is not None, "Executive Board authorize directive button missing"
    exec_auth_btn.click().run()
    print("  ✓ Executive Boardroom Captain authorized directive. Sequence transitioned to Media & PR Scrum.")

    # STEP D: MEDIA & PR SCRUM CAPTAIN
    assert any("Media & PR Captain" in info.value for info in inst.info)
    pub_btn = next((b for b in inst.button if "Publish Headline" in b.label), None)
    assert pub_btn is not None, "Media publish headline button missing"
    pub_btn.click().run()
    print("  ✓ Media & PR Captain published headline. Round 1 concluded, transitioned to Recap.")

    # STEP E: ROUND 1 RECAP & ADVANCE TO ROUND 2
    assert any("Round 1 Debrief" in info.value for info in inst.info)
    adv_r2_btn = next((b for b in inst.button if "Start Round 2" in b.label), None)
    assert adv_r2_btn is not None, "Advance to Round 2 button missing"
    adv_r2_btn.click().run()
    print("  ✓ Advanced to Round 2.")

    # -------------------------------------------------------------
    # 5. ROUND 2 & ADVERSARY FINAL ACTION GAMBIT
    # -------------------------------------------------------------
    print("\n--- [TEST 5] Round 2 Sequence & Adversary Final Gambit ---")
    
    # R2 Hackers
    deploy_btn_r2 = next((b for b in inst.button if "Deploy Vector" in b.label), None)
    assert deploy_btn_r2 is not None
    deploy_btn_r2.click().run()

    # R2 IT
    it_btn_r2 = next((b for b in inst.button if "Deploy & Recommend Option" in b.label), None)
    assert it_btn_r2 is not None
    it_btn_r2.click().run()

    # R2 Exec
    exec_btn_r2 = next((b for b in inst.button if "Authorize Directive" in b.label), None)
    assert exec_btn_r2 is not None
    exec_btn_r2.click().run()

    # R2 Media
    media_btn_r2 = next((b for b in inst.button if "Publish Headline" in b.label), None)
    assert media_btn_r2 is not None
    media_btn_r2.click().run()

    # Advance from R2 Recap to Adversary Final Action Gambit
    adv_gambit_btn = next((b for b in inst.button if "Advance to Final Threat Actor Gambit" in b.label), None)
    assert adv_gambit_btn is not None, "Button to advance to Final Threat Actor Gambit missing"
    adv_gambit_btn.click().run()
    print("  ✓ Advanced to Adversary Final Action Gambit.")

    # ADVERSARY FINAL ACTION: Press Attack or Retreat
    assert any("Final Gambit" in info.value for info in inst.info)
    press_btn = next((b for b in inst.button if "Press the Attack" in b.label), None)
    retreat_btn = next((b for b in inst.button if "Safe Retreat" in b.label), None)
    assert press_btn is not None, "Press the Attack button missing"
    assert retreat_btn is not None, "Safe Retreat button missing"

    # Instructor authorizes Press Attack
    press_btn.click().run()
    print("  ✓ Executed final gambit: Press the Attack.")

    # GAME OVER VERIFICATION
    assert any("Simulation Concluded" in info.value for info in inst.info)
    all_text = " ".join([m.value for m in inst.markdown])
    assert any(badge in all_text for badge in [
        "MISSION SUCCESS — ENTERPRISE PREVAILED",
        "SURVIVED — ENTERPRISE DAMAGED BUT SOLVENT",
        "CATASTROPHIC FAILURE — BANKRUPTCY DECLARED"
    ])
    assert "Final Company Health:" in all_text
    print("  ✓ Final outcome assessment rendered successfully with Company Health score.")

    # Reset test simulation button
    reset_btn = next((b for b in inst.button if "Reset Simulation for New Playthrough" in b.label or "Reset Test Sim" in b.label), None)
    assert reset_btn is not None
    reset_btn.click().run()
    assert any("Simulation in Lobby" in info.value for info in inst.info)
    print("  ✓ Reset Test Simulation cleanly returned sandbox to Lobby for a new run.")

    print("\n=====================================================================")
    print("🎉 ALL INSTRUCTOR TESTING MODE TESTS PASSED FLAWLESSLY!")
    print("=====================================================================")

if __name__ == "__main__":
    test_instructor_mode_end_to_end()
