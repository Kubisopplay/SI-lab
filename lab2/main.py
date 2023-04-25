from game import Game
from ai import Ai_Random, Ai_MinMaxBase
import random
import cProfile
import multiprocessing as mp



random.seed(2137)
game = Game()

players = {}
players[Ai_Random()] = 0
players[Ai_MinMaxBase(1)] = 0
players[Ai_MinMaxBase(2)] = 0
players[Ai_MinMaxBase(3)] = 0
 



#game.setupPlayers(Ai_MinMaxBase(3), Ai_MinMaxBase(3))
#result = game.play()


def benchmark():
    number = 0
    for i in range(1):
        for player1 in players.keys():
            for player2 in players.keys():
                number += 1
                print(player1 , " vs ", player2, " number ", number)
                game.setupPlayers(player1, player2)
                result = game.play()
                if result[0] > result[1]:
                    players[player1] += 1
                elif result[0] < result[1]:
                    players[player2] += 1
    
#benchmark()
cProfile.run('benchmark()') 

for player, score in players.items():
    print(str(player), score)