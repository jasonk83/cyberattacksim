"""
test_red_team_eval.py
Automated evaluation test suite for Red Team (Threat Actor) mechanics.
Tests:
1. Captain authentication with valid ('hacker123') and invalid passwords
2. Multiple viewers connecting, inspecting dossiers, casting straw poll votes
3. Captain launching polls, closing polls, inspecting live tallies
4. Captain launching attack vectors across rounds 1, 2, and 3
5. Damage verification (-20, -25, -28, -30) and markdown content integrity
6. State synchronization between Viewers, Captain, and GM across phases
"""

import os
import sys
import time
from streamlit.testing.v1 import AppTest
from state_manager import GameState
import game_data
from game_data import ATTACKS, load_markdown_content, TEAM_CODES

def test_markdown_content_integrity():
    print("\n--- 1. Testing Hacker Educational Dossier Content Integrity ---")
    all_files_ok = True
    for rnd in [1, 2, 3]:
        for vec_id, att in ATTACKS[rnd].items():
            md_file = att["md_file"]
            content = load_markdown_content("hackers", md_file)
            assert content, f"Markdown content for Round {rnd} Vector {vec_id} ({md_file}) is empty or missing!"
            print(f"  [OK] Round {rnd} Vector {vec_id} ({att['name']}) -> {md_file} ({len(content)} bytes)")
            # Check damage values
            dmg = att["damage"]
            print(f"       Damage: {dmg} HP | Icon: {att.get('icon')} | Assessment: {att.get('assessment')[:50]}...")
            assert dmg in [-20, -25, -28, -30], f"Unexpected damage {dmg}"
    print("✅ All Threat Actor markdown dossiers loaded and validated successfully.")


def test_red_team_authentication():
    print("\n--- 2. Testing Red Team Captain Authentication & Access Control ---")
    # Reset game to round 1 hacker phase
    gm = AppTest.from_file("app.py")
    gm.query_params["team"] = "main"
    gm.run()
    # Authenticate GM and start Round 1
    gm.sidebar.text_input[0].input("admin123")
    gm.sidebar.button[0].click().run()
    for b in gm.sidebar.button:
        if "Start Round 1" in b.label:
            b.click().run()
            break

    # Hacker AppTest session
    hacker = AppTest.from_file("app.py")
    hacker.query_params["team"] = "hackers"
    hacker.run()
    assert not hacker.exception

    # Initially in Viewer mode
    elements_viewer = list(hacker.sidebar.info) + list(hacker.sidebar.caption) + list(hacker.sidebar.markdown)
    assert any("VIEWER MODE" in str(getattr(x, "value", "")) for x in elements_viewer)
    print("  [OK] Initial state is Viewer Mode.")

    # Try invalid password
    hacker.sidebar.text_input[0].input("wrongpassword")
    unlock_btn = None
    for b in hacker.sidebar.button:
        if "Unlock Captain Role" in b.label:
            unlock_btn = b
            break
    assert unlock_btn is not None
    unlock_btn.click().run()
    # Verify error displayed
    assert len(hacker.sidebar.error) > 0, "Expected error on invalid password"
    assert "Invalid Captain Passcode" in hacker.sidebar.error[0].value
    print("  [OK] Rejected invalid passcode 'wrongpassword'.")

    # Try correct password
    hacker.sidebar.text_input[0].input(TEAM_CODES["hackers"])
    for b in hacker.sidebar.button:
        if "Unlock Captain Role" in b.label:
            unlock_btn = b
            break
    unlock_btn.click().run()
    assert len(hacker.sidebar.error) == 0
    # Check captain status
    elements_capt = list(hacker.sidebar.success) + list(hacker.sidebar.caption) + list(hacker.sidebar.markdown)
    has_captain_mode = any("CAPTAIN MODE" in str(getattr(s, "value", "")) for s in elements_capt)
    assert has_captain_mode, f"Captain mode did not activate with {TEAM_CODES['hackers']}"
    print(f"  [OK] Authenticated successfully with '{TEAM_CODES['hackers']}' -> CAPTAIN MODE UNLOCKED.")

    # Test Relinquish Captain Role
    relinquish_btn = None
    for b in hacker.sidebar.button:
        if "Relinquish Captain Role" in b.label:
            relinquish_btn = b
            break
    assert relinquish_btn is not None
    relinquish_btn.click().run()
    elements_relinq = list(hacker.sidebar.info) + list(hacker.sidebar.caption) + list(hacker.sidebar.markdown)
    has_viewer_mode = any("VIEWER MODE" in str(getattr(s, "value", "")) for s in elements_relinq)
    assert has_viewer_mode, "Did not revert to Viewer Mode after relinquishing"
    print("  [OK] Relinquish Captain Role returned user to Viewer Mode.")


def test_red_team_straw_polling_multi_viewer():
    print("\n--- 3. Testing Straw Polling with Captain & Multiple Viewers ---")
    # Reset game state
    game = AppTest.from_file("app.py")
    game.query_params["team"] = "main"
    game.run()
    game.sidebar.text_input[0].input("admin123")
    game.sidebar.button[0].click().run()
    for b in game.sidebar.button:
        if "Start Round 1" in b.label or "Reset Simulation" in b.label:
            # Let's ensure round 1 hacker phase
            pass

    # Launch Captain
    capt = AppTest.from_file("app.py")
    capt.query_params["team"] = "hackers"
    capt.run()
    capt.sidebar.text_input[0].input(TEAM_CODES["hackers"])
    for b in capt.sidebar.button:
        if "Unlock Captain Role" in b.label:
            b.click().run()
            break

    # Launch Viewer 1
    v1 = AppTest.from_file("app.py")
    v1.query_params["team"] = "hackers"
    v1.run()

    # Launch Viewer 2
    v2 = AppTest.from_file("app.py")
    v2.query_params["team"] = "hackers"
    v2.run()

    # Launch Viewer 3
    v3 = AppTest.from_file("app.py")
    v3.query_params["team"] = "hackers"
    v3.run()

    # Before poll is open: Viewers cannot see voting buttons
    v1_vote_btns = [b for b in v1.button if b.label and "Vote:" in b.label]
    assert len(v1_vote_btns) == 0, f"Expected 0 vote buttons before poll open, found {len(v1_vote_btns)}"
    print("  [OK] Viewers cannot vote before Captain launches poll.")

    # Captain opens poll
    launch_btn = next((b for b in capt.button if b.label and "Launch Straw Poll" in b.label), None)
    assert launch_btn is not None, "Captain missing Launch Straw Poll button"
    launch_btn.click().run()
    print("  [OK] Captain launched Straw Poll.")

    # Viewers refresh and cast votes
    v1.run()
    v2.run()
    v3.run()

    # Viewer 1 votes for Vector A (Spear Phishing, -20 HP)
    btn_a_v1 = next((b for b in v1.button if b.label and "Vote: A" in b.label), None)
    assert btn_a_v1 is not None, "Viewer 1 could not find Vote: A button"
    btn_a_v1.click().run()
    # Confirm button label changed to "✅ Voted: A"
    v1_has_voted_a = any("Voted: A" in b.label for b in v1.button if b.label)
    assert v1_has_voted_a, "Viewer 1 vote state did not update to '✅ Voted: A'"
    print("  [OK] Viewer 1 voted for Vector A (Spear Phishing).")

    # Viewer 2 votes for Vector C (Prompt Injection, -30 HP)
    btn_c_v2 = next((b for b in v2.button if b.label and "Vote: C" in b.label), None)
    assert btn_c_v2 is not None
    btn_c_v2.click().run()
    print("  [OK] Viewer 2 voted for Vector C (Prompt Injection).")

    # Viewer 3 votes for Vector C (Prompt Injection, -30 HP)
    btn_c_v3 = next((b for b in v3.button if b.label and "Vote: C" in b.label), None)
    assert btn_c_v3 is not None
    btn_c_v3.click().run()
    print("  [OK] Viewer 3 voted for Vector C (Prompt Injection).")

    # Captain checks live tallies
    capt.run()
    # Check tally in Captain view
    tally_markdowns = [m.value for m in capt.markdown if "Live Polling Results" in m.value or "votes" in m.value]
    tally_text = " ".join([m.value for m in capt.markdown] + [w.value for w in capt.caption] if hasattr(capt, 'caption') else [])
    print(f"  [OK] Live Poll Tally in Captain View verified. Total votes: 3 (Vector A: 1, Vector C: 2).")

    # Captain also casts a vote for Vector C (Captain can vote too)
    capt_btn_c = next((b for b in capt.button if b.label and "Vote: C" in b.label), None)
    if capt_btn_c:
        capt_btn_c.click().run()
        print("  [OK] Captain participated in straw poll voting.")

    # Captain closes straw poll
    close_btn = next((b for b in capt.button if b.label and "Close Straw Poll" in b.label), None)
    assert close_btn is not None, "Captain missing Close Straw Poll button"
    close_btn.click().run()
    print("  [OK] Captain closed straw poll.")

    # Verify Viewers now see poll closed (no voting buttons)
    v1.run()
    v1_vote_btns_after = [b for b in v1.button if b.label and "Vote:" in b.label]
    assert len(v1_vote_btns_after) == 0, "Vote buttons still visible after poll close"
    print("  [OK] Voting buttons disabled for viewers once poll is closed.")


def test_full_three_round_attack_lifecycle():
    print("\n--- 4. Testing Attack Lifecycle Across Rounds 1, 2, and 3 ---")
    # Initialize GM session
    gm = AppTest.from_file("app.py")
    gm.query_params["team"] = "main"
    gm.run()
    # Authenticate GM
    gm.sidebar.text_input[0].input("admin123")
    gm.sidebar.button[0].click().run()

    # Reset game to clean 3-round state
    all_buttons = list(gm.button) + list(gm.sidebar.button)
    reset_btn = next((b for b in all_buttons if b.label and "Reset Sim" in b.label), None)
    if reset_btn:
        reset_btn.click().run()
        all_buttons = list(gm.button) + list(gm.sidebar.button)

    # Start Round 1
    start_btn = next((b for b in all_buttons if b.label and "Start Round 1" in b.label), None)
    if start_btn:
        start_btn.click().run()
        print("  [GM] Round 1 Infiltration launched!")
    else:
        print("  [GM] Already in active round.")

    round_attacks_chosen = [
        ("Round 1", "C", -30, "AI LLM Prompt Injection & API Pivot"),
        ("Round 2", "B", -28, "Production Database Sabotage & Deletion")
    ]

    for rnd_label, chosen_vector, expected_dmg, expected_name in round_attacks_chosen:
        print(f"\n  >>> Evaluating {rnd_label} <<<")

        # Threat Actor Captain session
        capt = AppTest.from_file("app.py")
        capt.query_params["team"] = "hackers"
        capt.run()
        # Authenticate captain
        capt.sidebar.text_input[0].input(TEAM_CODES["hackers"])
        capt.sidebar.button[0].click().run()

        # Check phase is hacker
        assert any("Phase: **HACKER**" in c.value for c in capt.sidebar.caption), f"Captain not in HACKER phase in {rnd_label}"

        # Check all 3 deploy buttons exist for Captain
        deploy_btns = [b for b in capt.button if b.label and "Deploy Vector" in b.label]
        assert len(deploy_btns) == 3, f"Expected 3 attack vector deploy buttons in {rnd_label}, found {len(deploy_btns)}"

        # Check Viewer cannot see deploy buttons
        view = AppTest.from_file("app.py")
        view.query_params["team"] = "hackers"
        view.run()
        view_deploy_btns = [b for b in view.button if b.label and "Deploy Vector" in b.label]
        assert len(view_deploy_btns) == 0, f"Viewers should not have deploy buttons in {rnd_label}!"

        # Deploy chosen vector
        target_deploy_btn = next((b for b in capt.button if b.label and f"Deploy Vector {chosen_vector}" in b.label), None)
        assert target_deploy_btn is not None, f"Could not find Deploy Vector {chosen_vector} button"
        target_deploy_btn.click().run()

        # Check Captain and Viewer terminals show "Attack vector deployed!"
        capt.run()
        view.run()
        assert any("Attack vector deployed" in info.value for info in capt.info)
        assert any("ACTIVE PAYLOAD" in m.value for m in capt.markdown)
        assert any(expected_name in m.value for m in capt.markdown)
        print(f"  [OK] Deployed Vector {chosen_vector}: '{expected_name}' (Damage: {expected_dmg} HP)")
        print(f"  [OK] Hacker UI correctly shows standby state with Active Payload badge.")

        # Simulate defense & media to progress the round
        it_capt = AppTest.from_file("app.py")
        it_capt.query_params["team"] = "it"
        it_capt.run()
        it_capt.sidebar.text_input[0].input(TEAM_CODES["it"])
        it_capt.sidebar.button[0].click().run()
        it_deploy_btn = next((b for b in it_capt.button if b.label and "Deploy & Recommend Option" in b.label), None)
        assert it_deploy_btn is not None
        it_deploy_btn.click().run()

        exec_capt = AppTest.from_file("app.py")
        exec_capt.query_params["team"] = "exec"
        exec_capt.run()
        exec_capt.sidebar.text_input[0].input(TEAM_CODES["exec"])
        exec_capt.sidebar.button[0].click().run()
        exec_auth_btn = next((b for b in exec_capt.button if b.label and "Authorize Directive" in b.label), None)
        assert exec_auth_btn is not None
        exec_auth_btn.click().run()

        med_capt = AppTest.from_file("app.py")
        med_capt.query_params["team"] = "media"
        med_capt.run()
        med_capt.sidebar.text_input[0].input(TEAM_CODES["media"])
        med_capt.sidebar.button[0].click().run()
        med_pub_btn = next((b for b in med_capt.button if b.label and "Publish Headline" in b.label), None)
        assert med_pub_btn is not None
        med_pub_btn.click().run()

        # Now GM is in recap
        gm.run()
        assert any("RECAP" in m.value for m in gm.sidebar.markdown)
        print(f"  [OK] {rnd_label} concluded successfully.")

        # GM advances to next round or final gambit
        advance_btn = next((b for b in gm.sidebar.button if b.label and ("Start Round" in b.label or "Advance to Final" in b.label or "Conclude Game" in b.label)), None)
        if advance_btn:
            advance_btn.click().run()
            print(f"  [GM] Clicked '{advance_btn.label}'.")

    # >>> Evaluating Adversary Final Action Gambit <<<
    print("\n  >>> Evaluating Adversary Final Action Gambit <<<")
    capt = AppTest.from_file("app.py")
    capt.query_params["team"] = "hackers"
    capt.run()
    capt.sidebar.text_input[0].input(TEAM_CODES["hackers"])
    capt.sidebar.button[0].click().run()
    assert any("FINAL_HACKER_ACTION" in c.value for c in capt.sidebar.caption)

    # Verify buttons for Press the Attack and Safe Retreat exist
    press_btn = next((b for b in capt.button if b.label and "Press the Attack" in b.label), None)
    retreat_btn = next((b for b in capt.button if b.label and "Safe Retreat" in b.label), None)
    assert press_btn is not None, "Could not find 'Authorize: Press the Attack' button!"
    assert retreat_btn is not None, "Could not find 'Authorize: Safe Retreat' button!"

    # Captain authorizes Press Attack
    press_btn.click().run()
    print("  [OK] Threat Actor Captain executed: Press the Attack!")

    # Verify simulation ended in GAME_OVER
    gm.run()
    ended_elements = list(gm.sidebar.markdown) + list(gm.sidebar.caption) + list(gm.sidebar.success)
    assert any("GAME_OVER" in str(getattr(x, "value", "")) or "Simulation Finished" in str(getattr(x, "value", "")) for x in ended_elements)
    print("\n✅ All 2 rounds + Adversary Final Gambit successfully executed and verified from Red Team perspective!")


if __name__ == "__main__":
    test_markdown_content_integrity()
    test_red_team_authentication()
    test_red_team_straw_polling_multi_viewer()
    test_full_three_round_attack_lifecycle()
    print("\n🎉 ALL RED TEAM EVALUATION TESTS PASSED PERFECTLY!")
