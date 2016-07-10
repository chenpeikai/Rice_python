"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

# Add your functions here.
def mc_trial(board, player):
    '''the function make trial in the board untill someone win'''
    statues = board.check_win()
    if statues == None:
        empty = board.get_empty_squares()
        random_index = random.randrange(0 , len(empty))
        board.move(empty[random_index][0] , empty[random_index][1] , player)
        
        # Recursion
        player = provided.switch_player(player)
        return mc_trial(board , player)
    else:
        return statues

def mc_update_scores(scores, board, player):
    '''the function updata the scores according the board and the curplayer'''
    dim = board.get_dim()
    table = {provided.EMPTY:0}
    winner = board.check_win()
    if winner == player:
        table[player] = SCORE_CURRENT
        table[provided.switch_player(player)] = -SCORE_OTHER
    elif winner == provided.switch_player(player):
        table[player] = -SCORE_CURRENT
        table[provided.switch_player(player)] = SCORE_OTHER
    else:
        table[player] = 0
        table[provided.switch_player(player)] = 0
    for row in range(dim):
        for col in range(dim):
            name = board.square(row,col)
            scores[row][col] += table[name]
                
def get_best_move(board, scores):
    '''the function take the board and get the best move according the scores'''
    max_score = -float('inf')
    max_index = []
    for index in board.get_empty_squares():
        if scores[index[0]][index[1]] > max_score:
            max_index = [index]
            max_score = scores[index[0]][index[1]]
        elif scores[index[0]][index[1]] == max_score:
            max_index.append(index)
    random_index = random.randrange(len(max_index))
    return max_index[random_index]

def mc_move(board, curplayer, ntrials):
    '''the function take board and make a  Monte Carlo simulation by the ntrials,
    then get the best move'''
    dim = board.get_dim()
    scores = [[0 for _ in range(dim)]
              for _ in range(dim)]
    for _ in range(ntrials):
        test_board = board.clone()
        mc_trial(test_board , curplayer)
        mc_update_scores(scores, test_board, curplayer)
    return get_best_move(board , scores)

        
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.
#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(4, provided.PLAYERX, mc_move, NTRIALS, False)
