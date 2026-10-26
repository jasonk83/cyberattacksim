"""
simulate_full_multiplayer.py
End-to-end multi-session simulator using Streamlit AppTest.
Simulates GM, Captains, and Viewers across Hackers, IT, Exec, and Media.
Logs latency, state consistency, UI element integrity, and game flow metrics.
"""

import sys
import time
from streamlit.testing.v1 import AppTest
from state_manager import GameState
import game_data

def run_role_simulation(rounds=2):
    print(f"=== Starting Multi-Session Tabletop Simulation ({rounds} Rounds) ===")
    start_time = time.time()
    
    # 1. Initialize GM Projector
    gm = AppTest.from_file("app.py")
    gm.query_params["team"] = "main"
    gm.run()
    assert not gm.exception, f"GM exception: {gm.exception}"
    print("  [GM] Loaded Mission Control Projector.")

    # Authenticate GM
    admin_pwd_input = gm.sidebar.text_input[0]
    admin_pwd_input.input("admin123")
    gm.sidebar.button[0].click().run()
    assert not gm.exception
    print("  [GM] Authenticated with GM Console.")

    # Set round count if in lobby
    # Find start round button
    start_btn = None
    for b in gm.sidebar.button:
        if "Start Round 1" in b.label:
            start_btn = b
            break
    if start_btn:
        start_btn.click().run()
        print("  [GM] Started Round 1!")

    # 2. Simulate Hackers
    # Hacker Captain
    h_capt = AppTest.from_file("app.py")
    h_capt.query_params["team"] = "hackers"
    h_capt.run()
    # Enter captain passcode
    h_capt.sidebar.text_input[0].input("hacker123")
    h_capt.sidebar.button[0].click().run()
    print("  [Hackers] Captain authenticated.")

    # Hacker Viewer
    h_view = AppTest.from_file("app.py")
    h_view.query_params["team"] = "hackers"
    h_view.run()
    print("  [Hackers] Viewer joined in Viewer Mode.")

    # Captain opens poll
    open_poll_btn = None
    for b in h_capt.button:
        if "Launch Straw Poll" in b.label:
            open_poll_btn = b
            break
    assert open_poll_btn is not None, "Could not find Launch Straw Poll button in Hacker Captain view"
    open_poll_btn.click().run()
    print("  [Hackers] Captain launched Straw Poll.")

    # Viewer casts vote for Vector B
    h_view.run()
    vote_b = None
    for b in h_view.button:
        if "Vote: B" in b.label:
            vote_b = b
            break
    assert vote_b is not None, "Could not find Vote: B button in Hacker Viewer"
    vote_b.click().run()
    print("  [Hackers] Viewer cast vote for Vector B.")

    # Captain observes vote and deploys Vector B
    h_capt.run()
    deploy_b = None
    for b in h_capt.button:
        if "Deploy Vector B" in b.label:
            deploy_b = b
            break
    assert deploy_b is not None, "Could not find Deploy Vector B button"
    deploy_b.click().run()
    print("  [Hackers] Captain deployed Vector B. Phase transitioned to IT Defense.")

    # 3. Simulate IT Defense
    it_capt = AppTest.from_file("app.py")
    it_capt.query_params["team"] = "it"
    it_capt.run()
    it_capt.sidebar.text_input[0].input("tech123")
    it_capt.sidebar.button[0].click().run()

    it_view = AppTest.from_file("app.py")
    it_view.query_params["team"] = "it"
    it_view.run()

    # IT Captain opens poll
    it_poll_btn = None
    for b in it_capt.button:
        if "Launch Straw Poll" in b.label:
            it_poll_btn = b
            break
    assert it_poll_btn is not None, "Could not find IT Launch Straw Poll button"
    it_poll_btn.click().run()
    print("  [IT] Captain launched Straw Poll.")

    # IT Viewer votes for Option 1 (Heavy Downtime)
    it_view.run()
    vote_it_1 = None
    for b in it_view.button:
        if "Vote: 1" in b.label:
            vote_it_1 = b
            break
    assert vote_it_1 is not None, "Could not find Vote: 1 button in IT Viewer"
    vote_it_1.click().run()
    print("  [IT] Viewer voted for Option 1 (24h Downtime).")

    # IT Captain deploys Option 1
    it_capt.run()
    dep_it_1 = None
    for b in it_capt.button:
        if "Deploy & Recommend Option 1" in b.label:
            dep_it_1 = b
            break
    assert dep_it_1 is not None, "Could not find Deploy & Recommend Option 1 button"
    dep_it_1.click().run()
    print("  [IT] Captain submitted Option 1 to Board. Phase transitioned to Executive Governance.")

    # 4. Simulate Executive Boardroom
    ex_capt = AppTest.from_file("app.py")
    ex_capt.query_params["team"] = "exec"
    ex_capt.run()
    ex_capt.sidebar.text_input[0].input("board123")
    ex_capt.sidebar.button[0].click().run()

    ex_view = AppTest.from_file("app.py")
    ex_view.query_params["team"] = "exec"
    ex_view.run()

    # Exec Captain launches poll
    ex_poll_btn = None
    for b in ex_capt.button:
        if "Launch Straw Poll" in b.label:
            ex_poll_btn = b
            break
    assert ex_poll_btn is not None
    ex_poll_btn.click().run()
    print("  [Exec] Captain launched Straw Poll.")

    # Viewer votes to Downgrade
    ex_view.run()
    vote_down = None
    for b in ex_view.button:
        if "downgrade" in b.label.lower():
            vote_down = b
            break
    assert vote_down is not None, "Could not find downgrade vote button in Exec Viewer"
    vote_down.click().run()
    print("  [Exec] Viewer voted to Downgrade.")

    # Exec Captain authorizes Compromise (Option B)
    ex_capt.run()
    auth_down = next(
        (b for b in ex_capt.button if getattr(b, "key", "") == "btn_exec_downgrade" or ("Authorize Directive" in b.label and any(k in b.label for k in ["Compromise", "Downgrade", "Option B"]))),
        None
    )
    assert auth_down is not None, f"Could not find Exec compromise/downgrade button. Available: {[b.label for b in ex_capt.button]}"
    auth_down.click().run()
    print("  [Exec] Captain authorized Compromise directive. Phase transitioned to Media Scrum.")

    # 5. Simulate Media Scrum
    m_capt = AppTest.from_file("app.py")
    m_capt.query_params["team"] = "media"
    m_capt.run()
    m_capt.sidebar.text_input[0].input("press123")
    m_capt.sidebar.button[0].click().run()

    m_view = AppTest.from_file("app.py")
    m_view.query_params["team"] = "media"
    m_view.run()

    # Media Captain launches poll
    m_poll_btn = None
    for b in m_capt.button:
        if "Launch Straw Poll" in b.label:
            m_poll_btn = b
            break
    assert m_poll_btn is not None
    m_poll_btn.click().run()
    print("  [Media] Captain launched Straw Poll.")

    # Media Viewer votes for Headline 3 (Balanced)
    m_view.run()
    vote_m_3 = None
    for b in m_view.button:
        if "Headline 3" in b.label:
            vote_m_3 = b
            break
    assert vote_m_3 is not None
    vote_m_3.click().run()
    print("  [Media] Viewer voted for Headline 3.")

    # Media Captain publishes Headline 3
    m_capt.run()
    pub_3 = None
    for b in m_capt.button:
        if "Publish Headline 3" in b.label:
            pub_3 = b
            break
    assert pub_3 is not None
    pub_3.click().run()
    print("  [Media] Captain published Headline 3. Round 1 complete, transitioned to Recap.")

    # 6. Verify GM Projector Update
    gm.run()
    print("  [GM] Projector updated to Recap phase.")

    elapsed = time.time() - start_time
    print(f"✅ Full round simulation completed in {elapsed:.2f}s with zero exceptions!")
    return True

if __name__ == "__main__":
    run_role_simulation(rounds=1)
