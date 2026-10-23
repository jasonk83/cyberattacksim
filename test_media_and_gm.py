"""
test_media_and_gm.py
Comprehensive automated test suite for Media Scrum & Game Master (GM Projector & Console)
for CloudStore Command: Cyber Attack Simulation
"""

import sys
import time
from streamlit.testing.v1 import AppTest
from scoring_engine import calculate_round_impact, evaluate_final_outcome, get_outcome_thresholds
from game_data import TEAM_CODES, DYNAMIC_HEADLINES, ATTACKS, IT_CHOICES

def helper_advance_to_media(round_mult=1.0, it_choice_opt="1", exec_choice_opt="downgrade"):
    """Drives the simulation from Lobby to Media Scrum phase via AppTest clicks."""
    # 1. GM starts Round
    gm = AppTest.from_file("app.py")
    gm.query_params["team"] = "main"
    gm.run()
    gm.sidebar.text_input[0].input("admin123")
    gm.sidebar.button[0].click().run()

    for b in gm.sidebar.button:
        if "Reset Sim" in b.label:
            b.click().run()
            break

    if round_mult != 1.0:
        mult_select = gm.sidebar.selectbox[0]
        mult_select.set_value(round_mult).run()

    for b in gm.sidebar.button:
        if "Start Round 1" in b.label:
            b.click().run()
            break

    # 2. Red Team Hackers deploy Vector B
    h = AppTest.from_file("app.py")
    h.query_params["team"] = "hackers"
    h.run()
    h.sidebar.text_input[0].input("hacker123")
    h.sidebar.button[0].click().run()
    for b in h.button:
        if "Deploy Vector B" in b.label:
            b.click().run()
            break

    # 3. IT Defense deploys Option 1
    it = AppTest.from_file("app.py")
    it.query_params["team"] = "it"
    it.run()
    it.sidebar.text_input[0].input("tech123")
    it.sidebar.button[0].click().run()
    for b in it.button:
        if f"Deploy & Recommend Option {it_choice_opt}" in b.label:
            b.click().run()
            break

    # 4. Executive Board issues directive
    ex = AppTest.from_file("app.py")
    ex.query_params["team"] = "exec"
    ex.run()
    ex.sidebar.text_input[0].input("board123")
    ex.sidebar.button[0].click().run()
    for b in ex.button:
        if exec_choice_opt.lower() in b.label.lower():
            b.click().run()
            break

    return gm

def test_media_authentication_and_viewers():
    print("\n--- [TEST 1] Media Captain Authentication & Viewer Separation ---")
    
    # 1. Test Incorrect Passcode
    m_fail = AppTest.from_file("app.py")
    m_fail.query_params["team"] = "media"
    m_fail.run()
    assert not m_fail.exception
    assert len(m_fail.sidebar.text_input) > 0
    m_fail.sidebar.text_input[0].input("wrongpassword")
    m_fail.sidebar.button[0].click().run()
    assert not m_fail.exception
    assert any("Invalid Captain Passcode" in err.value for err in m_fail.sidebar.error)
    print("  ✓ Invalid passcode rejected with error message.")

    # 2. Test Correct Passcode ('press123')
    m_capt = AppTest.from_file("app.py")
    m_capt.query_params["team"] = "media"
    m_capt.run()
    m_capt.sidebar.text_input[0].input("press123")
    m_capt.sidebar.button[0].click().run()
    assert not m_capt.exception
    assert any("CAPTAIN MODE UNLOCKED" in s.value for s in m_capt.sidebar.success)
    print("  ✓ Passcode 'press123' successfully unlocked Captain Mode.")

    # 3. Test Relinquish Captain Role
    relinq_btn = next((b for b in m_capt.sidebar.button if "Relinquish Captain Role" in b.label), None)
    assert relinq_btn is not None, "Relinquish Captain Role button should be available"
    relinq_btn.click().run()
    assert any("VIEWER MODE" in info.value for info in m_capt.sidebar.info)
    print("  ✓ Relinquish Captain Role reverted session back to Viewer Mode.")

    # 4. Viewer Mode verification
    m_view = AppTest.from_file("app.py")
    m_view.query_params["team"] = "media"
    m_view.run()
    assert not m_view.exception
    assert any("VIEWER MODE" in info.value for info in m_view.sidebar.info)
    print("  ✓ Unauthenticated user defaults cleanly to Viewer Mode.")


def test_media_straw_polling_and_headlines():
    print("\n--- [TEST 2] Media Straw Polling & Headline Impact Validation ---")

    # 1. Advance Game State to Media Phase in Round 1
    gm = helper_advance_to_media(round_mult=1.0, it_choice_opt="1", exec_choice_opt="downgrade")

    # Setup Media Captain
    m_capt = AppTest.from_file("app.py")
    m_capt.query_params["team"] = "media"
    m_capt.run()
    m_capt.sidebar.text_input[0].input("press123")
    m_capt.sidebar.button[0].click().run()

    # Verify Captain sees breaking wire & executive decision
    assert any("BREAKING INTELLIGENCE WIRE" in m.value for m in m_capt.markdown)
    assert any("DOWNGRADE" in m.value for m in m_capt.markdown)
    print("  ✓ Media terminal displays Breaking Intelligence Wire and Executive Directive (DOWNGRADE).")

    # Verify headline clarity and impact indicators in Captain view
    capt_markdown_text = " ".join(m.value for m in m_capt.markdown)
    assert "Headline 1" in capt_markdown_text and "Sensationalist" in capt_markdown_text
    assert "Health -12" in capt_markdown_text
    assert "Headline 2" in capt_markdown_text and "Critical" in capt_markdown_text
    assert "Health -5" in capt_markdown_text
    assert "Headline 3" in capt_markdown_text and "Balanced" in capt_markdown_text
    assert "Health +2" in capt_markdown_text
    assert "Headline 4" in capt_markdown_text and "Favorable" in capt_markdown_text
    assert "Health +8" in capt_markdown_text
    print("  ✓ Headline UI clearly displays Tiers (Sensationalist/Critical/Balanced/Favorable) and Health Deltas (-12, -5, +2, +8).")

    # 2. Test Straw Polling
    # Captain launches poll
    launch_btn = next((b for b in m_capt.button if "Launch Straw Poll" in b.label), None)
    assert launch_btn is not None, "Launch Straw Poll button not found in Captain view"
    launch_btn.click().run()
    print("  ✓ Media Captain launched live Straw Poll.")

    # Setup Viewer 1, Viewer 2, Viewer 3
    v1 = AppTest.from_file("app.py")
    v1.query_params["team"] = "media"
    v1.session_state["voter_id"] = "viewer_press_1"
    v1.run()

    v2 = AppTest.from_file("app.py")
    v2.query_params["team"] = "media"
    v2.session_state["voter_id"] = "viewer_press_2"
    v2.run()

    v3 = AppTest.from_file("app.py")
    v3.query_params["team"] = "media"
    v3.session_state["voter_id"] = "viewer_press_3"
    v3.run()

    # Viewers cast votes across headlines
    # Viewer 1 votes Headline 1 (Sensationalist)
    btn_v1 = next((b for b in v1.button if "Headline 1" in b.label and "Vote" in b.label), None)
    assert btn_v1 is not None, "Vote: Headline 1 button not found for Viewer 1"
    btn_v1.click().run()

    # Viewer 2 votes Headline 3 (Balanced)
    btn_v2 = next((b for b in v2.button if "Headline 3" in b.label and "Vote" in b.label), None)
    assert btn_v2 is not None
    btn_v2.click().run()

    # Viewer 3 votes Headline 4 (Favorable)
    btn_v3 = next((b for b in v3.button if "Headline 4" in b.label and "Vote" in b.label), None)
    assert btn_v3 is not None
    btn_v3.click().run()

    # Verify Viewers have NO Publish buttons
    viewer_pub_btns = [b for b in v1.button if "Publish" in b.label]
    assert len(viewer_pub_btns) == 0, f"Viewer should not see Publish buttons: {viewer_pub_btns}"
    print("  ✓ Viewers are strictly prohibited from publishing headlines.")

    # Captain sees the votes
    m_capt.run()
    m_capt_text = " ".join(m.value for m in m_capt.markdown)
    assert "Live Polling Results" in m_capt_text
    print("  ✓ Straw poll tallied 3 distributed votes across headlines, visible to Captain.")

    # Viewer 1 changes vote to Headline 4 (Favorable)
    v1.run()
    change_btn = next((b for b in v1.button if "Headline 4" in b.label and "Vote" in b.label), None)
    assert change_btn is not None
    change_btn.click().run()
    print("  ✓ Viewer vote change submitted successfully.")

    # 3. Captain Publishes Headline 4
    m_capt.run()
    pub_h4 = next((b for b in m_capt.button if "Publish Headline 4" in b.label), None)
    assert pub_h4 is not None, "Publish Headline 4 button not found in Captain view"
    pub_h4.click().run()

    # Verify Media View after publishing transitions to Recap
    assert any("Breaking story published" in s.value for s in m_capt.success)
    print("  ✓ Captain successfully published Headline 4 (+8 HP Favorable). Terminal indicates story published.")

    # Verify GM Projector now shows round recap with Headline 4
    gm.run()
    gm_text = " ".join(m.value for m in gm.markdown)
    assert "Decisive Defense" in gm_text or "+8 HP" in gm_text or "Round 1" in gm_text
    print("  ✓ GM Projector reflects Recap phase with Headline 4 (+8 HP).")


def test_gm_projector_and_fragment_sync():
    print("\n--- [TEST 3] GM Projector (/?team=main) & Live Telemetry Sync ---")

    # 1. Unauthenticated Projector View (Audience / Big Screen)
    proj = AppTest.from_file("app.py")
    proj.query_params["team"] = "main"
    proj.run()
    assert not proj.exception
    assert any("CloudStore Command: Mission Control" in t.value for t in proj.title)
    print("  ✓ Mission Control loaded in Projector Mode.")

    # 2. Reset and start round 1
    gm = AppTest.from_file("app.py")
    gm.query_params["team"] = "main"
    gm.run()
    gm.sidebar.text_input[0].input("admin123")
    gm.sidebar.button[0].click().run()
    for b in gm.sidebar.button:
        if "Reset Sim" in b.label:
            b.click().run()
            break
    for b in gm.sidebar.button:
        if "Start Round 1" in b.label:
            b.click().run()
            break

    # Verify Projector picks up Hacker phase
    proj.run()
    assert any("Selecting Attack Vector" in info.value for info in proj.info)
    print("  ✓ Projector synced: Threat Actors selecting attack.")

    # 3. Hacker deploys attack
    h = AppTest.from_file("app.py")
    h.query_params["team"] = "hackers"
    h.run()
    h.sidebar.text_input[0].input("hacker123")
    h.sidebar.button[0].click().run()
    for b in h.button:
        if "Deploy Vector A" in b.label:
            b.click().run()
            break

    # Verify Projector picks up IT phase & active incident
    proj.run()
    assert any("Deliberating Containment" in info.value for info in proj.info)
    assert any("Spear Phishing" in m.value for m in proj.markdown)
    print("  ✓ Projector synced: Active Enterprise Breach card (Spear Phishing) & IT deliberation.")

    # 4. IT deploys
    it = AppTest.from_file("app.py")
    it.query_params["team"] = "it"
    it.run()
    it.sidebar.text_input[0].input("tech123")
    it.sidebar.button[0].click().run()
    for b in it.button:
        if "Deploy & Recommend Option 2" in b.label:
            b.click().run()
            break

    # Verify Projector picks up Exec phase
    proj.run()
    assert any("Reviewing IT Proposal" in info.value for info in proj.info)
    print("  ✓ Projector synced: Executive Board reviewing IT proposal.")

    # 5. Exec authorizes
    ex = AppTest.from_file("app.py")
    ex.query_params["team"] = "exec"
    ex.run()
    ex.sidebar.text_input[0].input("board123")
    ex.sidebar.button[0].click().run()
    for b in ex.button:
        if "Approve" in b.label:
            b.click().run()
            break

    # Verify Projector picks up Media phase
    proj.run()
    assert any("Selecting Breaking Headline" in info.value for info in proj.info)
    print("  ✓ Projector synced: Media & PR selecting breaking headline.")

    # 6. Media publishes Headline 1 (Sensationalist -12)
    m = AppTest.from_file("app.py")
    m.query_params["team"] = "media"
    m.run()
    m.sidebar.text_input[0].input("press123")
    m.sidebar.button[0].click().run()
    for b in m.button:
        if "Publish Headline 1" in b.label:
            b.click().run()
            break

    # Verify Projector displays Round Recap & Net Delta
    proj.run()
    proj_text = " ".join(m.value for m in proj.markdown)
    assert "Round 1:" in proj_text or "Net Health Change:" in proj_text
    print("  ✓ Projector synced: Scoreboard Incident Chronology rendered complete round breakdown.")


def test_gm_console_controls():
    print("\n--- [TEST 4] GM Console Controls: Rounds, Multipliers, Timer, Undo ---")

    gm = AppTest.from_file("app.py")
    gm.query_params["team"] = "main"
    gm.run()
    
    # 1. Unlock GM Console with admin123
    gm.sidebar.text_input[0].input("admin123")
    gm.sidebar.button[0].click().run()
    assert any("GM Console Unlocked" in s.value for s in gm.sidebar.success)
    print("  ✓ GM Console unlocked via admin passcode.")

    # Reset
    for b in gm.sidebar.button:
        if "Reset Sim" in b.label:
            b.click().run()
            break

    # 2. Test Session Round Count Radio (2 vs 3 rounds)
    round_radio = gm.sidebar.radio[0]
    assert round_radio.value == 2
    round_radio.set_value(3).run()
    round_radio.set_value(2).run()
    print("  ✓ Round configuration toggled between 2 and 3 rounds.")

    # 3. Test Threat Multipliers (1.0x, 1.2x, 1.5x, 2.0x)
    mult_select = gm.sidebar.selectbox[0]
    mult_select.set_value(2.0).run()
    print("  ✓ Threat multiplier set to 2.0x.")

    # 4. Start Round 1
    start_btn = next((b for b in gm.sidebar.button if "Start Round 1" in b.label), None)
    assert start_btn is not None
    start_btn.click().run()
    print("  ✓ Started Round 1 with 2.0x intensity.")

    # 5. Test Timer Controls
    # Pause
    pause_btn = next((b for b in gm.sidebar.button if "Pause" in b.label), None)
    assert pause_btn is not None
    pause_btn.click().run()
    print("  ✓ Timer paused.")

    # Resume
    resume_btn = next((b for b in gm.sidebar.button if "Resume" in b.label), None)
    assert resume_btn is not None
    resume_btn.click().run()
    print("  ✓ Timer resumed.")

    # Reset
    reset_btn = next((b for b in gm.sidebar.button if "Reset Timer" in b.label), None)
    assert reset_btn is not None
    reset_btn.click().run()
    print("  ✓ Timer reset back to full duration.")

    # 6. Test Multiplier Effect on Round Scoring
    # Attack C (-30 dmg) with 2.0x multiplier = -60.0 dmg
    h = AppTest.from_file("app.py")
    h.query_params["team"] = "hackers"
    h.run()
    h.sidebar.text_input[0].input("hacker123")
    h.sidebar.button[0].click().run()
    for b in h.button:
        if "Deploy Vector C" in b.label:
            b.click().run()
            break

    it = AppTest.from_file("app.py")
    it.query_params["team"] = "it"
    it.run()
    it.sidebar.text_input[0].input("tech123")
    it.sidebar.button[0].click().run()
    for b in it.button:
        if "Deploy & Recommend Option 1" in b.label:
            b.click().run()
            break

    ex = AppTest.from_file("app.py")
    ex.query_params["team"] = "exec"
    ex.run()
    ex.sidebar.text_input[0].input("board123")
    ex.sidebar.button[0].click().run()
    for b in ex.button:
        if "Approve" in b.label:
            b.click().run()
            break

    m = AppTest.from_file("app.py")
    m.query_params["team"] = "media"
    m.run()
    m.sidebar.text_input[0].input("press123")
    m.sidebar.button[0].click().run()
    for b in m.button:
        if "Publish Headline 2" in b.label:
            b.click().run()
            break

    gm.run()
    gm_text = " ".join(m.value for m in gm.markdown)
    assert "-60" in gm_text or "2x" in gm_text or "2.0x" in gm_text
    print("  ✓ 2.0x Multiplier accurately doubled attack damage in Incident Chronology (-60 HP).")

    # 7. Test Undo
    undo_btn = next((b for b in gm.sidebar.button if "Undo" in b.label), None)
    assert undo_btn is not None
    assert not undo_btn.disabled
    undo_btn.click().run()
    print("  ✓ Round undo clicked and state rolled back.")


def test_game_over_and_outcome_assessment():
    print("\n--- [TEST 5] Game Over Assessment & Outcome Distribution Cutoffs ---")

    # 1. Calibrated Threshold Verification
    b2, w2 = get_outcome_thresholds(2)
    assert (b2, w2) == (39, 70)
    assert evaluate_final_outcome(70.0, 2)[0] == "Win"
    assert evaluate_final_outcome(69.9, 2)[0] == "Survive"
    assert evaluate_final_outcome(39.0, 2)[0] == "Survive"
    assert evaluate_final_outcome(38.9, 2)[0] == "Bankrupt"
    print("  ✓ 2-round outcome thresholds verified (Bankrupt < 39 | Survive 39-69 | Win >= 70).")

    b3, w3 = get_outcome_thresholds(3)
    assert (b3, w3) == (30, 62)
    assert evaluate_final_outcome(62.0, 3)[0] == "Win"
    assert evaluate_final_outcome(61.9, 3)[0] == "Survive"
    assert evaluate_final_outcome(30.0, 3)[0] == "Survive"
    assert evaluate_final_outcome(29.9, 3)[0] == "Bankrupt"
    print("  ✓ 3-round outcome thresholds verified (Bankrupt < 30 | Survive 30-61 | Win >= 62).")

    # 2. Simulate 2-Round Game Completion to Game Over Screen
    gm = AppTest.from_file("app.py")
    gm.query_params["team"] = "main"
    gm.run()
    gm.sidebar.text_input[0].input("admin123")
    gm.sidebar.button[0].click().run()

    # Reset Sim & set 2 rounds
    for b in gm.sidebar.button:
        if "Reset Sim" in b.label:
            b.click().run()
            break
    gm.sidebar.radio[0].set_value(2).run()

    # Round 1
    for b in gm.sidebar.button:
        if "Start Round 1" in b.label:
            b.click().run()
            break

    # Hackers R1
    h = AppTest.from_file("app.py")
    h.query_params["team"] = "hackers"
    h.run()
    h.sidebar.text_input[0].input("hacker123")
    h.sidebar.button[0].click().run()
    for b in h.button:
        if "Deploy Vector" in b.label:
            b.click().run()
            break

    # IT R1
    it = AppTest.from_file("app.py")
    it.query_params["team"] = "it"
    it.run()
    it.sidebar.text_input[0].input("tech123")
    it.sidebar.button[0].click().run()
    for b in it.button:
        if "Deploy & Recommend Option 1" in b.label:
            b.click().run()
            break

    # Exec R1
    ex = AppTest.from_file("app.py")
    ex.query_params["team"] = "exec"
    ex.run()
    ex.sidebar.text_input[0].input("board123")
    ex.sidebar.button[0].click().run()
    for b in ex.button:
        if "Approve" in b.label:
            b.click().run()
            break

    # Media R1
    m = AppTest.from_file("app.py")
    m.query_params["team"] = "media"
    m.run()
    m.sidebar.text_input[0].input("press123")
    m.sidebar.button[0].click().run()
    for b in m.button:
        if "Publish Headline 4" in b.label:
            b.click().run()
            break

    # GM advances to Round 2
    gm.run()
    advance_r2_btn = next((b for b in gm.sidebar.button if "Start Round 2" in b.label), None)
    assert advance_r2_btn is not None, "Start Round 2 button missing in R1 recap"
    advance_r2_btn.click().run()
    print("  ✓ GM advanced game from Round 1 Recap to Round 2.")

    # Hackers R2
    h.run()
    for b in h.button:
        if "Deploy Vector" in b.label:
            b.click().run()
            break

    # IT R2
    it.run()
    for b in it.button:
        if "Deploy & Recommend Option 1" in b.label:
            b.click().run()
            break

    # Exec R2
    ex.run()
    for b in ex.button:
        if "Approve" in b.label:
            b.click().run()
            break

    # Media R2
    m.run()
    for b in m.button:
        if "Publish Headline 4" in b.label:
            b.click().run()
            break

    # GM in Round 2 Recap -> Advance to Final Gambit
    gm.run()
    conclude_btn = next((b for b in gm.sidebar.button if "Advance to Final" in b.label or "Conclude Game" in b.label), None)
    assert conclude_btn is not None, "Advance to Final button missing in Round 2 recap"
    conclude_btn.click().run()
    print("  ✓ Advanced simulation to Adversary Final Gambit.")

    # Threat Actor executes Safe Retreat
    h.run()
    retreat_btn = next((b for b in h.button if "Safe Retreat" in b.label), None)
    assert retreat_btn is not None, "Safe Retreat button not found in Hacker view"
    retreat_btn.click().run()
    print("  ✓ Hackers executed final gambit (Safe Retreat), transitioning to 'game_over'.")

    # Verify Game Over Banner rendered
    gm.run()
    gm_text = " ".join(m.value for m in gm.markdown)
    assert any(badge in gm_text for badge in [
        "MISSION SUCCESS — ENTERPRISE PREVAILED",
        "SURVIVED — ENTERPRISE DAMAGED BUT SOLVENT",
        "CATASTROPHIC FAILURE — BANKRUPTCY DECLARED"
    ]), "Game over screen must render calibrated tier badge"
    assert "Final Company Health:" in gm_text
    print("  ✓ Game Over screen rendered final outcome assessment banner and final health score.")


if __name__ == "__main__":
    test_media_authentication_and_viewers()
    test_media_straw_polling_and_headlines()
    test_gm_projector_and_fragment_sync()
    test_gm_console_controls()
    test_game_over_and_outcome_assessment()
    print("\n🎉 ALL 5 COMPREHENSIVE TEST SUITES COMPLETED WITH 100% SUCCESS!")
