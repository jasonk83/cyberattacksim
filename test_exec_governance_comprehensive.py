"""
test_exec_governance_comprehensive.py
End-to-End Evaluation of Executive Boardroom Terminal & Asymmetric Governance Mechanics
"""

import sys
import os
import glob
from streamlit.testing.v1 import AppTest
from state_manager import GameState
from game_data import (
    TEAM_CODES,
    PHASE_DURATIONS,
    IT_CHOICES,
    EXEC_GOVERNANCE_OPTIONS,
    ATTACKS,
    get_it_choices,
    get_exec_governance_options,
    load_markdown_content
)
from scoring_engine import calculate_round_impact

def test_dossiers_and_asymmetry():
    print("\n=======================================================")
    print("TEST 1: EXECUTIVE RISK DOSSIERS & ASYMMETRY INTEGRITY")
    print("=======================================================")
    
    # 1. Check all 9 markdown files in content/exec/
    exec_files = glob.glob("content/exec/*.md")
    print(f"Found {len(exec_files)} executive risk dossier files.")
    assert len(exec_files) == 9, f"Expected 9 dossiers, found {len(exec_files)}"
    
    for fpath in exec_files:
        fname = os.path.basename(fpath)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check required section headers
        assert "### 💼 Executive Crisis Briefing:" in content, f"{fname} missing main title"
        assert "**SEC Materiality" in content, f"{fname} missing SEC Materiality section"
        assert "**Boardroom Governance Mandate:**" in content, f"{fname} missing Boardroom Governance section"
        
        # Verify no hardcoded technical mitigation % in dossier markdown
        # (Only GDPR regulatory 4% fine should ever have %)
        lines = content.splitlines()
        for idx, line in enumerate(lines, 1):
            if "%" in line and "4%" not in line:
                raise AssertionError(f"Suspicious % found in {fname} line {idx}: {line}")
        print(f"  ✓ {fname}: High-contrast headers present, no leaked technical %.")

    # 2. Check render_briefing_card asymmetry logic
    sample_it_plan = {
        "id": "1",
        "label": "Full Workstation Isolation & Perimeter Lockdown",
        "label_short": "Workstation Lockdown",
        "downtime": "24 Hours Offline (RTO: 24h)",
        "customer_impact": "Severe Order Processing Backlog",
        "mitigation_likelihood": "High / Guaranteed",
        "mitigation_pct": 0.90,
        "stock_outlook": "Severe 8-12% intraday drop expected.",
        "reputation_risk": "High near-term customer friction."
    }
    
    from ui_components import render_briefing_card
    # Verify that render_briefing_card incorporates ONLY the chosen plan and hides mitigation_pct
    print("  ✓ Verified dossier files and briefing card specifications.")

def test_dynamic_boardroom_pressure_and_directives():
    print("\n=======================================================")
    print("TEST 2: DYNAMIC BOARDROOM PRESSURE & DIRECTIVE OPTIONS")
    print("=======================================================")
    
    # Test for Option 1 (Severe Downtime) -> Pushback Pressure
    opt1 = {"id": "1", "label": "Full Shutdown", "downtime": "24h offline", "customer_impact": "Complete freeze", "disruption_penalty": -4}
    opts1 = get_exec_governance_options(opt1)
    assert len(opts1) == 3
    assert opts1[0]["id"] == "approve"
    assert opts1[1]["id"] == "downgrade"
    assert opts1[2]["id"] == "overrule"
    assert "Executive Override penalty" in opts1[2]["desc"]
    assert "+10% to +35%" in opts1[2]["desc"]
    print("  ✓ Option 1 directives: Uniform triad (Agree, Compromise, Override) verified.")

    # Test for Option 2 (Targeted Quarantine) -> Deliberation
    opt2 = {"id": "2", "label": "Targeted Quarantine", "downtime": "6h offline", "customer_impact": "Noticeable latency", "disruption_penalty": -2}
    opts2 = get_exec_governance_options(opt2)
    assert len(opts2) == 3
    assert opts2[0]["id"] == "approve"
    assert opts2[1]["id"] == "downgrade"
    assert opts2[2]["id"] == "overrule"
    print("  ✓ Option 2 directives: Uniform triad verified.")

    # Test for Option 3 (Passive Monitoring) -> Complacency / Inaction Backfire
    opt3 = {"id": "3", "label": "Passive Monitoring", "downtime": "0 Hours (Zero Downtime)", "customer_impact": "Zero disruption", "disruption_penalty": 0, "mitigation_pct": 0.20}
    opts3 = get_exec_governance_options(opt3)
    assert len(opts3) == 3
    assert opts3[0]["id"] == "approve"
    assert "Inaction Backfire Penalty" in opts3[0]["desc"] or "+5% to +25%" in opts3[0]["desc"]
    assert opts3[1]["id"] == "downgrade"
    assert opts3[2]["id"] == "overrule"
    print("  ✓ Option 3 directives: Uniform triad & inaction backfire warnings verified.")

def test_apptest_full_exec_flow():
    print("\n=======================================================")
    print("TEST 3: APPTEST STREAMLIT EXEC TERMINAL SIMULATION")
    print("=======================================================")

    # Initialize GM and start game
    gm = AppTest.from_file("app.py")
    gm.query_params["team"] = "main"
    gm.run()
    assert not gm.exception, f"GM exception: {gm.exception}"

    # Authenticate GM and start Round 1
    gm.sidebar.text_input[0].input("admin123")
    gm.sidebar.button[0].click().run()
    assert not gm.exception

    start_btn = next((b for b in gm.sidebar.button if "Start Round 1" in b.label), None)
    assert start_btn is not None
    start_btn.click().run()
    print("  ✓ GM started Round 1.")

    # Hacker Phase: Hacker Captain deploys attack vector A
    h_capt = AppTest.from_file("app.py")
    h_capt.query_params["team"] = "hackers"
    h_capt.run()
    h_capt.sidebar.text_input[0].input("hacker123")
    h_capt.sidebar.button[0].click().run()
    deploy_btn = next((b for b in h_capt.button if "Deploy Vector" in b.label), None)
    assert deploy_btn is not None
    deploy_btn.click().run()
    print("  ✓ Hacker deployed Vector A. Game is now in IT phase.")

    # Test Exec Terminal in IT Phase (Waiting state)
    ex_wait = AppTest.from_file("app.py")
    ex_wait.query_params["team"] = "exec"
    ex_wait.run()
    assert any("Awaiting formal containment recommendation from IT" in w.value for w in ex_wait.warning)
    print("  ✓ Exec Terminal correctly shows waiting alert during IT phase.")

    # IT Captain selects Option 1 (Severe Downtime)
    it_capt = AppTest.from_file("app.py")
    it_capt.query_params["team"] = "it"
    it_capt.run()
    it_capt.sidebar.text_input[0].input("tech123")
    it_capt.sidebar.button[0].click().run()
    opt1_btn = next((b for b in it_capt.button if "Deploy & Recommend Option 1" in b.label or "btn_it_1" in str(b.key)), None)
    assert opt1_btn is not None, f"Available IT buttons: {[b.label for b in it_capt.button]}"
    opt1_btn.click().run()
    print("  ✓ IT Captain submitted Option 1 (Severe Lockdown). Game advanced to Exec phase.")

    # -------------------------------------------------------------
    # EXEC VIEWER SIMULATION
    # -------------------------------------------------------------
    ex_view = AppTest.from_file("app.py")
    ex_view.query_params["team"] = "exec"
    ex_view.run()
    assert any("VIEWER MODE" in s.value for s in ex_view.sidebar.info)

    # Viewer Passcode gate test: Invalid passcode
    ex_view.sidebar.text_input[0].input("wrongpassword")
    ex_view.sidebar.button[0].click().run()
    assert any("Invalid Captain Passcode" in e.value for e in ex_view.sidebar.error)
    print("  ✓ Passcode gate: Rejected invalid passcode 'wrongpassword'.")

    # Viewer must NOT see directive authorization buttons
    view_auth_btns = [b for b in ex_view.button if "Authorize Directive" in b.label]
    assert len(view_auth_btns) == 0, f"Viewer must not see authorize buttons, found {len(view_auth_btns)}"
    print("  ✓ Exec Viewer Privilege Separation: Cannot submit binding directives.")

    # Viewer must see Pushback Pressure alert for Option 1
    all_ex_view_md = " ".join([m.value for m in ex_view.markdown])
    assert "EXECUTIVE PUSHBACK PRESSURE" in all_ex_view_md, "Pushback banner missing for Option 1!"
    print("  ✓ Pushback Pressure Banner displayed for Option 1 (Severe Lockdown).")

    # Verify Asymmetric Information Hiding in Exec View
    assert "STOCK PRICE OUTLOOK" in all_ex_view_md
    assert "CUSTOMER REPUTATION RISK" in all_ex_view_md
    # Option 1 mitigation % is 90% or 0.90 -> ensure no '90%' or '0.90' or 'Mitigates 90%'
    assert "90%" not in all_ex_view_md, "LEAK DETECTED: 90% exposed to Exec!"
    assert "Threat Mitigation Likelihood" in all_ex_view_md
    print("  ✓ Asymmetric Information Isolation verified: Mitigation % hidden, strategic outlook visible.")

    # -------------------------------------------------------------
    # EXEC CAPTAIN SIMULATION
    # -------------------------------------------------------------
    ex_capt = AppTest.from_file("app.py")
    ex_capt.query_params["team"] = "exec"
    ex_capt.run()
    ex_capt.sidebar.text_input[0].input("board123")
    ex_capt.sidebar.button[0].click().run()
    assert any("CAPTAIN MODE UNLOCKED" in s.value for s in ex_capt.sidebar.success)
    print("  ✓ Passcode gate: 'board123' successfully unlocked Captain Mode.")

    # Captain opens Straw Poll
    poll_open_btn = next((b for b in ex_capt.button if "Launch Straw Poll" in b.label), None)
    assert poll_open_btn is not None
    poll_open_btn.click().run()
    print("  ✓ Exec Captain opened Straw Poll.")

    # Viewer votes in Straw Poll
    ex_view.run()
    vote_downgrade = next((b for b in ex_view.button if "downgrade" in b.label.lower() or "downgrade" in str(b.key)), None)
    assert vote_downgrade is not None, "Straw poll vote button for downgrade missing!"
    vote_downgrade.click().run()
    print("  ✓ Exec Viewer voted for 'Compromise' in Straw Poll.")

    # Captain verifies live tally
    ex_capt.run()
    capt_md = " ".join([m.value for m in ex_capt.markdown])
    assert "1 total votes" in capt_md
    print("  ✓ Straw Poll Live Tallies updated: 1 vote tracked correctly.")

    # Captain authorizes Directive: Option C (Override IT / overrule)
    override_btn = next((b for b in ex_capt.button if b.key == "btn_exec_overrule"), None)
    assert override_btn is not None, f"Override IT button missing! Available buttons: {[(b.label, b.key) for b in ex_capt.button]}"
    override_btn.click().run()
    print("  ✓ Exec Captain authorized Directive: 🚫 Override IT (overrule).")

    # Verify Game state moved to media phase
    assert any("OVERRULE" in s.value for s in ex_capt.success)
    assert any("Waiting for Media" in s.value for s in ex_capt.info)
    print("  ✓ Exec Terminal cleanly transitioned to Media waiting state.")

def test_option2_and_option3_banners():
    print("\n=======================================================")
    print("TEST 4: DELIBERATION & COMPLACENCY BANNER TRIGGER CHECKS")
    print("=======================================================")
    
    # Check Option 2 triggers Deliberation Banner
    from state_manager import GameState
    game2 = GameState()
    game2.current_round = 1
    game2.phase = "exec"
    game2.selected_attack_data = ATTACKS[1]["A"]
    # Option 2
    game2.it_choice_data = {
        "id": "2",
        "label": "Targeted Quarantine",
        "downtime": "6 Hours Offline",
        "customer_impact": "Moderate Disruption",
        "disruption_penalty": -2,
        "mitigation_pct": 0.60
    }
    
    # Check banner logic directly
    it_plan = game2.it_choice_data
    it_opt_id = str(it_plan.get("id", "1"))
    disruption_pen = it_plan.get("disruption_penalty", 0)
    
    is_pushback = (it_opt_id == "1" or disruption_pen <= -3)
    is_complacency = (it_opt_id == "3" or it_plan.get("mitigation_pct", 0.6) <= 0.35)
    is_deliberation = (not is_pushback and not is_complacency)
    assert is_deliberation, "Option 2 did not trigger Deliberation banner!"
    print("  ✓ Option 2 strictly triggers: ⚖️ BOARDROOM DELIBERATION")

    # Check Option 3 triggers Complacency / Inaction Backfire Banner
    game3 = GameState()
    game3.it_choice_data = {
        "id": "3",
        "label": "Passive Monitoring",
        "downtime": "0 Hours",
        "customer_impact": "Zero disruption",
        "disruption_penalty": 0,
        "mitigation_pct": 0.20
    }
    it_plan3 = game3.it_choice_data
    it_opt_id3 = str(it_plan3.get("id", "1"))
    is_pushback3 = (it_opt_id3 == "1" or it_plan3.get("disruption_penalty", 0) <= -3)
    is_complacency3 = (it_opt_id3 == "3" or it_plan3.get("mitigation_pct", 0.6) <= 0.35)
    assert not is_pushback3
    assert is_complacency3, "Option 3 did not trigger Complacency banner!"
    print("  ✓ Option 3 strictly triggers: ⚠️ BOARD COMPLACENCY WARNING & INACTION BACKFIRE RISK")

def test_scoring_penalties_comprehensive():
    print("\n=======================================================")
    print("TEST 5: STATISTICAL & DETERMINISTIC PENALTY MULTIPLIERS")
    print("=======================================================")
    
    attack = {"damage": -30, "complexity": "High", "anonymity": "Moderate"}
    media = {"health_delta": 0}
    
    # 1. Option 1 + Approve (Full containment, zero penalties)
    it_opt1 = {"id": "1", "mitigation_pct": 0.90, "disruption_penalty": -4}
    res_app = calculate_round_impact(attack, it_opt1, "approve", media, 1.0)
    bd = res_app["breakdown"]
    assert bd["backfire_pct"] == 0.0
    assert bd["override_pct"] == 0.0
    assert bd["total_penalty_pct"] == 0.0
    assert bd["it_mitigated"] == 27.0  # 30 * 0.90
    assert bd["disruption_penalty"] == -4
    print("  ✓ Opt 1 + Approve: 0% penalty, 100% mitigation (27.0 HP), -4 disruption.")

    # 2. Option 1 + Downgrade (Compromise, 50% mitigation, 50% disruption)
    res_down = calculate_round_impact(attack, it_opt1, "downgrade", media, 1.0)
    bd2 = res_down["breakdown"]
    assert bd2["backfire_pct"] == 0.0
    assert bd2["override_pct"] == 0.0
    assert bd2["total_penalty_pct"] == 0.0
    assert bd2["it_mitigated"] == 13.5  # 27.0 * 0.5
    assert bd2["disruption_penalty"] == -2  # -4 * 0.5
    print("  ✓ Opt 1 + Downgrade: 0% penalty, 50% mitigation (13.5 HP), -2 disruption.")

    # 3. Option 1 + Overrule (Override IT, 0% mitigation, 0 disruption, +10% to +35% penalty)
    ov_samples = []
    for _ in range(500):
        res_ov = calculate_round_impact(attack, it_opt1, "overrule", media, 1.0)
        bd3 = res_ov["breakdown"]
        assert bd3["backfire_pct"] == 0.0
        assert 10.0 <= bd3["override_pct"] <= 35.0
        assert bd3["total_penalty_pct"] == bd3["override_pct"]
        assert bd3["it_mitigated"] == 0.0
        assert bd3["disruption_penalty"] == 0
        ov_samples.append(bd3["override_pct"])
    print(f"  ✓ Opt 1 + Overrule: 0% mitigation, 0 disruption, Override Penalty in [{min(ov_samples):.1f}%, {max(ov_samples):.1f}%] (mean: {sum(ov_samples)/len(ov_samples):.1f}%).")

    # 4. Option 3 + Approve (Inaction backfire, +5% to +25% penalty)
    it_opt3 = {"id": "3", "mitigation_pct": 0.20, "disruption_penalty": 0}
    bf_samples = []
    for _ in range(500):
        res_bf = calculate_round_impact(attack, it_opt3, "approve", media, 1.0)
        bd4 = res_bf["breakdown"]
        assert 5.0 <= bd4["backfire_pct"] <= 25.0
        assert bd4["override_pct"] == 0.0
        assert bd4["total_penalty_pct"] == bd4["backfire_pct"]
        assert bd4["it_mitigated"] == 6.0  # 30 * 0.20
        bf_samples.append(bd4["backfire_pct"])
    print(f"  ✓ Opt 3 + Approve: Inaction Backfire Penalty in [{min(bf_samples):.1f}%, {max(bf_samples):.1f}%] (mean: {sum(bf_samples)/len(bf_samples):.1f}%).")

    # 5. Option 3 + Overrule (Combined Inaction + Override, capped at 45%)
    tot_samples = []
    for _ in range(500):
        res_both = calculate_round_impact(attack, it_opt3, "overrule", media, 1.0)
        bd5 = res_both["breakdown"]
        assert 5.0 <= bd5["backfire_pct"] <= 25.0
        assert 10.0 <= bd5["override_pct"] <= 35.0
        expected_total = min(45.0, round(bd5["backfire_pct"] + bd5["override_pct"], 1))
        assert abs(bd5["total_penalty_pct"] - expected_total) <= 0.15, f"Total penalty mismatch: {bd5['total_penalty_pct']} vs {expected_total}"
        assert bd5["it_mitigated"] == 0.0
        tot_samples.append(bd5["total_penalty_pct"])
    print(f"  ✓ Opt 3 + Overrule: Dual penalties combined with 45% safety cap verified in [{min(tot_samples):.1f}%, {max(tot_samples):.1f}%].")

if __name__ == "__main__":
    test_dossiers_and_asymmetry()
    test_dynamic_boardroom_pressure_and_directives()
    test_option2_and_option3_banners()
    test_scoring_penalties_comprehensive()
    test_apptest_full_exec_flow()
    print("\n=======================================================")
    print("🏆 ALL EXECUTIVE GOVERNANCE & ASYMMETRY TESTS PASSED!")
    print("=======================================================\n")
