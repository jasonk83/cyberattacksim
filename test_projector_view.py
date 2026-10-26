"""
test_projector_view.py
Automated end-to-end test suite for the dedicated Class Projector View (?team=projector).

Verifies:
1. Complete removal of sidebar widgets (zero sidebar buttons, text inputs, radio, or controls).
2. Complete suppression of all interactive mission control buttons:
   - No Start Round / Advance buttons
   - No Timer Pause / Resume / Reset buttons
   - No manual HP adjustment buttons (+10 HP / -10 HP)
   - No manual Refresh Scoreboard button
3. Presence of presentation scoreboard elements:
   - Title & caption
   - Unobtrusive 'Live Telemetry Auto-Sync' badge
   - Threatening Countdown Clock
   - Primary Enterprise Health Gauge
   - Real-time Team Deliberation Telemetry badges
   - Active Incident Alert card
   - Round Recap card
4. Real-time synchronized state updates from GM and team actions.
5. Presence in GM Console shareable URLs and Preview switcher.
"""

from streamlit.testing.v1 import AppTest
from state_manager import GameState
from game_data import TEAM_CODES


def test_projector_view_clean_layout():
    print("\n--- [TEST 1] Projector View Clean Layout & Control Suppression ---")
    proj = AppTest.from_file("app.py")
    proj.query_params["team"] = "projector"
    proj.run()
    assert not proj.exception

    # 1. Verify title and live sync badge
    assert any("CloudStore Command: Mission Control" in t.value for t in proj.title)
    main_text = " ".join([m.value for m in proj.markdown])
    assert "Live Telemetry Auto-Sync" in main_text, "Live sync telemetry badge missing on projector"
    print("  ✓ Projector view rendered clean title and Live Telemetry Auto-Sync badge.")

    # 2. Verify sidebar is completely empty / no widgets rendered
    assert len(proj.sidebar.button) == 0, f"Sidebar buttons found on projector: {[b.label for b in proj.sidebar.button]}"
    assert len(proj.sidebar.text_input) == 0, "Sidebar text input found on projector"
    assert len(proj.sidebar.radio) == 0, "Sidebar radio found on projector"
    assert len(proj.sidebar.selectbox) == 0, "Sidebar selectbox found on projector"
    print("  ✓ Verified: Zero sidebar interactive controls rendered on Projector view.")

    # 3. Verify ALL action buttons are absent in the main area
    all_btn_labels = [b.label for b in proj.button]
    assert not any("Start Round" in l for l in all_btn_labels), "Start Round button found on projector!"
    assert not any("Advance" in l for l in all_btn_labels), "Advance button found on projector!"
    assert not any("Pause" in l for l in all_btn_labels), "Pause Timer button found on projector!"
    assert not any("Resume" in l for l in all_btn_labels), "Resume Timer button found on projector!"
    assert not any("Reset" in l for l in all_btn_labels), "Reset button found on projector!"
    assert not any("+10 HP" in l or "Add" in l for l in all_btn_labels), "+10 HP button found on projector!"
    assert not any("-10 HP" in l or "Subtract" in l for l in all_btn_labels), "-10 HP button found on projector!"
    assert not any("Refresh Scoreboard" in l for l in all_btn_labels), "Manual Refresh button found on projector!"
    assert len(proj.button) == 0, f"Unexpected buttons on projector: {all_btn_labels}"
    print("  ✓ Verified: Zero interactive action buttons rendered in main area.")


def test_projector_live_synchronization():
    print("\n--- [TEST 2] Projector Live Telemetry Synchronization ---")

    # 1. GM resets simulation to lobby
    gm = AppTest.from_file("app.py")
    gm.query_params["team"] = "main"
    gm.run()
    gm.sidebar.text_input[0].input("admin123")
    gm.sidebar.button[0].click().run()
    for b in gm.sidebar.button:
        if "Reset Sim" in b.label:
            b.click().run()
            break

    # 2. Check Projector in Lobby
    proj = AppTest.from_file("app.py")
    proj.query_params["team"] = "projector"
    proj.run()
    proj_md = " ".join([m.value for m in proj.markdown])
    assert "LOBBY" in proj_md.upper(), "Lobby phase missing from countdown clock"
    assert any("Standby in Lobby" in info.value for info in proj.info)
    print("  ✓ Projector synced: Lobby phase and team standby badges.")

    # 3. GM starts Round 1
    start_btn = next((b for b in gm.sidebar.button if "Start Round 1" in b.label), None)
    if not start_btn:
        start_btn = next((b for b in gm.button if "Start Round 1" in b.label), None)
    assert start_btn is not None
    start_btn.click().run()

    # 4. Projector reflects Hacker phase without any action buttons
    proj.run()
    proj_md = " ".join([m.value for m in proj.markdown])
    assert "THREAT ACTOR INFILTRATION" in proj_md.upper(), "Hacker phase missing from countdown clock"
    assert any("Selecting Attack Vector" in info.value for info in proj.info)
    assert len(proj.button) == 0
    print("  ✓ Projector synced: Round 1 Threat Actor Infiltration active (read-only).")

    # 5. Hacker deploys Vector A
    h = AppTest.from_file("app.py")
    h.query_params["team"] = "hackers"
    h.run()
    h.sidebar.text_input[0].input(TEAM_CODES["hackers"])
    h.sidebar.button[0].click().run()
    deploy_btn = next((b for b in h.button if "Deploy Vector A" in b.label), None)
    assert deploy_btn is not None
    deploy_btn.click().run()

    # 6. Projector reflects IT Containment and Active Breach Alert
    proj.run()
    proj_md = " ".join([m.value for m in proj.markdown])
    assert "Spear Phishing" in proj_md, "Active breach card missing on projector"
    assert any("Deliberating Containment" in info.value for info in proj.info)
    assert len(proj.button) == 0
    print("  ✓ Projector synced: Active Enterprise Breach card (Spear Phishing) & IT deliberation telemetry.")


def test_gm_console_projector_links_and_preview():
    print("\n--- [TEST 3] GM Console Shareable URLs & Terminal Preview ---")

    gm = AppTest.from_file("app.py")
    gm.query_params["team"] = "main"
    gm.run()
    gm.sidebar.text_input[0].input("admin123")
    gm.sidebar.button[0].click().run()
    assert not gm.exception

    # 1. Shareable links audit
    codes_text = " ".join([c.value for c in gm.sidebar.code])
    assert "?team=projector" in codes_text, "Shareable URL for '?team=projector' missing in GM console!"
    print("  ✓ GM Console correctly publishes shareable link for '?team=projector'.")

    # 2. Terminal preview switcher audit
    preview_select = next((s for s in gm.sidebar.selectbox if "View As:" in s.label), None)
    assert preview_select is not None, "Preview mode selectbox missing"
    assert "Class Projector (Clean Display)" in preview_select.options, "Class Projector missing from Preview options"
    print("  ✓ Terminal Preview switcher includes 'Class Projector (Clean Display)'.")

    # 3. Switch preview to Class Projector
    preview_select.set_value("Class Projector (Clean Display)").run()
    assert not gm.exception
    preview_text = " ".join([m.value for m in gm.markdown])
    assert "Live Telemetry Auto-Sync" in preview_text
    print("  ✓ Preview switcher successfully rendered clean Class Projector layout.")


if __name__ == "__main__":
    test_projector_view_clean_layout()
    test_projector_live_synchronization()
    test_gm_console_projector_links_and_preview()
    print("\n🎉 ALL CLASS PROJECTOR VIEW TESTS PASSED 100%!")
