import numpy as np
import multiprocessing as mp
valid_called = 0

def add_coords(coords1, coords2):
    return (coords1[0] + coords2[0], coords1[1] + coords2[1])

def is_valid_coords(coords):
    return 0<= coords[0] < 8 and 0<= coords[1] < 8

def second_side(side):
    return 2 if side == 1 else 1



class Board:
    MOVE_DIRS = [(-1, -1), (-1, 0), (-1, 1),
             (0, -1),           (0, 1),
             (1, -1), (1, 0), (1, 1)]

    def __init__(self):
        self.board = np.zeros((8,8), dtype=np.int8) # 1 -> black, 2 -> white
        self.board[3,3] = 1
        self.board[4,4] = 1 
        self.board[3,4] = 2
        self.board[4,3] = 2
    
    def get_board(self):
        return self.board.copy()
    
    def do_move(self, move: tuple, player):
        if move == None:
            return False
        self.board[move] = player
        self.convert_stones(self.get_affected_stones(player,move))
        return True
    
    def convert_stones(self, affected):
        for coords in affected:
            self.board[coords] = second_side(self.board[coords])
        pass

    def get_affected_stones(self, side, move: tuple) -> list:
        affected = []
        second = second_side(side)
        for dir in Board.MOVE_DIRS:
            dx, dy = dir
            x, y = move
            x += dx
            y += dy
            potential = []
            while is_valid_coords((x,y)) and self.board[x,y] == second:
                potential.append((x,y))
                x += dx
                y += dy
            if is_valid_coords((x,y)) and self.board[x,y] == side:
                affected.extend(potential)
                
        return affected

    def get_valid_moves(self, side) -> list:
        valid_moves = []
        second = second_side(side)
        for i in range(8):
            for j in range(8):
                if self.board[i,j] == side:
                    for dx, dy in Board.MOVE_DIRS:
                        x = i + dx
                        y = j + dy
                        count = 0
                        while 0<=x<8 and 0<=y<8 and self.board[x,y] not in (0,side):
                            count += 1
                            x+=dx
                            y+=dy
                        if 0<=x<8 and 0<=y<8 and self.board[x,y] == 0 and count > 0:
                            if (x,y) not in valid_moves: valid_moves.append((x,y))
        return valid_moves


    def copy(self):
        new_board = Board()
        new_board.board = self.board.copy()
        return new_board
    
    def is_ended(self):
        return not (np.sum(self.board ==0) or 
                    len(self.get_valid_moves(1)) == 0 and 
                    len(self.get_valid_moves(2)) == 0)


    def get_score(self):
        return np.sum(self.board == 1), np.sum(self.board == 2)
    def __str__(self):
<<<<<<< Updated upstream
        return str(self.board)#.replace("0"," ").replace("1","\N{black circle}").replace("2","\N{white circle}")
=======
        return str(self.board)
        #return str(self.board).replace("0"," ").replace("1","\N{black circle}").replace("2","\N{white circle}")
>>>>>>> Stashed changes




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
        print(self.main_board)
        print("-----------------------")
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
                continue
            if np.sum(self.main_board.board == 0) == 0:
                break
            if np.sum(self.main_board.board == 1) == 0 or np.sum(self.main_board.board == 2) == 0:
                break
            move = self.Turn(valid_moves)
   
        #print(valid_called)
        return self.get_score()
    
    def get_winner(self, score):
        if score[0] > score[1]:
            return self.player1.__class__.__name__
        elif score[0] < score[1]:
            return self.player2.__class__.__name__
        else:
            return 0