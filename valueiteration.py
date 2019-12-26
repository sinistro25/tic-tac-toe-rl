from tictactoe import TicTacToe
from ai import Agent
from copy import deepcopy
import pickle
from utilities import *
RVICTORY = 1
RLOSS = -1
RDRAW = 0
RBASE = 0
EPSILON = 0.0001

# If gamma < 1 it will prioritize to end the game the sooner posible
# I set it to 1 because I like to see my enemies suffer when and I stall the
# the game when they can't win (MUAHAHAHA!)
GAMMA = 0.90
#GAMMA = 1



class StateActionSpaceGenerator:
    
    def __init__(self,game):
        self.num_states = 0
        self.game = game
        self.action_state_transition = {}
        # player X movements
        self._recursive_move(game)
        # player O movements
        for i in range(game.sz):
            for j in range(game.sz):
                g = deepcopy(game)
                g.mark(i,j)
                self._recursive_move(g)
        return None
        
    def _recursive_move(self,game):
        tboard = list_to_tuple2d(game.board)
        
        if game.finished():
            self.action_state_transition[tboard] = {}
            return 
        if tboard in self.action_state_transition:
            return
        self.action_state_transition[tboard] = {}
        
        for action in game.open_fields():
            self.action_state_transition[tboard][action] = set()
            n_game = deepcopy(game)
            n_game.mark(*action)
            if n_game.finished():
                self.action_state_transition[tboard][action].add(list_to_tuple2d(n_game.board))
                self.action_state_transition[list_to_tuple2d(n_game.board)] = {}
                continue
            for action2 in n_game.open_fields():
                n2_game = deepcopy(n_game)
                n2_game.mark(*action2)
                self.action_state_transition[tboard][action].add(list_to_tuple2d(n2_game.board))
                self._recursive_move(n2_game)




def reward(state):
    b = TicTacToe(board=tuple_to_list2d(state))
    tmp = b.finished()
    if tmp == False:
        return RBASE
    if tmp == True:
        return RDRAW
    if tmp == Player.X:
        return RVICTORY
    return RLOSS

class ReinforcementAgent(Agent):
    def __init__(self,game,player=Player.X):
        self.player = player
        # Must recieve a board in the player X state
        assert(game.player == Player.X and not game.finished())
        if player == Player.X:
            self.game = game
            self.ast = StateActionSpaceGenerator(game).action_state_transition
        else:
            self.game = game
            self.ast = {}
            for i in range(game.sz*game.sz):
                g = deepcopy(game)
                if not g.mark(i//game.sz,i % game.sz):
                    continue
                self.ast.update(StateActionSpaceGenerator(g).action_state_transition)
        self._init_v_pi()
        self._value_iteration()        
        self.policy = self._policy()
    
    def _init_v_pi(self):
        states = self.ast.keys()
        mult = 0
        if self.player is Player.X:
            mult = 1
        else:
            mult = -1
        v_pi = {}    
        for state in states:
            #print(state)
            v_pi[state] = mult*reward(state)
        self.v_pi = v_pi
        
    def _value_iteration(self):
        v_pi,action_state_transition = self.v_pi,self.ast
        
        while True:
            delta = 0
            for state, actions in action_state_transition.items():
                v_max = v_pi[state]

                for new_states in actions.values():
                    n = len(new_states)
                    v = 0
                    for new_state in new_states:
                        v += v_pi[new_state]
                    v /= n
                    v *= GAMMA
                    if v > v_max:
                        v_max = v
                delta = max(delta,abs(v_max-v_pi[state]))
                v_pi[state] = v_max
            if epsilon_equal(delta,0):
                return
            
    def _policy(self):
        v_pi = self.v_pi
        action_state_transition = self.ast
        pi = {}
        for state,actions in action_state_transition.items():
            v_max = float("-inf")
            a_max = None
            for action, n_states in actions.items():
                v = 0
                n = len(n_states)
                for n_state in n_states:
                    v += GAMMA*v_pi[n_state]
                v /= n
                if v > v_max:
                    v_max = v
                    a_max   = action
            pi[state] = a_max
        return pi   
    
    
if __name__ == "__main__":
    print("Calculating and saving the X player agent policy...")
    game = TicTacToe()
    agent = ReinforcementAgent(game,player=Player.X)
    file = open("policy_X.pkl","wb")
    pickle.dump(agent.policy, file)
    file.close() 
    
    print("Calculating and saving the O player agent policy...")
    agent = ReinforcementAgent(game,player=Player.O)
    file = open("policy_O.pkl","wb")
    pickle.dump(agent.policy, file)
    file.close()   
    print("Finished!")