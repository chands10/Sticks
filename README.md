# Sticks AI
* A program that uses Expectimax (or Minimax) search to win a game of sticks
* The rules of Sticks can be found here (with some differentiations noted below): https://en.wikipedia.org/wiki/Chopsticks_(hand_game)
  - Note that this program can only support 2 players (which can be any combination of humans vs AIs)
  - No player can split and have a hand with at least five fingers after the split, or have the same configuration as before the split
  - If a player's hand reaches at least five fingers, it is considered a dead hand
* Run Game.py to start the game and enter in the number of humans playing (0 - 2)
* Supported commands:
  - tap [your hand] [opponent hand]
    - left hand is represented by 0
    - right hand is represented by 1
  - split [new left hand value] [new right hand value]
