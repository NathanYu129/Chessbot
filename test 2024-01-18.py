
# UGLY INITIAL TESTING AREA FOR BOTS
# WILL LATER CLEAN THIS UP/INTEGRATE WITH UCI TO JUST USE ONLINE INTERFACES

import chess

#from testBot import tBot
from testBot2 import twoBot
# from supervisedBot import sBot

# CONVERT TO UCI LATER
# For the moment, bots are simply defined as having a single function getMove(Board board,bool turn) which
# Intakes a position, and returns a move for the side who's turn it is
# Remember to make abstract generalizable bot class at some point
bot = twoBot()

# Checks whether or not the game has ended, and gives appropriate output
# Will update to actually list conditions of outcome like cause/winning side
# atm will just return that the game ended and the winning side
def handleGameOver(b):
    outcome = b.outcome()
    if outcome == None: return False
    winner = outcome.winner
    if winner:
        print("White wins")
        return True
    if not winner: #could be an else rn, but leave like this to accomodate more detailed output later
        print("Black wins")
        return True
    else:
        return False

def playChess():
    board = chess.Board()

    # True = white to move, False = black to move
    turn = board.turn

    print("Please input all moves in uci (ex. \"e2e4\")")
    print(board)

    while(True):
        #Check if game is over, print appropriate result
        if handleGameOver(board): break

        #Get move
        move = ""
        while(True):
            try:
                if turn:
                    #move = input("White to move: ")
                    move = chess.Move.uci(bot.getMove(board))
                    print(move)
                else:
                    move = input("Black to move: ")

                #check if im tryna halt the execution
                if move == "halt": break
            
                #attempt to play move
                board.push_uci(move)

                #if move was legal:
                turn = not turn
                break
            except chess.IllegalMoveError:
                print("Illegal move, try again")
            except ValueError:
                print("Invalid input that is not halt, try again")

        #break out of outer loop
        if move == "halt": break
        #Display board
        print(board)


playChess()