from tictactoe import TicTacToe
from gameUI import draw_board,handle_events
from valueiteration import ReinforcementAgent
from ai import Agent
from utilities import Player
import pickle
import sys

# Create a new game and draw something on the screen
# while waiting for loading or calculation of the policy.
game = TicTacToe()
draw_board(game.board)

v = sys.argv[1]
if v == "X" or v == "x":
    player = Player.X
elif v == "o" or v == "O" or v == "0":
    player = Player.O
else:
    print(f("{v} isn't a valid player, please use 'X' or 'O'"))
    print("Using default...")
    player = Player.X

print("Player starting" if player == Player.X else "Player second")



# Use precalculated policy from file.
# If file not present, find the policy via value iteration.
try:
    print("Reading the AI policy")
    if player == player.X:
        file = open("policy_O.pkl","rb")
    else:
        file = open("policy_X.pkl", "rb")
    policy = pickle.load(file)
    ai = Agent(game,policy)
except:
    print("Failed to read the AI policy, calculating it now...")
    print("To precalculate and save the policy run valueiteration.py")
    ai = ReinforcementAgent(game,~player)
print("Ready to play!!!")

assert(len(sys.argv) == 2)



# TODO : Add possibility for player to play as O
while True:
    if not game.finished() and game.player is ~player:
        ai.play()
    handle_events(game)            
    draw_board(game.board)