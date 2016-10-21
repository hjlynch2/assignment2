# By convention, white always goes first
# TO-DO:
# -Improve defensive heuristic
# -Improve offensive heuristic
# -Maybe, improve the ordering of ABPruning
from copy import deepcopy
import argparse
import sys
import time
import numpy as np
import math

class BreakthroughGame:
    def __init__(self, matchup, heuristic): #)
        self.board = []
        self.score = {'b': 16, 'w': 16}
        with open('board.txt') as textFile:
            lines = [line.split() for line in textFile]
            self.board = lines

    def makeMove(self, prevloc, newloc, agent):
        try:
            if (agent == 'b' and self.board[newloc[0]][newloc[1]] == 'w'):
                self.score['w'] -= 1
            if (agent == 'w' and self.board[newloc[0]][newloc[1]] == 'b'):
                self.score['b'] -= 1
            self.board[newloc[0]][newloc[1]] = agent
            self.board[prevloc[0]][prevloc[1]] = '-'
        except: pass
        return

# "Generally, an effective offensive strategy is to recognize
# and attack "pivotal" pieces which are in positions to block
# multiple routes to victory. An effective defense is to
# arrange multiple blocking pieces in a blocking pattern
# (since a single defending piece can not effectively block
# a single attacking piece)."
# - https://en.wikipedia.org/wiki/Breakthrough_(board_game)

    def offensive(self, agent, opponent): #CHANGE THIS
        return (self.score[agent] - self.score[opponent])

    def defensive(self, agent, opponent): #CHANGE THIS
        return (self.score[opponent] - self.score[agent])

    def generateMoves(self, agent):
        available_moves = []
        if(agent == 'w'):
            for idy in range(len(self.board)):
                for idx in range(len(self.board[idy])):
                    if (self.board[idy][idx] == 'w'):
                        try:
                            forward = [(idy,idx),(idy-1,idx)]
                            if(idy-1 >= 0):
                                if(self.board[forward[1][0]][forward[1][1]] == '-'):
                                    available_moves.append(forward)
                        except: pass
                        try:
                            left_diagonal = [(idy,idx),(idy-1,idx-1)]
                            if(idx-1 >= 0 and idy-1 >= 0):
                                if(self.board[left_diagonal[1][0]][left_diagonal[1][1]] == '-' or self.board[left_diagonal[1][0]][left_diagonal[1][1]] == 'b'):
                                    available_moves.append(left_diagonal)
                        except: pass
                        try:
                            right_diagonal = [(idy,idx),(idy-1,idx+1)]
                            if(idy-1 >= 0):
                                if(self.board[right_diagonal[1][0]][right_diagonal[1][1]] == '-' or self.board[right_diagonal[1][0]][right_diagonal[1][1]] == 'b'):
                                    available_moves.append(right_diagonal)
                        except: pass
        if(agent == 'b'):
            for idy in range(len(self.board)):
                for idx in range(len(self.board[idy])):
                    if (self.board[idy][idx] == 'b'):
                        try:
                            forward = [(idy,idx),(idy+1,idx)]
                            if(self.board[forward[1][0]][forward[1][1]] == '-'):
                                available_moves.append(forward)
                        except: pass
                        try:
                            left_diagonal = [(idy,idx),(idy+1,idx+1)]
                            if(self.board[left_diagonal[1][0]][left_diagonal[1][1]] == '-' or self.board[left_diagonal[1][0]][left_diagonal[1][1]] == 'w'):
                                available_moves.append(left_diagonal)
                        except: pass
                        try:
                            right_diagonal = [(idy,idx),(idy+1,idx-1)]
                            if(idx-1 >= 0):
                                if(self.board[right_diagonal[1][0]][right_diagonal[1][1]] == '-' or self.board[right_diagonal[1][0]][right_diagonal[1][1]] == 'w'):
                                    available_moves.append(right_diagonal)
                        except: pass
        return available_moves

def miniMax(game, agent, opponent, max_player, depth, heuristic, move=None):
    if(depth == 0 or 'b' in game.board[7] or 'w' in game.board[0] or game.score['b'] == 0 or game.score['w'] == 0):
        if(heuristic == 'ovd'): return (game.offensive(agent, opponent) if max_player else game.defensive(agent, opponent), move)
        if(heuristic == 'dvo'): return (game.defensive(agent, opponent) if max_player else game.offensive(agent, opponent), move)
        if(heuristic == 'ovo'): return (game.offensive(agent, opponent) if max_player else game.offensive(agent, opponent), move)
        if(heuristic == 'dvd'): return (game.defensive(agent, opponent) if max_player else game.defensive(agent, opponent), move)
    max_value = -sys.maxsize - 1
    min_value = sys.maxsize
    best_move = [(-1,-1),(-1,-1)]
    moves_available = game.generateMoves(agent)
    for available in moves_available:
        game_copy = deepcopy(game)
        miniMax.nodes += 1
        game_copy.makeMove(available[0], available[1], agent)
        move_score = miniMax(game_copy, opponent, agent, not max_player, depth-1, heuristic, available)
        if max_player:
            if move_score[0] > max_value:
                max_value = move_score[0]
                best_move = available
        else:
            if move_score[0] < min_value:
                min_value = move_score[0]
                best_move = available
    return (max_value if max_player else min_value, best_move)

def ABPruning(game, agent, opponent, max_player, depth, alpha, beta, heuristic, move=0):
    if(depth == 0 or 'b' in game.board[7] or 'w' in game.board[0] or game.score['b'] == 0 or game.score['w'] == 0):
        if(heuristic == 'ovd'): return (game.offensive(agent, opponent) if max_player else game.defensive(agent, opponent), move)
        if(heuristic == 'dvo'): return (game.defensive(agent, opponent) if max_player else game.offensive(agent, opponent), move)
        if(heuristic == 'ovo'): return (game.offensive(agent, opponent) if max_player else game.offensive(agent, opponent), move)
        if(heuristic == 'dvd'): return (game.defensive(agent, opponent) if max_player else game.defensive(agent, opponent), move)
    best_move = [(-1,-1),(-1,-1)]
    moves_available = game.generateMoves(agent)
    for available in moves_available:
        game_copy = deepcopy(game)
        ABPruning.nodes += 1
        game_copy.makeMove(available[0], available[1], agent)
        move_score = ABPruning(game_copy, opponent, agent, not max_player, depth-1, alpha, beta, heuristic, available)
        if max_player:
            if move_score[0] > alpha:
                alpha = move_score[0]
                best_move = available
                if(alpha >= beta): break
        else:
            if move_score[0] < beta:
                beta = move_score[0]
                best_move = available
                if(alpha >= beta): break
    return (alpha if max_player else beta, best_move)

def simulate(game, matchup, heuristic):
    expanded_nodes = {'b': [], 'w': []}
    move_time = {'b': [], 'w': []}
    current_team = 'w'
    opponent_team = 'b'
    total_moves = 0
    if(matchup == 'mvm'):
        max_player = True

        while('b' not in game.board[7] or 'w' not in game.board[0] or game.score['b'] > 0 or game.score['w'] > 0):
            start_time = time.time()
            miniMax.nodes = 0

            result = miniMax(game, current_team, opponent_team, max_player, 3, heuristic)
            if(result[1] == None): break
            game.makeMove(result[1][0], result[1][1], current_team)

            for row in game.board: print('  '.join(row))
            print("Move:", result[1][0], "->", result[1][1])
            print(miniMax.nodes, "nodes expanded by", current_team)
            expanded_nodes[current_team].append(miniMax.nodes)
            final_time = time.time() - start_time
            print("Move Time: %s seconds" % final_time)
            move_time[current_team].append(final_time)
            total_moves += 1

            current_team, opponent_team = opponent_team, current_team

    if(matchup == 'ava'):
        max_player = True

        while('b' not in game.board[7] or 'w' not in game.board[0] or game.score['b'] > 0 or game.score['w'] > 0):
            start_time = time.time()
            ABPruning.nodes = 0

            result = ABPruning(game, current_team, opponent_team, max_player, 3, -100000, 100000, heuristic)
            if(result[1] == None): break
            try: game.makeMove(result[1][0], result[1][1], current_team)
            except: break

            for row in game.board: print('  '.join(row))
            print("Move:", result[1][0], "->", result[1][1])
            print(ABPruning.nodes, "nodes expanded by", current_team)
            expanded_nodes[current_team].append(ABPruning.nodes)
            final_time = time.time() - start_time
            print("Move Time: %s seconds" % final_time)
            move_time[current_team].append(final_time)
            total_moves += 1

            current_team, opponent_team = opponent_team, current_team

    if(matchup == 'mva'):
        max_player = True

        while('b' not in game.board[7] or 'w' not in game.board[0] or game.score['b'] > 0 or game.score['w'] > 0):
            start_time = time.time()
            miniMax.nodes = 0
            ABPruning.nodes = 0

            if(current_team == 'w'):
                result = miniMax(game, current_team, opponent_team, max_player, 3, heuristic)
            if(current_team == 'b'):
                result = ABPruning(game, current_team, opponent_team, max_player, 3, -100000, 100000, heuristic)
            if(result[1] == None): break

            try: game.makeMove(result[1][0], result[1][1], current_team)
            except: break

            for row in game.board: print('  '.join(row))
            print("Move:", result[1][0], "->", result[1][1])
            if(current_team == 'w'):
                print(miniMax.nodes, "nodes expanded by", current_team)
                expanded_nodes[current_team].append(miniMax.nodes)
            if(current_team == 'b'):
                print(ABPruning.nodes, "nodes expanded by", current_team)
                expanded_nodes[current_team].append(ABPruning.nodes)
            final_time = time.time() - start_time
            print("Move Time: %s seconds" % final_time)
            move_time[current_team].append(final_time)
            total_moves += 1

            current_team, opponent_team = opponent_team, current_team

    if(matchup == 'avm'):
        max_player = True

        while('b' not in game.board[7] or 'w' not in game.board[0] or game.score['b'] > 0 or game.score['w'] > 0):
            start_time = time.time()
            miniMax.nodes = 0
            ABPruning.nodes = 0

            if(current_team == 'w'):
                result = ABPruning(game, current_team, opponent_team, max_player, 3, -100000, 100000, heuristic)
            if(current_team == 'b'):
                result = miniMax(game, current_team, opponent_team, max_player, 3, heuristic)
            if(result[1] == None): break

            try: game.makeMove(result[1][0], result[1][1], current_team)
            except: break

            for row in game.board: print('  '.join(row))
            print("Move:", result[1][0], "->", result[1][1])
            if(current_team == 'b'):
                print(miniMax.nodes, "nodes expanded by", current_team)
                expanded_nodes[current_team].append(miniMax.nodes)
            if(current_team == 'w'):
                print(ABPruning.nodes, "nodes expanded by", current_team)
                expanded_nodes[current_team].append(ABPruning.nodes)
            final_time = time.time() - start_time
            print("Move Time: %s seconds" % final_time)
            move_time[current_team].append(final_time)
            total_moves += 1

            current_team, opponent_team = opponent_team, current_team

    print('----------------------------------------------------------')
    print('Total Expanded Nodes by White:', sum(expanded_nodes['w']))
    print('Total Expanded Nodes by Black:', sum(expanded_nodes['b']))
    print('White Average Nodes Expanded Per Move:', np.mean(expanded_nodes['w']))
    print('Black Average Nodes Expanded Per Move:', np.mean(expanded_nodes['b']))
    print('White Average Time Per Move:', np.mean(move_time['w']))
    print('Black Average Time Per Move:', np.mean(move_time['b']))
    print('Number of Workers Captured by White:', 16-game.score['b'])
    print('Number of Workers Captured by Black:', 16-game.score['w'])
    print('Total Moves Until Win:', total_moves)
    for row in game.board: print('  '.join(row))
    if('b' in game.board[7] or game.score['w'] == 0):
        print("Black Wins!")
        return
    if('w' in game.board[7] or game.score['b'] == 0):
        print("White Wins!")
        return
    return

def main():
    parser = argparse.ArgumentParser(description = "Play Breakthrough")
    parser.add_argument('matchup', help = "mvm, ava, mva, or avm?")
    parser.add_argument('heuristic', help = "ovd, dvo, ovo, or dvd?")
    #parser.add_argument('part', help = "2.1 or 2.2?")
    args = parser.parse_args()

    bt = BreakthroughGame(args.matchup, args.heuristic)
    #bt = BreakthroughGame(args.matchup, args.heuristic, args.part)
    print("Playing Breakthrough on mode", args.matchup, args.heuristic)
    #print("Playing Breakthrough on mode", args.matchup, args.heuristic, args.part)
    simulate(bt, args.matchup, args.heuristic)
    #simulate(bt, args.matchup, args.heuristic, args.part)

if __name__ == "__main__":
    main()
