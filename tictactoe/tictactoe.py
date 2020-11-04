"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None



def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_counter = 0
    o_counter = 0
    for i in board:
        for j in i:
            if (j == X or j == "X"):
                x_counter = x_counter + 1
            if (j == O or j == "O"):
                o_counter = o_counter + 1           
    if (x_counter == 0 and o_counter == 0):
        return X
    else:
        if (x_counter > o_counter):
            return O
        else:
            return X           

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for i in range(0, 3):
        temp = board[i]
        for j in range(0, 3):
            if (temp[j] == EMPTY or temp[j] == None):
                actions.append((i, j))

    return actions            

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    tempBoard = copy.deepcopy(board)
    if (player(board) == X):
        tempBoard[action[0]][action[1]] = X

    elif (player(board) == O):
        tempBoard[action[0]][action[1]] = O

    else:
        tempBoard[action[0]][action[1]] = X

    return tempBoard   

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    if (terminal(board) == False):
        return EMPTY
    else:
        for i in range(0, 3):
            if (board[i][0] == board[i][1] == board[i][2]):
                if (board[i][0] == X):
                    return X
                elif (board[i][0] == O):
                    return O 
            if (board[0][i] == board[1][i] == board[2][i]):
                if (board[0][i] == X):
                    return X
                elif (board[0][i] == O):
                    return O

        if (board[0][0] == board[1][1] == board[2][2]):
            if (board[0][0] == X):
                return X
            if (board[0][0] == O):
                return O

        if (board[0][2] == board[1][1] == board[2][0]):
            if (board[0][2] == X):
                return X 
            if (board[0][2] == O):
                return O

        return EMPTY                                                             

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #Check for verticle lines
    if board[0][0] == board[1][0] == board[2][0] and board[0][0] != EMPTY: 
        return True
    if board[0][1] == board[1][1] == board[2][1] and board[0][1] != EMPTY: 
        return True
    if board[0][2] == board[1][2] == board[2][2] and board[0][2] != EMPTY: 
        return True

    #Check for horizontal lines
    if board[0][0] == board[0][1] == board[0][2] and board[0][0] != EMPTY:
        return True
    if board[1][0] == board[1][1] == board[1][2] and board[1][0] != EMPTY:
        return True
    if board[2][0] == board[2][1] == board[2][2] and board[2][0] != EMPTY:
        return True

    #Checks for diagonal lines    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return True
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:                            
        return True

    check = True    
    for i in board:
        for j in i:
            if (j == EMPTY):
                check = False

    return check    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if (winner(board) == X):
        return 1
    elif (winner(board) == O):
        return -1
    elif (winner(board) == EMPTY):
        return 0
    else:
        return 0               

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if (terminal(board) == True):
        return None
    else:
        bestScore = 1
        bestPlay = ()
        for play in actions(board):
            score = Min(result(board, play))
            if score < bestScore:
                bestScore = score
                bestPlay = play
        return bestPlay        

def Min(board):
    if (terminal(board) == True):
        return utility(board)
    else:
        bestMinScore = 1
        for play in actions(board):
            bestMinScore = min(bestMinScore, Max(result(board, play)))
        return bestMinScore 

def Max(board):
    if (terminal(board) == True):
        return utility(board)
    else:
        bestMaxScore = -1
        for play in actions(board):
            bestMaxScore = max(bestMaxScore, Min(result(board, play)))
        return bestMaxScore                    

