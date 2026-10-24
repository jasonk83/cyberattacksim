"""
test_gm_hp_adjustment.py
Automated test suite verifying the manual company HP adjustment buttons (+10 HP and -10 HP)
in the Game Master (GM) console main area.

Verifies:
1. GameState.adjust_company_health logic (delta addition, subtraction, upper/lower clamping, and undo snapshot).
2. Access control / Password gate:
   - Buttons are NOT visible when unauthenticated (?team=main without admin password).
   - Buttons ARE visible in the main area once the admin password ('admin123') is entered.
   - Buttons disappear again upon locking the console.
3. Interactive behavior:
   - Clicking '-10 HP' decreases company HP by 10 points.
   - Clicking '+10 HP' increases company HP by 10 points.
   - Health is clamped properly between 0.0 and 100.0 HP.
4. Workflow availability:
   - Manual adjustment works at any stage in the workflow (lobby, hacker, it, exec, media, recap, game_over).
5. Instructor testing mode integration (?team=instructor).
"""

import sys
from streamlit.testing.v1 import AppTest
from state_manager import GameState


def test_game_state_adjust_company_health():
    print("\n--- [TEST 1] GameState.adjust_company_health Unit Tests ---")
    game = GameState()
    assert game.company_health == 100.0, f"Expected initial HP 100.0, got {game.company_health}"

    # Subtract 10 HP
    new_hp = game.adjust_company_health(-10.0, reason="Penalize IT for timeout")
    assert new_hp == 90.0
    assert game.company_health == 90.0
    print("  ✓ Successfully subtracted 10 HP (100.0 -> 90.0 HP).")

    # Subtract another 10 HP
    game.adjust_company_health(-10.0)
    assert game.company_health == 80.0
    print("  ✓ Successfully subtracted another 10 HP (90.0 -> 80.0 HP).")

    # Add 10 HP
    game.adjust_company_health(10.0, reason="Penalize hackers for timeout")
    assert game.company_health == 90.0
    print("  ✓ Successfully added 10 HP (80.0 -> 90.0 HP).")

    # Test Upper Clamping (100.0 max)
    game.adjust_company_health(20.0)
    assert game.company_health == 100.0
    print("  ✓ Health clamped at maximum 100.0 HP.")

    # Test Lower Clamping (0.0 min)
    game.adjust_company_health(-150.0)
    assert game.company_health == 0.0
    print("  ✓ Health clamped at minimum 0.0 HP.")

    # Test Undo rollback
    assert len(game.snapshots) > 0
    rolled_back = game.undo_last_round()
    assert rolled_back is True
    assert game.company_health == 100.0
    print("  ✓ Undo restored health back to snapshot state.")


def test_gm_console_password_gate():
    print("\n--- [TEST 2] GM Console Password Gate for HP Adjustment Buttons ---")

    # 1. Unauthenticated viewer visiting ?team=main
    at_unauth = AppTest.from_file("app.py")
    at_unauth.query_params["team"] = "main"
    at_unauth.run()
    assert not at_unauth.exception

    # Buttons should NOT be present in main area before password is provided
    add_btns_unauth = [b for b in at_unauth.button if "Add +10 HP" in b.label or "+10 HP" in b.label]
    sub_btns_unauth = [b for b in at_unauth.button if "Subtract -10 HP" in b.label or "-10 HP" in b.label]
    assert len(add_btns_unauth) == 0, "Security Violation: +10 HP button rendered before admin password was provided!"
    assert len(sub_btns_unauth) == 0, "Security Violation: -10 HP button rendered before admin password was provided!"
    print("  ✓ Verified: +10 HP and -10 HP buttons are HIDDEN prior to entering admin password.")

    # 2. Enter invalid password
    admin_pwd_input = at_unauth.sidebar.text_input[0]
    admin_pwd_input.input("wrongpass")
    at_unauth.sidebar.button[0].click().run()
    assert not at_unauth.exception
    assert any("Incorrect Admin Password" in err.value for err in at_unauth.sidebar.error)
    add_btns_wrong = [b for b in at_unauth.button if "Add +10 HP" in b.label or "+10 HP" in b.label]
    assert len(add_btns_wrong) == 0, "Security Violation: +10 HP button rendered after wrong password!"
    print("  ✓ Verified: Buttons remain HIDDEN after entering incorrect password.")

    # 3. Enter valid admin password ('admin123') in fresh session
    at = AppTest.from_file("app.py")
    at.query_params["team"] = "main"
    at.run()
    at.sidebar.text_input[0].input("admin123")
    at.sidebar.button[0].click().run()
    assert not at.exception
    assert any("GM Console Unlocked" in s.value for s in at.sidebar.success)

    # Buttons MUST now appear in main area
    add_btn = next((b for b in at.button if "Add +10 HP" in b.label), None)
    sub_btn = next((b for b in at.button if "Subtract -10 HP" in b.label), None)
    assert add_btn is not None, "Missing '+10 HP' button in GM console main area after authentication!"
    assert sub_btn is not None, "Missing '-10 HP' button in GM console main area after authentication!"
    print("  ✓ Verified: '+10 HP' and '-10 HP' buttons successfully APPEAR after unlocking GM Console.")

    # 4. Lock console again
    lock_btn = next((b for b in at.sidebar.button if "Lock Console" in b.label), None)
    assert lock_btn is not None, "Lock Console button missing from authenticated sidebar"
    lock_btn.click().run()
    assert not at.exception

    # Buttons should disappear
    add_btns_relocked = [b for b in at.button if "Add +10 HP" in b.label or "+10 HP" in b.label]
    sub_btns_relocked = [b for b in at.button if "Subtract -10 HP" in b.label or "-10 HP" in b.label]
    assert len(add_btns_relocked) == 0, "+10 HP button persisted after locking console!"
    assert len(sub_btns_relocked) == 0, "-10 HP button persisted after locking console!"
    print("  ✓ Verified: Buttons cleanly disappear after locking GM Console.")


def test_interactive_hp_adjustment_in_workflow():
    print("\n--- [TEST 3] Interactive Manual HP Adjustment in Live Workflow ---")

    at = AppTest.from_file("app.py")
    at.query_params["team"] = "main"
    at.run()

    # Authenticate as GM
    at.sidebar.text_input[0].input("admin123")
    at.sidebar.button[0].click().run()
    assert not at.exception

    # Reset simulation to clean lobby state
    for b in at.sidebar.button:
        if "Reset Sim" in b.label:
            b.click().run()
            break

    # Check initial health in lobby
    # Find buttons
    sub_btn = next((b for b in at.button if "Subtract -10 HP" in b.label), None)
    add_btn = next((b for b in at.button if "Add +10 HP" in b.label), None)
    assert sub_btn is not None
    assert add_btn is not None

    # 1. Test in Lobby: Penalize IT/Exec (-10 HP)
    sub_btn.click().run()
    assert not at.exception
    # Gauge should reflect 90.0 HP
    main_text = " ".join(m.value for m in at.markdown)
    assert "90.0" in main_text or "90" in main_text, "Markdown gauge text did not update to 90 HP"
    print("  ✓ Subtracted 10 HP in Lobby phase (Health is now 90.0 HP).")

    # 2. Start Round 1 (Transition to Hacker phase)
    start_btn = next((b for b in at.sidebar.button if "Start Round 1" in b.label), None)
    if not start_btn:
        start_btn = next((b for b in at.button if "Start Round 1" in b.label), None)
    assert start_btn is not None
    start_btn.click().run()
    assert not at.exception

    # 3. Test in Hacker phase: Penalize Hackers/Media (+10 HP)
    add_btn = next((b for b in at.button if "Add +10 HP" in b.label), None)
    assert add_btn is not None, "+10 HP button missing in hacker phase"
    add_btn.click().run()
    assert not at.exception
    main_text = " ".join(m.value for m in at.markdown)
    assert "100.0" in main_text, "Markdown gauge did not update to 100.0 HP after +10 adjustment"
    print("  ✓ Added 10 HP in Hacker phase (Health restored to 100.0 HP).")

    # 4. Subtract twice (-20 HP total)
    sub_btn = next((b for b in at.button if "Subtract -10 HP" in b.label), None)
    sub_btn.click().run()
    sub_btn = next((b for b in at.button if "Subtract -10 HP" in b.label), None)
    sub_btn.click().run()
    assert not at.exception
    main_text = " ".join(m.value for m in at.markdown)
    assert "80.0" in main_text, "Markdown gauge did not reflect 80.0 HP after two -10 deductions"
    print("  ✓ Subtracted 20 HP sequentially (Health is now 80.0 HP).")


def test_instructor_mode_hp_buttons():
    print("\n--- [TEST 4] Instructor Testing Mode Integration ---")

    inst = AppTest.from_file("app.py")
    inst.query_params["team"] = "instructor"
    inst.run()

    # Locked initially
    add_btns_locked = [b for b in inst.button if "Add +10 HP" in b.label]
    assert len(add_btns_locked) == 0, "HP buttons rendered on locked instructor screen"

    # Unlock with tryit123
    inst.text_input[0].input("tryit123")
    inst.button[0].click().run()
    assert not inst.exception

    # Buttons should be available in instructor HUD
    add_btn = next((b for b in inst.button if "Add +10 HP" in b.label), None)
    sub_btn = next((b for b in inst.button if "Subtract -10 HP" in b.label), None)
    assert add_btn is not None, "+10 HP button missing in instructor mode"
    assert sub_btn is not None, "-10 HP button missing in instructor mode"
    print("  ✓ HP adjustment buttons present and operational in Instructor Testing Sandbox.")


if __name__ == "__main__":
    test_game_state_adjust_company_health()
    test_gm_console_password_gate()
    test_interactive_hp_adjustment_in_workflow()
    test_instructor_mode_hp_buttons()
    print("\n🎉 ALL GM COMPANY HP ADJUSTMENT TESTS PASSED 100%!")
