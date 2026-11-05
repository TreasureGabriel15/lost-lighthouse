import unittest
from game import (new_game, move_player, pick_up, light_beacon,
                  available_actions, is_win, is_loss)


def walk(state, *places):
    """Helper: make several moves in a row."""
    for place in places:
        move_player(state, place)


class TestMysteryIsland(unittest.TestCase):

    def test_new_game_starts_correctly(self):  # T1
        state = new_game("Ada")
        self.assertEqual(state["location"], "Beach")
        self.assertEqual(state["energy"], 5)
        self.assertEqual(state["inventory"], [])
        self.assertFalse(state["game_over"])

    def test_invalid_destination_changes_nothing(self):  # T2
        state = new_game("Ada")
        move_player(state, "Banana")
        self.assertEqual(state["location"], "Beach")
        self.assertEqual(state["energy"], 5)
        self.assertEqual(state["inventory"], [])

    def test_legal_move_costs_one_energy(self):  # T3
        state = new_game("Ada")
        move_player(state, "Jungle")
        self.assertEqual(state["location"], "Jungle")
        self.assertEqual(state["energy"], 4)

    def test_wrong_direction_is_free(self):  # T4
        state = new_game("Ada")
        move_player(state, "Lighthouse")  # not an exit from the Beach
        self.assertEqual(state["location"], "Beach")
        self.assertEqual(state["energy"], 5)

    def test_rope_can_be_collected_once(self):  # T5
        state = new_game("Ada")
        walk(state, "Jungle")
        pick_up(state)
        pick_up(state)
        self.assertEqual(state["inventory"].count("rope"), 1)

    def test_bridge_blocked_without_rope(self):  # T6
        state = new_game("Ada")
        walk(state, "Cave")
        move_player(state, "Old Bridge")
        self.assertEqual(state["location"], "Cave")
        self.assertEqual(state["energy"], 4)  # only the Beach->Cave move cost energy

    def test_beacon_needs_lantern(self):  # T7
        state = new_game("Ada")
        state["location"] = "Lighthouse"
        light_beacon(state)
        self.assertFalse(is_win(state))
        self.assertFalse(state["game_over"])

    def test_beacon_with_lantern_wins(self):  # T8
        state = new_game("Ada")
        state["location"] = "Lighthouse"
        state["inventory"].append("lantern")
        light_beacon(state)
        self.assertTrue(is_win(state))
        self.assertTrue(state["game_over"])

    def test_running_out_of_energy_loses(self):  # T9
        state = new_game("Ada")
        state["energy"] = 1
        move_player(state, "Jungle")
        self.assertTrue(is_loss(state))
        self.assertEqual(state["energy"], 0)

    def test_replay_starts_fresh(self):  # T10
        first = new_game("Ada")
        first["inventory"].append("rope")
        first["energy"] = 1
        second = new_game("Ada")
        self.assertEqual(second["inventory"], [])
        self.assertEqual(second["energy"], 5)
        self.assertEqual(second["location"], "Beach")

    def test_full_winning_route(self):
        state = new_game("Ada")
        walk(state, "Jungle")
        pick_up(state)                      # rope
        walk(state, "Cave")
        pick_up(state)                      # lantern
        walk(state, "Old Bridge", "Lighthouse")
        light_beacon(state)
        self.assertTrue(is_win(state))
        self.assertEqual(state["energy"], 1)

    def test_cliff_route_is_a_trap(self):
        state = new_game("Ada")
        walk(state, "Cave")
        pick_up(state)                      # lantern
        walk(state, "Jungle")
        pick_up(state)                      # rope
        walk(state, "Cave", "Old Bridge", "Lighthouse")
        self.assertTrue(is_loss(state))     # arrives with 0 energy
        self.assertFalse(is_win(state))

    def test_coconut_gives_energy_once(self):
        state = new_game("Ada")
        walk(state, "Jungle", "Tide Pools")  # energy 3
        pick_up(state)                       # +3
        self.assertEqual(state["energy"], 6)
        pick_up(state)                       # second time: no extra energy
        self.assertEqual(state["energy"], 6)

    def test_no_moves_after_game_over(self):
        state = new_game("Ada")
        state["game_over"] = True
        move_player(state, "Jungle")
        self.assertEqual(state["location"], "Beach")
        self.assertEqual(state["energy"], 5)

    def test_actions_empty_when_game_over(self):
        state = new_game("Ada")
        state["game_over"] = True
        self.assertEqual(available_actions(state), [])


if __name__ == "__main__":
    unittest.main()