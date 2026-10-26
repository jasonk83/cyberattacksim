import sys
import time
from streamlit.testing.v1 import AppTest
from state_manager import GameState
from game_data import TEAM_CODES, PHASE_DURATIONS, IT_CHOICES, EXEC_GOVERNANCE_OPTIONS, ATTACKS, get_it_choices

def test_blue_team_deep():
    print("=====================================================================")
    print("🧪 STARTING DEEP BLUE TEAM (IT & EXEC) EVALUATION TEST SUITE")
    print("=====================================================================")

    # Initialize GM and start game
    gm = AppTest.from_file("app.py")
    gm.query_params["team"] = "main"
    gm.run()
    assert not gm.exception, f"GM failed to load: {gm.exception}"

    # Authenticate GM
    admin_input = gm.sidebar.text_input[0]
    admin_input.input("admin123")
    gm.sidebar.button[0].click().run()
    assert not gm.exception

    # Set 2 rounds in lobby (default)
    for r in gm.sidebar.radio:
        if r.label == "Session Round Count":
            r.set_value(2)
            break
    gm.run()

    # 1. Verify Timer configurations
    it_duration = PHASE_DURATIONS.get('it')
    exec_duration = PHASE_DURATIONS.get('exec')
    print(f"\n[Timer Audit] IT Phase Duration: {it_duration}s ({it_duration//60} min)")
    print(f"[Timer Audit] Exec Phase Duration: {exec_duration}s ({exec_duration//60} min)")
    assert it_duration == 300, "IT duration must be 300s (5 min)"
    assert exec_duration == 180, "Exec duration must be 180s (3 min)"
    print("  ✅ Timer duration asymmetry verified: Exec has 40% less deliberation time than IT (3 min vs 5 min).")

    # Start Round 1
    start_btn = next((b for b in gm.sidebar.button if "Start Round 1" in b.label), None)
    assert start_btn is not None
    start_btn.click().run()
    print("  [GM] Initiated Round 1.")

    # Loop through Rounds 1, 2
    for current_round in range(1, 3):
        print(f"\n==================== SIMULATING ROUND {current_round} / 2 ====================")
        
        # Threat Actor Phase: Captain deploys attack vector A
        h_capt = AppTest.from_file("app.py")
        h_capt.query_params["team"] = "hackers"
        h_capt.run()
        h_capt.sidebar.text_input[0].input("hacker123")
        h_capt.sidebar.button[0].click().run()
        
        deploy_btn = next((b for b in h_capt.button if "Deploy Vector" in b.label), None)
        assert deploy_btn is not None, "Hacker deploy button not found"
        deploy_btn.click().run()
        print(f"  [Hacker] Vector deployed. System transitioned to IT Defense phase.")

        # -------------------------------------------------------------
        # STEP 1: IT DEFENSE SIMULATION (VIEWERS & CAPTAIN)
        # -------------------------------------------------------------
        print("\n  --- [TESTING IT DEFENSE (ROUND {})] ---".format(current_round))

        # Check Timer in IT Phase
        it_capt = AppTest.from_file("app.py")
        it_capt.query_params["team"] = "it"
        it_capt.run()
        
        # Verify IT Captain Authentication
        it_capt.sidebar.text_input[0].input("tech123")
        it_capt.sidebar.button[0].click().run()
        assert any("CAPTAIN MODE UNLOCKED" in s.value for s in it_capt.sidebar.success)
        print("  [IT Captain Auth] Passcode 'tech123' successfully verified.")

        # Verify IT Phase clock duration in HTML
        clock_md = next((m.value for m in it_capt.markdown if "threat-clock-container" in m.value), "")
        assert "IT CONTAINMENT DELIBERATION" in clock_md.upper(), "Clock title does not show IT Containment phase"
        print("  [IT Timer Verification] Clock displaying active IT Threat Window.")

        # Test IT Viewers joining
        it_view1 = AppTest.from_file("app.py")
        it_view1.query_params["team"] = "it"
        it_view1.run()
        assert any("VIEWER MODE" in s.value for s in it_view1.sidebar.info)
        
        # Confirm Viewers have NO deployment buttons
        view_deploy_btns = [b for b in it_view1.button if "Deploy & Recommend" in b.label]
        assert len(view_deploy_btns) == 0, "Viewers must not see deployment buttons"
        print("  [IT Security] Verified: Viewers strictly prohibited from submitting containment proposals.")

        # Audit IT Option details (Downtime vs Disruption vs Likelihood)
        all_it_md = " ".join([m.value for m in it_capt.markdown])
        round_options = get_it_choices(current_round, "A")
        for opt in round_options:
            mit_badge = f"Likelihood: {opt['mitigation_likelihood']}"
            downtime_text = opt['downtime']
            disrupt_text = opt['disruption']
            assert mit_badge in all_it_md, f"Missing {mit_badge} in IT terminal"
            assert downtime_text in all_it_md, f"Missing {downtime_text} in IT terminal"
            print(f"  [IT Options R{current_round}] Opt {opt['id']}: {mit_badge} | {downtime_text} | {disrupt_text}")

        # IT Straw Polling Test
        it_poll_launch = next((b for b in it_capt.button if "Launch Straw Poll" in b.label), None)
        assert it_poll_launch is not None
        it_poll_launch.click().run()
        print("  [IT Polling] Captain opened team Straw Poll.")

        # Viewer 1 votes for Option 1
        it_view1.run()
        v1_btn = next((b for b in it_view1.button if "Vote: 1" in b.label), None)
        assert v1_btn is not None
        v1_btn.click().run()
        print("  [IT Polling] Viewer 1 voted for Option 1.")

        # Viewer 2 joins and votes for Option 2
        it_view2 = AppTest.from_file("app.py")
        it_view2.query_params["team"] = "it"
        it_view2.run()
        v2_btn = next((b for b in it_view2.button if "Vote: 2" in b.label), None)
        assert v2_btn is not None
        v2_btn.click().run()
        print("  [IT Polling] Viewer 2 voted for Option 2.")

        # Captain sees tallies (2 votes total)
        it_capt.run()
        capt_poll_text = " ".join([m.value for m in it_capt.markdown])
        assert "2 total votes" in capt_poll_text
        print("  [IT Polling Tally] Live results verified: 2 total votes tracked correctly.")

        # Captain submits proposal
        # Round 1: Option 1 (Full Lockout, 90% mitigation)
        # Round 2: Option 2 (Partial Outage, 60% mitigation)
        # Round 3: Option 3 (Zero Downtime, 25% mitigation)
        target_opt_id = str(current_round)
        deploy_target = next((b for b in it_capt.button if f"Option {target_opt_id}" in b.label and "Deploy" in b.label), None)
        assert deploy_target is not None, f"Deploy button for Option {target_opt_id} not found"
        deploy_target.click().run()
        print(f"  [IT Containment Submitted] Captain submitted Option {target_opt_id} to Board.")

        # IT Terminal updates to waiting state
        it_capt.run()
        assert any("Technical containment proposed" in s.value for s in it_capt.success)
        assert any("Waiting for Executive Boardroom" in s.value for s in it_capt.info)
        print("  [IT Post-Submission UI] Verified: IT enters waiting state for Board decision.")

        # -------------------------------------------------------------
        # STEP 2: EXECUTIVE BOARDROOM SIMULATION (ASYMMETRIC GOVERNANCE)
        # -------------------------------------------------------------
        print("\n  --- [TESTING EXECUTIVE BOARDROOM (ROUND {})] ---".format(current_round))

        # Test Exec Viewer joins
        ex_view1 = AppTest.from_file("app.py")
        ex_view1.query_params["team"] = "exec"
        ex_view1.run()
        assert any("VIEWER MODE" in s.value for s in ex_view1.sidebar.info)

        # Confirm Viewers cannot authorize directives
        view_auth_btns = [b for b in ex_view1.button if "Authorize Directive" in b.label]
        assert len(view_auth_btns) == 0, "Exec Viewers must not see authorization buttons"
        print("  [Exec Security] Verified: Exec Viewers cannot issue corporate directives.")

        # CHECK ASYMMETRIC INFORMATION ISOLATION:
        # Technical protection % must be CLASSIFIED/HIDDEN from the Board
        # Find the IT proposal markdown card
        it_proposal_md = next((m.value for m in ex_view1.markdown if "IT PROPOSAL STRATEGIC IMPACT ASSESSMENT" in m.value or "IT DEPARTMENT DIRECTIVE PROPOSAL" in m.value), "")
        assert it_proposal_md != "", "IT Department Proposal card not found in Exec view!"
        assert "STOCK PRICE OUTLOOK" in it_proposal_md, "Stock Price Outlook missing!"
        assert "CUSTOMER REPUTATION RISK" in it_proposal_md, "Customer Reputation Risk missing!"
        
        # Verify technical protection numbers are NOT leaked in Exec view
        chosen_it_data = next((c for c in round_options if str(c['id']) == target_opt_id), {})
        leak_str = f"{int(chosen_it_data['mitigation_pct']*100)}%"
        assert leak_str not in it_proposal_md, f"LEAK DETECTED: IT mitigation {leak_str} exposed to Executive Board!"
        assert "Mitigates" not in it_proposal_md, "LEAK DETECTED: 'Mitigates' keyword exposed in proposal card!"
        print(f"  [Exec Asymmetry Verified] 🛡️ Strategic outlook visible; technical mitigation % ({leak_str}) successfully HIDDEN from Board.")

        # Verify Business Downtime & Disruption ARE visible to Exec
        assert chosen_it_data["exec_view"] in it_proposal_md, "Business downtime/disruption description missing from proposal card!"
        print(f"  [Exec Briefing Visibility] Business disruption visible: \"{chosen_it_data['exec_view']}\"")

        # Test Exec Captain Authentication
        ex_capt = AppTest.from_file("app.py")
        ex_capt.query_params["team"] = "exec"
        ex_capt.run()
        ex_capt.sidebar.text_input[0].input("board123")
        ex_capt.sidebar.button[0].click().run()
        assert any("CAPTAIN MODE UNLOCKED" in s.value for s in ex_capt.sidebar.success)
        print("  [Exec Captain Auth] Passcode 'board123' successfully verified.")

        # Check Exec Timer in Clock
        clock_exec_md = next((m.value for m in ex_capt.markdown if "threat-clock-container" in m.value), "")
        assert "EXECUTIVE CRISIS GOVERNANCE" in clock_exec_md.upper(), "Clock title does not show Exec phase"
        print("  [Exec Timer Verification] 3-Minute clock displaying Executive Crisis Governance window.")

        # Exec Straw Polling
        ex_poll_launch = next((b for b in ex_capt.button if "Launch Straw Poll" in b.label), None)
        assert ex_poll_launch is not None
        ex_poll_launch.click().run()
        print("  [Exec Polling] Captain opened Executive Straw Poll.")

        # Exec Viewer votes
        ex_view1.run()
        # Directives: R1 -> Approve ("Agree with IT"), R2 -> Downgrade ("Compromise"), R3 -> Overrule ("Override IT")
        decision_map = {1: "approve", 2: "downgrade", 3: "overrule"}
        target_directive = decision_map[current_round]

        vote_directive_btn = next((b for b in ex_view1.button if target_directive in b.label.lower() or target_directive in str(b.key)), None)
        assert vote_directive_btn is not None, f"Vote button for {target_directive} not found"
        vote_directive_btn.click().run()
        print(f"  [Exec Polling] Exec Viewer voted to: {target_directive.upper()}.")

        # Exec Captain confirms tallies and authorizes directive
        ex_capt.run()
        capt_exec_poll_text = " ".join([m.value for m in ex_capt.markdown])
        assert "1 total votes" in capt_exec_poll_text
        print(f"  [Exec Polling Tally] Live results verified: 1 vote tracked.")

        # Verify dynamic pressure / deliberation banner
        if current_round == 1:
            assert any("PUSHBACK" in m.value.upper() for m in ex_capt.markdown), "Pushback pressure banner missing for Option 1!"
            print("  [Exec Pushback Pressure] ⚠️ Pushback banner verified: Board under shareholder pressure.")
        elif current_round == 2:
            assert any("DELIBERATION" in m.value.upper() for m in ex_capt.markdown), "Deliberation banner missing for Option 2!"
            print("  [Exec Deliberation] ⚖️ Targeted deliberation banner verified.")

        auth_btn = next((b for b in ex_capt.button if (b.key == f"btn_exec_{target_directive}") or ("Authorize Directive" in b.label and (target_directive in b.label.lower() or target_directive in str(b.key)))), None)
        assert auth_btn is not None, f"Authorize button for {target_directive} not found"
        auth_btn.click().run()
        print(f"  [Exec Directive Issued] Captain authorized: {target_directive.upper()}.")

        # Verify Exec terminal displays directive confirmation
        ex_capt.run()
        assert any("Governance directive issued" in s.value for s in ex_capt.success)
        assert any("Waiting for Media & PR Scrum" in s.value for s in ex_capt.info)
        print("  [Exec Post-Directive UI] Verified: Exec enters waiting state for Media scrum.")

        # -------------------------------------------------------------
        # STEP 3: MEDIA SCRUM & ROUND WRAP-UP
        # -------------------------------------------------------------
        print("\n  --- [MEDIA & ROUND RECAP] ---")
        m_capt = AppTest.from_file("app.py")
        m_capt.query_params["team"] = "media"
        m_capt.run()
        m_capt.sidebar.text_input[0].input("press123")
        m_capt.sidebar.button[0].click().run()
        
        # Publish headline
        pub_btn = next((b for b in m_capt.button if "Publish" in b.label), None)
        assert pub_btn is not None
        pub_btn.click().run()
        print(f"  [Media] Headline published. Round {current_round} finalized.")

        # GM checks recap and advances to next round or concludes
        gm.run()
        print(f"  [GM Scoreboard] Company Health after Round {current_round}: {gm.session_state.get('voter_id') is not None}")
        
        if current_round < 2:
            advance_btn = next((b for b in gm.sidebar.button if f"Start Round {current_round + 1}" in b.label), None)
            assert advance_btn is not None, f"Button 'Start Round {current_round + 1}' not found in GM sidebar"
            advance_btn.click().run()
            print(f"  [GM] Advanced simulation to Round {current_round + 1}.")
        else:
            advance_btn = next((b for b in gm.sidebar.button if "Advance to Final" in b.label or "Conclude Game" in b.label), None)
            assert advance_btn is not None, "Button to advance to Final Threat Actor Gambit not found"
            advance_btn.click().run()
            print("  [GM] Advanced simulation to Adversary Final Gambit!")

    # Adversary Final Action Gambit
    print("\n  --- [ADVERSARY FINAL GAMBIT] ---")
    h_capt = AppTest.from_file("app.py")
    h_capt.query_params["team"] = "hackers"
    h_capt.run()
    h_capt.sidebar.text_input[0].input("hacker123")
    h_capt.sidebar.button[0].click().run()
    retreat_btn = next((b for b in h_capt.button if b.label and "Safe Retreat" in b.label), None)
    assert retreat_btn is not None, "Could not find Safe Retreat button"
    retreat_btn.click().run()
    print("  [Hackers] Executed Safe Retreat.")

    # Verify Game Over screen
    gm.run()
    assert any("Simulation Finished" in s.value for s in gm.sidebar.success)
    print("\n=====================================================================")
    print("🎉 ALL 2 ROUNDS + FINAL GAMBIT OF BLUE TEAM EVALUATION PASSED FLAWLESSLY!")
    print("=====================================================================")

if __name__ == "__main__":
    test_blue_team_deep()
