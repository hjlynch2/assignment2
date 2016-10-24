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
from random import randint

class BreakthroughGame:
    def __init__(self, matchup, heuristic): 
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

    def offensive(self, orig_game, agent, opponent): #CHANGE THIS
        num_agents = self.count_nums(agent, self.board)
        num_opponents = self.count_nums(opponent, self.board)

        #Param 1 is the number of opponents killed
        num_opponents_killed = self.count_nums(opponent, orig_game.board) - num_agents

        #Param 2 is how close we are to the end
        agent_dist_to_end = self.find_dist_to_end(agent, self.board)
        agent_old_dist = self.find_dist_to_end(agent, orig_game.board)
        dist_changed = agent_dist_to_end - agent_old_dist

        #Param 3 is how many lanes we have to get to the end
        num_open_lanes = self.find_lanes_to_end(agent, self.board)

        #Param 4 is how close the opponent is to winning
        opponent_dist_to_end = self.find_dist_to_end(opponent, self.board)
        diff_dist = agent_dist_to_end - opponent_dist_to_end

        #Param 5 is average distance to the end
        avg_dist_changed = self.find_avg_dist_to_end(agent, self.board) - self.find_avg_dist_to_end(agent, orig_game.board)

        #Param 6 is whether a win is imminent
        is_win_there = self.check_if_win(agent, self.board)
        is_win_almost_there = self.check_if_win_imminent(agent, self.board)

        opponent_win = self.check_if_win(opponent, self.board)
        opponent_imminent = self.check_if_win_imminent(opponent, self.board)

        return (5*num_opponents_killed + 5*(7-agent_dist_to_end) + avg_dist_changed + .5*num_open_lanes - diff_dist) + 1000*(is_win_there) + 500*(is_win_almost_there) - 100000*(opponent_win) - 1000*(opponent_imminent)


    def defensive(self, orig_game, agent, opponent): #CHANGE THIS
        num_agents = self.count_nums(agent, self.board)
        num_opponents = self.count_nums(opponent, self.board)

        #Param 1 is the number of opponents killed
        num_opponents_killed = self.count_nums(opponent, orig_game.board) - num_agents

        #Param 2 is how close we are to the end
        agent_dist_to_end = self.find_dist_to_end(agent, self.board)
        agent_old_dist = self.find_dist_to_end(agent, orig_game.board)
        dist_changed = agent_dist_to_end - agent_old_dist

        #Param 3 is how many lanes the opponent has to the end
        opponent_open_lanes = self.find_lanes_to_end(opponent, self.board)

        #Param 4 is how close the opponent is to winning
        opponent_dist_to_end = self.find_dist_to_end(opponent, self.board)
        diff_dist = agent_dist_to_end - opponent_dist_to_end

        #Param 5 is average distance to the end
        avg_dist_changed = self.find_avg_dist_to_end(agent, self.board) - self.find_avg_dist_to_end(agent, orig_game.board)

        return (num_opponents_killed + 2*(7-agent_dist_to_end) + avg_dist_changed - 2*opponent_open_lanes - diff_dist)


    def count_nums(self, color, board):
        count = 0
        for x in range(0, len(board)):
            for y in range(0, len(board[0])):
                if board[x][y] == color:
                    count += 1
        return count

    #Finds the minimum distance to the end
    def find_dist_to_end(self, color, board):
        dist = 10000 #initialize to large num
        if color == 'b':
            end_goal = 7
        else:
            end_goal = 0
        dist_sum = 0
        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                if(board[i][j] == color):
                    new_dist = abs(i - end_goal)
                    dist = min(dist, new_dist)
        return dist

    #Find avg distance to end
    def find_avg_dist_to_end(self, color, board):
        dist = 0
        num_pieces = 0
        if color == 'b':
            end_goal = 7
        else:
            end_goal = 0
        dist_sum = 0
        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                if(board[i][j] == color):
                    dist += abs(i - end_goal)
                    num_pieces += 1
        return float(dist)/num_pieces

    def find_lanes_to_end(self, color, board):
        num_lanes = 0
        if color == 'b':
            end_goal = 7
        else:
            end_goal = 0
        for i in range(0, len(board)):
            for j in range(0, len(board[0])):
                if(board[i][j] == color):
                    num_lanes += self.find_lanes(color, i, j, end_goal, board)
        return num_lanes

    def check_if_win(self, color, board):
        if color == 'b':
            end_goal = 7
        else:
            end_goal = 0

        return color in board[end_goal]

    def check_if_win_imminent(self, color, board):
        if color == 'b':
            pre_goal = 6
        else:
            pre_goal = 1

        return color in board[pre_goal]


    def find_lanes(self, color, cur_i, cur_j, end_row, board):
        res = 3
        if color == 'b':
            enemy = 'w'
            start = cur_i
            end = end_row
        else:
            enemy = 'b'
            start = end_row
            end = cur_i

        # Look straight ahead
        for x in range(start, end+1):
            if(board[x][cur_j] == enemy):
                res -= 1
                break

        #Look in the left lane
        if cur_j > 0:
            for x in range(start, end+1):
                if(board[x][cur_j-1] == enemy):
                    res -= 1
                    break
        else:
            res -= 1

        #Look in the right lane
        if cur_j < 7:
            for x in range(start, end+1):
                if(board[x][cur_j+1] == enemy):
                    res -= 1
                    break
        else:
            res -= 1

        return res


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

def miniMax(game, orig_game, agent, opponent, max_player, depth, heuristic, move=None):
    if(depth == 0 or 'b' in game.board[7] or 'w' in game.board[0] or game.score['b'] == 0 or game.score['w'] == 0):
        if(heuristic == 'ovd'): return (game.offensive(orig_game, agent, opponent) if max_player else game.defensive(orig_game, agent, opponent), move)
        if(heuristic == 'dvo'): return (game.defensive(orig_game, agent, opponent) if max_player else game.offensive(orig_game, agent, opponent), move)
        if(heuristic == 'ovo'): return (game.offensive(orig_game, agent, opponent) if max_player else game.offensive(orig_game, agent, opponent), move)
        if(heuristic == 'dvd'): return (game.defensive(orig_game, agent, opponent) if max_player else game.defensive(orig_game, agent, opponent), move)
    max_value = -sys.maxsize - 1
    min_value = sys.maxsize
    best_move = [(-1,-1),(-1,-1)]
    moves_available = game.generateMoves(agent)
    for available in moves_available:
        game_copy = deepcopy(game)
        miniMax.nodes += 1
        game_copy.makeMove(available[0], available[1], agent)
        move_score = miniMax(game_copy, orig_game, opponent, agent, not max_player, depth-1, heuristic, available)
        if max_player:
            if move_score[0] > max_value:
                max_value = move_score[0]
                best_move = available
        else:
            if move_score[0] < min_value:
                min_value = move_score[0]
                best_move = available
    return (max_value if max_player else min_value, best_move)

def ABPruning(game, orig_game, agent, opponent, max_player, depth, alpha, beta, heuristic, move=0):
    if(depth == 0 or 'b' in game.board[7] or 'w' in game.board[0] or game.score['b'] == 0 or game.score['w'] == 0):
        if(heuristic == 'ovd'): return (game.offensive(orig_game, agent, opponent) if max_player else game.defensive(orig_game, agent, opponent), move)
        if(heuristic == 'dvo'): return (game.defensive(orig_game, agent, opponent) if max_player else game.offensive(orig_game, agent, opponent), move)
        if(heuristic == 'ovo'): return (game.offensive(orig_game, agent, opponent) if max_player else game.offensive(orig_game, agent, opponent), move)
        if(heuristic == 'dvd'): return (game.defensive(orig_game, agent, opponent) if max_player else game.defensive(orig_game, agent, opponent), move)
    best_move = [(-1,-1),(-1,-1)]
    moves_available = game.generateMoves(agent)
    for available in moves_available:
        game_copy = deepcopy(game)
        ABPruning.nodes += 1
        game_copy.makeMove(available[0], available[1], agent)
        move_score = ABPruning(game_copy, orig_game, opponent, agent, not max_player, depth-1, alpha, beta, heuristic, available)
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

            result = miniMax(game, game, current_team, opponent_team, max_player, 3, heuristic)
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

            result = ABPruning(game, game, current_team, opponent_team, max_player, 3, -100000, 100000, heuristic)
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
                result = miniMax(game, game, current_team, opponent_team, max_player, 3, heuristic)
            if(current_team == 'b'):
                result = ABPruning(game, game, current_team, opponent_team, max_player, 3, -100000, 100000, heuristic)
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
                result = ABPruning(game, game, current_team, opponent_team, max_player, 3, -100000, 100000, heuristic)
            if(current_team == 'b'):
                result = miniMax(game, game, current_team, opponent_team, max_player, 3, heuristic)
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
