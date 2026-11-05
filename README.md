# lost-lighthouse
# The Lost Lighthouse

A text adventure for the terminal, written in Python. You wake on Mystery
Island after a storm. Light the lighthouse beacon before your energy runs
out so the rescue boat can find you.

## Prerequisites
- Python 3.10 or newer (the game uses `match`/`case`)
- No external libraries

## How to run
```
python3 main.py
```
Type the number of the option you want and press Enter.
(Use `python` instead of `python3` if that is the command on your machine.)

## Game rules
- You start at the Beach with 5 energy and an empty inventory.
- Each legal move costs 1 energy. Picking up items (except the coconut's
  bonus), checking your bag, and invalid input cost nothing.
- Locations: Beach, Jungle, Tide Pools, Cave, Old Bridge, Lighthouse.
- Rope (Jungle) is needed to reach the Old Bridge.
- Lantern (Cave) is needed, at the Lighthouse, to light the beacon.
- The coconut (Tide Pools) gives +3 energy when taken.
- Each item can be picked up only once.
- Energy reaching 0 before the beacon is lit means you lose.
- After a win or loss you can play again with a completely fresh game.
  Quitting ends the program without the replay question.

## Meaningful decisions
1. **Cliff path or jungle route.** The cliff path from the Beach to the Cave
   is one move shorter to the lantern, but the bridge needs the rope from
   the Jungle, so you must double back. Taking the cliff first leaves you
   with 0 energy on arrival at the Lighthouse, which is a loss.
2. **Coconut detour.** Tide Pools costs 2 moves round trip and gives +3
   energy. The player decides whether the detour is worth it.
3. **[Write your own third decision here, or note honestly that two are
   strong and describe what the third is.]**

## How to run the tests
```
python3 -m unittest discover -s tests -v
```

## Project structure
- `main.py`: input and output only (instructions, menu, printing, replay)
- `game.py`: all the rules, with no `input()` or `print()`
- `tests/test_game.py`: automated tests for the rules

## Example winning run
1. Walk to the Jungle (energy 4)
2. Take the rope
3. Walk to the Cave (energy 3)
4. Take the lantern
5. Walk to the Old Bridge (energy 2)
6. Walk to the Lighthouse (energy 1)
7. Light the beacon: you win with 1 energy left

## Known limits
- Reaching the Lighthouse on your last energy point loses the game before
  you can light the beacon.
- The coconut can raise energy above the starting 5.
- There is no save or load.
- The short pauses in the game use `time.sleep`, so the game feels slower
  than the rules alone would make it.
- Menu numbers change depending on what is available, so always read the
  menu before choosing.

## AI use
[Write this yourself, honestly: what AI taught you, what code it wrote,
and what you changed and tested on your own.]