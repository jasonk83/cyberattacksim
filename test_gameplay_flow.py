"""
test_gameplay_flow.py
Integration test for CloudStore Command gameplay state machine,
straw polling, asymmetric governance, and timer operations.
"""

from state_manager import GameState
from scoring_engine import evaluate_final_outcome, get_outcome_thresholds

def test_full_game_lifecycle():
    print("=== Testing Game State Lifecycle & Polling ===")
    game = GameState()
    game.reset(base_health=100.0, max_rounds=2)

    # 1. Test Lobby & Timer
    assert game.phase == "lobby"
    assert game.company_health == 100.0
    assert game.current_round == 1

    # Start Hacker Phase
    game.start_phase("hacker")
    assert game.phase == "hacker"
    assert game.phase_duration == 300
    rem = game.get_remaining_seconds()
    assert 295 <= rem <= 300, f"Expected ~300s remaining, got {rem}"

    # Test Timer Pause & Resume
    game.pause_timer()
    assert game.timer_paused is True
    paused_rem = game.get_remaining_seconds()
    game.resume_timer()
    assert game.timer_paused is False
    assert abs(game.get_remaining_seconds() - paused_rem) <= 1

    # 2. Test Straw Polling on Hacker Team
    sample_options = [{"id": "A", "label": "Phishing"}, {"id": "B", "label": "Exploit"}]
    game.open_poll("hackers", sample_options)
    assert game.polls["hackers"]["open"] is True

    # 3 Viewers vote
    game.cast_vote("hackers", "voter_1", "A")
    game.cast_vote("hackers", "voter_2", "A")
    game.cast_vote("hackers", "voter_3", "B")

    stats = game.get_poll_stats("hackers")
    assert stats["total_votes"] == 3
    assert stats["tallies"]["A"]["count"] == 2
    assert stats["tallies"]["B"]["count"] == 1
    print("✅ Straw polling verified successfully!")

    # Hacker Captain submits attack A
    game.submit_hacker_attack("A")
    assert game.phase == "it"
    assert game.selected_attack_key == "A"
    assert game.phase_duration == 300
    print("✅ Hacker attack submission & transition to IT verified!")

    # 3. Test IT Containment
    game.open_poll("it", [{"id": "1", "label": "Full Lockout"}, {"id": "2", "label": "EDR"}])
    game.cast_vote("it", "voter_it_1", "1")
    game.submit_it_choice("1")
    assert game.phase == "exec"
    assert game.it_choice_id == "1"
    assert game.phase_duration == 180  # Exec phase is 3 minutes (180s)
    print("✅ IT submission & transition to Exec (180s timer) verified!")

    # 4. Test Executive Governance
    game.open_poll("exec", [{"id": "approve", "label": "Approve"}])
    game.cast_vote("exec", "voter_ex_1", "approve")
    game.submit_exec_choice("approve")
    assert game.phase == "media"
    assert game.exec_action == "approve"
    assert game.phase_duration == 300  # Media phase is 5 minutes (300s)
    print("✅ Exec governance submission & transition to Media verified!")

    # 5. Test Media Selection & Round Evaluation
    game.submit_media_choice(2)  # Balanced headline
    assert game.phase == "recap"
    assert len(game.history) == 1
    rec = game.history[0]
    print(f"Round 1 Result: {rec['attack_name']} -> Net Health Delta: {rec['net_delta']} HP (New Health: {game.company_health})")
    assert 0 <= game.company_health <= 100
    print("✅ Round 1 evaluation & scoring breakdown verified!")

    # 6. Test Undo
    assert len(game.snapshots) > 0
    rolled_back = game.undo_last_round()
    assert rolled_back is True
    # Re-submit media choice to return to recap after undo test
    game.submit_media_choice(2)
    assert game.phase == "recap"

    # 7. Advance to Round 2 and Verify Straw Poll Reset
    game.advance_to_next_round()
    assert game.current_round == 2
    assert game.phase == "hacker"
    # Verify Hacker straw poll is cleanly reset
    assert game.polls["hackers"]["open"] is False
    assert len(game.polls["hackers"]["votes"]) == 0
    stats = game.get_poll_stats("hackers")
    assert stats["total_votes"] == 0
    print("✅ Hacker straw poll cleanly reset upon advancing to Round 2!")

    # Complete Round 2
    game.submit_hacker_attack("A")
    game.submit_it_choice("1")
    game.submit_exec_choice("approve")
    game.submit_media_choice(1)
    assert game.phase == "recap"
    assert len(game.history) == 2
    print("✅ Round 2 completed successfully!")

    # 8. Advance from Round 2 Recap -> Triggers Final Hacker Action
    game.advance_to_next_round()
    assert game.phase == "final_hacker_action"
    assert game.phase_duration == 180
    print("✅ Advanced to Final Threat Actor Gambit (final_hacker_action phase)!")

    # Test Hacker Straw Poll in Final Action
    game.open_poll("hackers", [{"id": "press", "label": "Press Attack"}, {"id": "retreat", "label": "Safe Retreat"}])
    game.cast_vote("hackers", "v1", "press")
    game.cast_vote("hackers", "v2", "retreat")
    stats = game.get_poll_stats("hackers")
    assert stats["total_votes"] == 2

    # Hacker Captain authorizes Press Attack
    result = game.submit_final_hacker_action("press")
    assert game.phase == "game_over"
    assert result["action"] == "press"
    if result["caught"]:
        assert result["damage"] == 0
        assert 3 <= result["recovery"] <= 15
        assert result["net_delta"] == result["recovery"]
    else:
        assert 15 <= result["damage"] <= 30
        assert result["recovery"] == 0
        assert result["net_delta"] == -result["damage"]
    assert game.final_hacker_action_data is not None
    print(f"✅ Final Hacker Action executed: {result['summary']}")

    # 9. Test Outcome Thresholds for 2 and 3 rounds
    b2, w2 = get_outcome_thresholds(2)
    assert b2 == 39 and w2 == 75
    b3, w3 = get_outcome_thresholds(3)
    assert b3 == 30 and w3 == 60

    tier_win, _, _ = evaluate_final_outcome(78.0, 2)
    assert tier_win == "Win"
    tier_survive, _, _ = evaluate_final_outcome(50.0, 2)
    assert tier_survive == "Survive"
    tier_bankrupt, _, _ = evaluate_final_outcome(25.0, 2)
    assert tier_bankrupt == "Bankrupt"
    print("✅ Outcome evaluation tiers verified!")
    print("\n🎉 ALL GAMEPLAY TESTS PASSED!")

if __name__ == "__main__":
    test_full_game_lifecycle()
