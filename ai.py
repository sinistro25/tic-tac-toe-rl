from utilities import list_to_tuple2d
class Agent:
    
    def __init__(self, game, policy):
        self.game = game
        self.policy = policy
    
    def play(self):
        tboard = list_to_tuple2d(self.game.board)
        self.game.mark(*self.policy[tboard])
