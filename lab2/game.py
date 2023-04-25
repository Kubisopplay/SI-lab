import numpy as np
import multiprocessing as mp
valid_called = 0

def add_coords(coords1, coords2):
    return (coords1[0] + coords2[0], coords1[1] + coords2[1])

def is_valid_coords(coords):
    return 0<= coords[0] < 8 and 0<= coords[1] < 8

def second_side(side):
    return 2 if side == 1 else 1

class Move:
    def __init__(self, coords1, coords2, affected_stones):
        self.coords1 = coords1
        self.coords2 = coords2
        self.affected_stones = affected_stones
        #if max(abs(coords1[0]-coords2[0]), abs(coords1[1]-coords2[1]))-1 > len(affected_stones):
        #   print("Invalid move")
        
    def __str__(self):
        return f"Move from {self.coords1} to {self.coords2} affected {len(self.affected_stones)}"

class Board:
    MOVE_DIRS = [(-1, -1), (-1, 0), (-1, 1),
             (0, -1),           (0, 1),
             (1, -1), (1, 0), (1, 1)]
    pool : mp.Pool

    def __init__(self):
        self.board = np.zeros((8,8), dtype=np.int8) # 1 -> black, 2 -> white
        self.board[3,3] = 1
        self.board[4,4] = 1 
        self.board[3,4] = 2
        self.board[4,3] = 2
    
    def get_board(self):
        return self.board.copy()
    
    def do_move(self, move: Move, player):
        if move == None:
            return False
        self.board[move.coords2[0], move.coords2[1]] = player
        self.convert_stones(move.affected_stones)
        return True
    
    def convert_stones(self, affected):
        for coords in affected:
            self.board[coords] = second_side(self.board[coords])
        pass


    def get_valid_moves(self, side) -> list:
        valid_moves = []
        second = second_side(side)
        for i in range(8):
            for j in range(8):
                if self.board[i,j] == side:
                    for dir in Board.MOVE_DIRS:
                        coords = add_coords((i,j), dir)
                        affected = [coords]

                        while is_valid_coords(coords) and self.board[coords] != side:
                            if self.board[coords] == second:
                                affected.append(coords)
                                coords = add_coords(coords, dir)
                                continue

                            if self.board[coords] == 0:
                                valid_moves.append(Move((i,j), coords, affected))
                                break
                            break
        return valid_moves


    def copy(self):
        new_board = Board()
        new_board.board = self.board.copy()
        return new_board
    
    def get_score(self):
        return np.sum(self.board == 1), np.sum(self.board == 2)
    def __str__(self):
        return str(self.board)




class Game:
    def __init__(self) -> None:
        self.main_board = Board()
        self.side = 1
        self.player1 = None
        self.player2 = None

    def setupPlayers(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def Turn(self, valid_moves = None):
        active_player = self.player1 if self.side == 1 else self.player2
        move = active_player.get_move(self.main_board, self.side, valid_moves)
        self.main_board.do_move(move, self.side)
        self.side = second_side(self.side)
        return move

    def get_score(self):
        return self.main_board.get_score()
    
    def play(self):
        self.main_board = Board()
        global valid_called
        valid_called = 0
        while True:
            valid_moves = self.main_board.get_valid_moves(self.side)
            #print(move," on side of ", self.side)
            #print(self.main_board)
            if len(valid_moves) == 0:
                self.side = second_side(self.side)
                if len(self.main_board.get_valid_moves(self.side)) == 0:
                    break
            if np.sum(self.main_board.board == 0) == 0:
                break
            if np.sum(self.main_board.board == 1) == 0 or np.sum(self.main_board.board == 2) == 0:
                break
            move = self.Turn(valid_moves)
   
        print(valid_called)
        return self.get_score()
    
    def get_winner(self, score):
        if score[0] > score[1]:
            return self.player1.__class__.__name__
        elif score[0] < score[1]:
            return self.player2.__class__.__name__
        else:
            return 0