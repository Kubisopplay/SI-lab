import random
from game import Board, second_side
import multiprocessing as mp
import numpy as np
class Node:
    def __init__(self, board: Board, side: int,  move:tuple) -> None:
        self.board = board
        self.side = side
        self.move = move #move that led to this node
        self.children = []
        self.weight = 0
    
    def add_children(self, children: list):
        self.children.extend(children)
        
    


    
class Ai_Base:
    def __init__(self) -> None:
        pass

    def get_move(self, board: Board, side: int, valid_moves: list) -> tuple:
        pass
    
    def calculate_weight(self, board: Board, side: int, move: tuple):
        pass
    
    def create_decision_tree(self, board: Board, side: int, depth: int):
        pass
    
    def __str__(self):
        return self.__class__.__name__
    


class Ai_Random(Ai_Base):
    def get_move(self, board: Board, side: int, valid_moves: list) -> tuple:
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

    def get_move(self, board: Board, side: int, valid_moves: list) -> tuple:
        root = Node(board,side,None)
        self.minmax(root, self.depth, side)
        tree = root.children
        tree.sort(key=lambda x: x.weight, reverse=True)
        if len(tree) > 0:
            return tree[0].move
        else: None
        
    
    def calculate_weight(self, board: Board, side: int, move: tuple):
        return self.heuristic1(board, side)
    
    def minmax(self,node, depth: int, starting_side: int = 0):
        if depth == 0:
            return self.heuristic1(node.board, node.side)
        if node.board.is_ended():
            return self.heuristic1(node.board, node.side)
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



class ABPruning(Ai_MinMaxBase):
    
    def get_move(self, board: Board, side: int, valid_moves: list) -> tuple:
        self.alpha = -np.inf
        self.beta = np.inf
        return super().get_move(board, side, valid_moves)
    

    def minmax(self,node, depth: int, starting_side: int = 0):
        if depth == 0:
            return self.heuristic1(node.board, node.side)
        if node.board.is_ended():
            return self.heuristic1(node.board, node.side)
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