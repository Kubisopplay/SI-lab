import random
from game import Board, Move, second_side
import multiprocessing as mp

class Node:
    def __init__(self, board: Board, side: int,  move:Move,depth: int) -> None:
        self.board = board
        self.side = side
        self.depth = depth
        self.move = move
        self.children = []
        self.weight = 0
    
    def add_children(self, children: list):
        self.children.extend(children)
        
    


    
class Ai_Base:
    def __init__(self) -> None:
        pass

    def get_move(self, board: Board, side: int, valid_moves: list) -> Move:
        pass
    
    def calculate_weight(self, board: Board, side: int, move: Move):
        pass
    
    def create_decision_tree(self, board: Board, side: int, depth: int):
        pass
    
    def __str__(self):
        return self.__class__.__name__
    


class Ai_Random(Ai_Base):
    def get_move(self, board: Board, side: int, valid_moves: list) -> Move:
        return random.choice(valid_moves)
    

class Ai_MinMaxBase(Ai_Base):
    def __init__(self, depth: int) -> None:
        super().__init__()
        self.depth = depth
        self.tree = None
 
    def __str__(self):
        return super().__str__() + f"({self.depth})"

    def get_move(self, board: Board, side: int, valid_moves: list) -> Move:
        tree = self.create_decision_tree(board, side, self.depth)
        tree.sort(key=lambda x: x.weight, reverse=True)
        if len(tree) > 0:
            return tree[0].move
        else: None
        
    
    def calculate_weight(self, board: Board, side: int, move: Move):
        return len(move.affected_stones)
    
    def create_decision_tree(self, board: Board, side: int, depth: int):
        children = []
        moves = board.get_valid_moves(side)
        for move in moves:
            node = Node(board.copy(), second_side(side),move, depth)
            node.board.do_move(move, side)
            node.weight = self.calculate_weight(board, side, move)
            if depth > 1:
                node.add_children(self.create_decision_tree(node.board, node.side, depth-1))
                node.weight -= sum([child.weight for child in node.children])
            #Stack overflow incoming, but i cba to fix it. 
            children.append(node)
        return children

