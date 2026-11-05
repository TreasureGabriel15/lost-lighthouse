WORLD = {
    "Beach": {
        "exits": ["Jungle", "Cave"],
        "item": None,
        "description": ("The storm has passed. Thick jungle lies ahead, and a "
                        "narrow cliff path winds off toward a dark cave."),
    },
    "Jungle": {
        "exits": ["Beach", "Cave", "Tide Pools"],
        "item": "rope",
        "description": ("Vines hang everywhere. A coil of strong rope lies "
                        "half-buried in the leaves."),
    },
    "Tide Pools": {
        "exits": ["Jungle"],
        "item": "coconut",
        "description": "Calm pools glitter here. A ripe coconut has washed ashore.",
    },
    "Cave": {
        "exits": ["Beach", "Jungle", "Old Bridge"],
        "item": "lantern",
        "description": "It is dim and damp. Something made of glass glints on a rock.",
    },
    "Old Bridge": {
        "exits": ["Cave", "Lighthouse"],
        "item": None,
        "description": ("The bridge is torn open over a deep gap. You would "
                        "need something to cross it."),
    },
    "Lighthouse": {
        "exits": ["Old Bridge"],
        "item": None,
        "description": "The great lamp is cold and dark. It needs a light source.",
    },
}

REQUIRED_TO_ENTER = {"Old Bridge": "rope"}
ENERGY_BONUS = {"coconut": 3}


def new_game(name):
    return {"name": name, "location": "Beach", "energy": 5,
            "inventory": [], "game_over": False, "won": False}


def can_move(state, destination):
    return destination in WORLD[state["location"]]["exits"]


def can_enter(state, destination):
    needed = REQUIRED_TO_ENTER.get(destination)
    return needed is None or needed in state["inventory"]


def can_light_beacon(state):
    return state["location"] == "Lighthouse" and "lantern" in state["inventory"]


def pick_up(state):
    item = WORLD[state["location"]]["item"]
    if state["game_over"]:
        return "The game is over."
    if item is None:
        return "There is nothing to pick up here."
    if item in state["inventory"]:
        return f"You already have the {item}."
    state["inventory"].append(item)
    bonus = ENERGY_BONUS.get(item, 0)
    if bonus:
        state["energy"] += bonus
        return f"You eat the {item} and feel stronger (+{bonus} energy)."
    return f"You picked up the {item}."


def move_player(state, destination):
    if state["game_over"]:
        return "The game is over."
    if not can_move(state, destination):
        return f"You can't go to {destination} from here."
    if not can_enter(state, destination):
        return (f"You need the {REQUIRED_TO_ENTER[destination]} "
                f"to reach the {destination}.")
    state["location"] = destination
    state["energy"] -= 1
    if state["energy"] <= 0:
        state["game_over"] = True
        return "You collapse from exhaustion."
    return f"You walk to the {destination}."


def light_beacon(state):
    if state["game_over"]:
        return "The game is over."
    if state["location"] != "Lighthouse":
        return "You need to be at the Lighthouse to light the beacon."
    if not can_light_beacon(state):
        return "You need the lantern to light the beacon."
    state["won"] = True
    state["game_over"] = True
    return "The beacon blazes to life. A rescue boat is on its way!"


def available_actions(state):
    if state["game_over"]:
        return []
    actions = [f"move:{place}" for place in WORLD[state["location"]]["exits"]]
    item = WORLD[state["location"]]["item"]
    if item is not None and item not in state["inventory"]:
        actions.append("pick_up")
    if state["location"] == "Lighthouse":
        actions.append("light_beacon")
    actions.append("inventory")
    actions.append("quit")
    return actions


def is_win(state):
    return state["won"]


def is_loss(state):
    return state["game_over"] and not state["won"]