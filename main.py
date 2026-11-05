import time
from game import (WORLD, REQUIRED_TO_ENTER, new_game, available_actions,
                  can_enter, move_player, pick_up, light_beacon,
                  is_win, is_loss)

LINE = "-" * 40
STARS = "*" * 40

ITEM_HINTS = {
    "rope": "Take the coil of rope (it might help you cross something)",
    "lantern": "Take the glinting lantern (it might light the way)",
    "coconut": "Eat the coconut to regain energy",
}

SPECIAL_ROUTES = {
    ("Beach", "Cave"): "Follow the narrow cliff path to the Cave",
}


def pause(seconds=1.0):
    time.sleep(seconds)


def show_instructions():
    print("=" * 40)
    print("   THE LOST LIGHTHOUSE")
    print("=" * 40)
    print("A storm wrecked your boat. You wake up on Mystery Island.")
    print("The lighthouse is dark. If you light its beacon, a rescue")
    print("boat will come. Every step you take costs 1 energy, and you")
    print("start with 5. If your energy hits 0, you lose.")
    print("Explore, read the clues, and choose your route wisely.")
    print("Type the number of an option and press Enter.\n")


def describe_action(state, action):
    if action == "pick_up":
        item = WORLD[state["location"]]["item"]
        return ITEM_HINTS.get(item, f"Take the {item}")
    if action == "inventory":
        return "Check your bag"
    if action == "light_beacon":
        return "Light the beacon"
    if action == "quit":
        return "Quit the game"
    if action.startswith("move:"):
        dest = action.split(":")[1]
        label = SPECIAL_ROUTES.get((state["location"], dest),
                                   f"Walk to the {dest}")
        if not can_enter(state, dest):
            needed = REQUIRED_TO_ENTER[dest]
            label += f" (you need the {needed} first)"
        return label
    return action


def play_game(name):
    state = new_game(name)

    while not state["game_over"]:
        print("\n" + LINE)
        print(f"You are at: {state['location']}")
        print(f"Energy left: {state['energy']}")
        print(LINE)
        print(WORLD[state["location"]]["description"])

        choices = available_actions(state)
        print("\nWhat would you like to do?")
        for idx, action in enumerate(choices, 1):
            print(f" [{idx}] {describe_action(state, action)}")

        try:
            choice_idx = int(input("\nPick a number: ")) - 1
            if choice_idx < 0 or choice_idx >= len(choices):
                print("Hmm, that number isn't on the menu. Try another one.")
                continue
        except ValueError:
            print("Please type a number from the menu.")
            continue

        action_taken = choices[choice_idx]

        match action_taken.split(":"):
            case ["move", dest]:
                print(f"\n-> {move_player(state, dest)}")
                pause()
            case ["pick_up"]:
                print(f"\n-> {pick_up(state)}")
                pause()
            case ["light_beacon"]:
                print(f"\n-> {light_beacon(state)}")
                pause()
            case ["inventory"]:
                print("\nYou open your bag...")
                pause(1.5)
                inv = state["inventory"]
                if inv:
                    print(f"You are carrying: {', '.join(inv)}")
                else:
                    print("Your bag is empty for now.")
                pause()
            case ["quit"]:
                print("\nThanks for playing, see you next time!")
                return False
            case _:
                print("\nI didn't understand that one.")

    pause(1.5)
    if is_win(state):
        print("\n" + STARS)
        print(f"Well done, {state['name']}! You lit the beacon and escaped!")
        print(STARS)
    elif is_loss(state):
        print("\n" + STARS)
        print("You ran out of energy this time. Try a different route?")
        print(STARS)
    return True


def ask_play_again():
    while True:
        answer = input("\nPlay again? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please type y or n.")


def main():
    show_instructions()
    name = input("What's your name, explorer? ").strip() or "Explorer"

    while True:
        finished = play_game(name)
        if not finished:
            break
        if not ask_play_again():
            print("\nGoodbye, explorer!")
            break


if __name__ == "__main__":
    main()