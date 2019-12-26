from utilities import *
class TicTacToe:
    def __init__(self,sz = 3, board = None):
        if board is None:
            self.board = [[None for i in range(sz)] for _ in range(sz)]
        else:
            self.board = board
        self.sz = sz
        self.player = Player.X
            
        
    def __repr__(self):
        s = "<Board: \n"
        for i in range(3):
            s += str(["_" if x is None else x for x in self.board[i]]) + "\n"
        s += ">"
        return s
    
    def _change_player(self):
        if self.player is Player.X:
            self.player = Player.O
        else:
            self.player = Player.X
            
    def mark(self,x,y):
        if self.board[y][x] is not None:
            return False
        else:
            self.board[y][x] = self.player
            self._change_player()
            return True
    
    def open_fields(self):
        of = []
        for i in range(self.sz):
            for j in range(self.sz):
                if self.board[j][i] is None:
                    of.append((i,j))
        return of                    
    def finished(self):
        for i in range(3):
            if self.board[i][0] and self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return self.board[i][0]
            elif self.board[0][i] and self.board[0][i] == self.board[1][i] == self.board[2][i]:
                return self.board[0][i]
        
        if self.board[0][0] and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0]
        if self.board[0][2] and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2]
        if self.open_fields() == []:
            return True
        return False    
