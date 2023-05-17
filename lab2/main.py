import time
from game import Game
from ai import Ai_Random, Ai_MinMaxBase, ABPruning,TestPruning
import random
import cProfile
import multiprocessing as mp



random.seed(2137)
game = Game()

players = {}

for i in range(1, 7):
    temp={}
    for j in range(1, 7):
        temp["heuristic"+str(j)]=0
    temp["heuristic1"]=1
    temp["heuristic"+str(i)]=1 
    players[TestPruning(3,temp)]=(0,0)


#game.setupPlayers(Ai_MinMaxBase(3), Ai_MinMaxBase(3))
#result = game.play()


def benchmark():
    number = 0
    start_time = time.time()
    for i in range(1):
        for player1 in players.keys():
            for player2 in players.keys():
                number += 1
                print(player1 , " vs ", player2, " number ", number)
                game.setupPlayers(player1, player2)
                result = game.play()
                if result[0] > result[1]:
                    players[player1] = (players[player1][0] + 1, players[player1][1])
                elif result[0] < result[1]:
                    players[player2] = (players[player2][0] + 1, players[player2][1])
                players[player1] = (players[player1][0], player1.total_time/player1.total_moves)
                players[player2] = (players[player2][0], player2.total_time/player2.total_moves)
    print("time: ", time.time() - start_time)
benchmark()
#cProfile.run('benchmark()') 

game.setupPlayers(Ai_MinMaxBase(1), ABPruning(5))
#result = game.play()
#print(result)
print("AI_name, wins, avg time")
for player, score in players.items():
    print(str(player), score)