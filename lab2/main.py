import time
from game import Game
from ai import Ai_Random, Ai_MinMaxBase, ABPruning
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
players[ABPruning(4)] = 0



#game.setupPlayers(Ai_MinMaxBase(3), Ai_MinMaxBase(3))
#result = game.play()


def benchmark():
    number = 0
    start_time = time.time()
    for i in range(5):
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
    print("time: ", time.time() - start_time)
#benchmark()
#cProfile.run('benchmark()') 

game.setupPlayers(Ai_MinMaxBase(1), ABPruning(5))
result = game.play()
print(result)

for player, score in players.items():
    print(str(player), score)