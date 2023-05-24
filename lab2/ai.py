import random
import time
from game import Board, second_side
import multiprocessing as mp
import numpy as np
class Node:
    def __init__(self, board: Board, side: int,  move) -> None:
        self.board = board
        self.side = side
        self.move = move #move that led to this node
        self.children = []
        self.weight = 0
    
    def add_children(self, children: list):
        self.children.extend(children)
        
    


    
class Ai_Base:
    def __init__(self) -> None:
        self.total_time = 0
        self.total_moves = 0
        pass

    def get_move(self, board: Board, side: int, valid_moves: list):
        pass
    
    def calculate_weight(self, board: Board, side: int, move: tuple):
        pass
    
    def create_decision_tree(self, board: Board, side: int, depth: int):
        pass
    
    def __str__(self):
        return self.__class__.__name__
    


class Ai_Random(Ai_Base):
    def get_move(self, board: Board, side: int, valid_moves: list):
        self.total_time += 1
        self.total_moves += 1
        if len(valid_moves) == 0:
            return None
        return random.choice(valid_moves)
    

class Ai_MinMaxBase(Ai_Base):
    def __init__(self, depth: int) -> None:
        super().__init__()
        self.depth = depth
        self.tree = None
 
    def __str__(self):
        return super().__str__() + f"({self.depth})"

    def get_move(self, board: Board, side: int, valid_moves: list):
        start = time.time()
        root = Node(board,side,None)
        self.minmax(root, self.depth, side)
        tree = root.children
        tree.sort(key=lambda x: x.weight, reverse=True)
        self.total_time += time.time() - start
        self.total_moves += 1
        if len(tree) > 0:
            return tree[0].move
        else: None
        
    
    def calculate_weight(self, board: Board, side: int, move: tuple):
        return self.heuristic1(board, side)  + self.heuristic4(board, side) + self.heuristic5(board, side, move)*4 + self.heuristic6(board, side)

    def minmax(self,node, depth: int, starting_side: int = 0):
        if depth == 0:
            return self.calculate_weight(node.board, node.side, node.move)
        if node.board.is_ended():
            return self.calculate_weight(node.board, node.side, node.move)
        children = []
        if node.side == starting_side:
            value = -np.inf
            for move in node.board.get_valid_moves(node.side):
                new_node = Node(node.board.copy(), second_side(node.side), move)
                new_node.board.do_move(move, node.side)
                value = max(value, self.minmax(new_node,depth-1, starting_side))
                new_node.weight = value
                children.append(new_node)
        else:
            value = np.inf
            for move in node.board.get_valid_moves(node.side):
                new_node = Node(node.board.copy(), second_side(node.side), move)
                new_node.board.do_move(move, node.side)
                value = min(value, self.minmax(new_node,depth-1, starting_side))
                new_node.weight = value
                children.append(new_node)
        node.add_children(children)
        return value

    def heuristic1(self, board: Board, side: int):
        return np.sum(board.board == side) #whatever
    
    def heuristic2(self, board: Board, side: int):
        return len(board.get_valid_moves(side)) #kosztowna heurystyka
    
    def heuristic3(self, board: Board, side: int):
        return np.sum(board.board == 0)
    
    def heuristic4(self, board: Board, side: int): #bardzo kosztowna heurystyka
        available_moves = board.get_valid_moves(side)
        if len(available_moves) != 0:
            weight = 0
            for move in available_moves:
                stones = board.get_affected_stones(side, move)
                weight += len(stones)
            return weight
        else:
            return -1
        
    def heuristic5(self,board :Board,side,move):
        return len(board.get_affected_stones(side,move))
    
    def heuristic6(self,board: Board, side: int):
        if board.is_ended():
            if np.sum(board.board ==side) > np.sum(board.board == second_side(side)) :
                return np.inf
            else:
                return -np.inf
        else:
            return 0




class ABPruning(Ai_MinMaxBase):
    
    def get_move(self, board: Board, side: int, valid_moves: list) -> tuple:
        self.alpha = -np.inf
        self.beta = np.inf
        return super().get_move(board, side, valid_moves)
    

    def minmax(self,node, depth: int, starting_side: int = 0):
        if depth == 0:
            return self.calculate_weight(node.board, node.side, node.move)
        if node.board.is_ended():
            return self.calculate_weight(node.board, node.side, node.move)
        children = []
        if node.side == starting_side:
            value = -np.inf
            for move in node.board.get_valid_moves(node.side):
                new_node = Node(node.board.copy(), second_side(node.side), move)
                new_node.board.do_move(move, node.side)
                value = max(value, self.minmax(new_node,depth-1, starting_side))
                new_node.weight = value
                children.append(new_node)
                if(value > self.beta):
                    break
                self.alpha = max(self.alpha, value)
                
        else:
            value = np.inf
            for move in node.board.get_valid_moves(node.side):
                new_node = Node(node.board.copy(), second_side(node.side), move)
                new_node.board.do_move(move, node.side)
                value = min(value, self.minmax(new_node,depth-1, starting_side))
                new_node.weight = value
                children.append(new_node)
                if(value < self.alpha):
                    break
                self.beta = min(self.beta, value)
        node.add_children(children)
        return value
        

class TestPruning(ABPruning):
    def __init__(self, depth: int, heuristics) -> None:
        super().__init__(depth)
        self.total_time = 0
        self.total_moves = 0
        self.heuristics = heuristics
        self.heuristic_table = {}
        self.heuristic_table["heuristic1"] = self.heuristic1
        self.heuristic_table["heuristic2"] = self.heuristic2
        self.heuristic_table["heuristic3"] = self.heuristic3
        self.heuristic_table["heuristic4"] = self.heuristic4
        self.heuristic_table["heuristic5"] = self.heuristic5
        self.heuristic_table["heuristic6"] = self.heuristic6
        pass

    def calculate_weight(self, board: Board, side: int, move: tuple):
        weight = 0
        for heuristic in self.heuristics:
            if heuristic == "heuristic5":
                weight += self.heuristic_table[heuristic](board, side, move)*self.heuristics[heuristic]
                continue
            weight += self.heuristic_table[heuristic](board, side)* self.heuristics[heuristic]
        return weight
    
    def __str__(self):
        return super().__str__() + self.heuristics.values().__str__()