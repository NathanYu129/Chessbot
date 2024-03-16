import chess

# SECOND ATTEMPT AT DIDACTIC CHESS BOT
# Key changes (not in musical sense):
#   In addition to direct material evaluation, also incorporates piece-square tables from chess programming wiki
#   to attempt positional understanding
#   Generalized search function to use recursion and have variable depth
# FUTURE CHANGES:
#   Implement more sophisticated search algorithm (Minimax? Negamax?)
#   Implement some sort of pruning or search optimization method
#   Implement opening theory using Polygot
#   Integrate with uci (IMPORTANT!!!!)
#   Oh and i guess actually write that abstract bot class lol

class twoBot():

    # Tables to count piece and position value
    # Table 0 will always be material value list
    # Table 1 will always be white's positional value list
    # Table 2 will always be black's positional value list
    # should i make this a tuple cuz it never gets changed? Runs into issues with declaring what where in python
    pieceTables = []

    # Simple table, just puts in baseline material values without thinking abt position
    # Experimenting with piece value weights, currently roughly multiplying by 40 relative to base material value
    #              p   k    b    r    q    K (king)
    #              1   3    3    5    11   100
    simpleTable = [40, 120, 120, 200, 440, 4000]

    # Wiki table, puts in the baseline piece value tables from the chess programming wiki
    # https://www.chessprogramming.org/Simplified_Evaluation_Function
    # NOTE: EDITED, DO NOT COPY PASTE DIRECTLY INTO NEW BOTS, REFER BACK TO WIKI FOR BASE TABLE
    # Due to nature of list representation vs how a chessboard looks, there will be two tables.
    # Since A1 corresponds to [0] the whiteside representation will be flipped relative to the wiki
    # version, with A1 being at the top left as [0] and H8 being at the bottom right as [63]
    # And thus the BLACK version will CORRESPOND to the wiki tables, to encourage advancing into the white position,
    # whereas the  WHITE version will BE FLIPPED
    # So essentially when looking at these tables, it corresponds to looking at a board from the black perspective
    whiteTable = [
        [
            # white pawn
            0,  0,  0,  0,  0,  0,  0,  0,
            5, 10, 10,-20,-20, 10, 10,  5,
            5, -5,-10,  0,  0,-10, -5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5,  5, 10, 25, 25, 10,  5,  5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0,  0,  0,  0,  0,  0,  0,  0
        ],
        [
            # white knight
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50
        ],
        [
            # white bishop
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -20,-10,-10,-10,-10,-10,-10,-20
        ],
        [
            # white rook
            0,  0,  0,  5,  5,  0,  0,  0,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            5, 10, 10, 10, 10, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ],
        [
            # white queen
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  5,  0,  0,  0,  0,-10,
            -10,  5,  5,  5,  5,  5,  0,-10,
            0,  0,  5,  5,  5,  5,  0, -5,
            -5,  0,  5,  5,  5,  5,  0, -5,
            -10,  0,  5,  5,  5,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20,
        ],
        [
            # white king middle game
            # wiki has an endgame version, ill worry abt it later
            20, 30, 10,  0,  0, 10, 30, 20,
            20, 20,  0,  0,  0,  0, 20, 20,
            -10,-20,-20,-20,-20,-20,-20,-10,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30
        ]
    ]

    blackTable = [
        [
            # black pawn
            0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5,  5, 10, 25, 25, 10,  5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5, -5,-10,  0,  0,-10, -5,  5,
            5, 10, 10,-20,-20, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ],
        [
            # black knight
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50
        ],
        [
            # black bishop
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -20,-10,-10,-10,-10,-10,-10,-20
        ],
        [
            # black rook
            0,  0,  0,  0,  0,  0,  0,  0,
            5, 10, 10, 10, 10, 10, 10,  5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            0,  0,  0,  5,  5,  0,  0,  0
        ],
        [
            # black queen
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5,  5,  5,  5,  0,-10,
            -5,  0,  5,  5,  5,  5,  0, -5,
            0,  0,  5,  5,  5,  5,  0, -5,
            -10,  5,  5,  5,  5,  5,  0,-10,
            -10,  0,  5,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20
        ],
        [
            # black king middle game
            # same as other
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -10,-20,-20,-20,-20,-20,-20,-10,
            20, 20,  0,  0,  0,  0, 20, 20,
            20, 30, 10,  0,  0, 10, 30, 20
        ]
    ]

    # Depth to search positions at
    # Minimum val should be 2 so it at least takes into account responses
    # Change this to be input for init function?
    depth = 2

    def __init__(self):
        self.pieceTables.append(self.simpleTable)
        self.pieceTables.append(self.whiteTable)
        self.pieceTables.append(self.blackTable)

    # Evaluates the current position on the board
    # Positive value means white favored, negative black
    def evaluatePosition(self, board):
        res = 0 # 0 is draw/even
        res += self.getMat(board, chess.WHITE) + self.getPos(board, chess.WHITE)
        res -= self.getMat(board, chess.BLACK) + self.getPos(board, chess.BLACK)
        return res
    
    # Sums up the total value for a side based on table in pieceTables[0]
    def getMat(self, board, side):
        res = 0
        # Remember, p = 1, k = 2, b = 3, r = 4, q = 5, K = 6
        for n in range(0, 5):
            # Total number of a piece times its weight in the table
            res += (len(board.pieces(n + 1, side))) * self.pieceTables[0][n]
        return res

    # Calculates the positional value of a side's pieces based on tables in pieceTables[1] and [2]
    def getPos(self, board, side):
        res = 0
        index = 1 # Handling which positional table to look at as piecet[1] is white and pt[2] is black
        if not side: index = 2
        # Remember, p = 1, k = 2, b = 3, r = 4, q = 5, K = 6
        for n in range(0, 5):
            squares = board.pieces(n + 1, side)
            for square in squares:
                res += self.pieceTables[index][n][square] # adds table weight of that piece occupying that square
        return res
    
    # Main outward-facing (remember to look up what the actual term for this is again) function
    # Takes a board and returns a move for who's turn it is based on calculation depth
    def getMove(self, board):
        (move, eval) = self.think(board, self.depth)
        return move

    # Recursive helper to getMove
    # Brute-force searches legal moves to find best resulting position to a given depth
    # Returns best move for who's side, plus eval
    def think(self, board, d):
        if d == 0: return (None, self.evaluatePosition(board)) # Base case, just evaluating a resulting position
        turn = board.turn
        movepool = list(board.legal_moves)
        if movepool == []: # No legal moves
            outcome = board.outcome()
            if outcome.winner == None: return (None, 0) # Draw
            elif outcome.winner: return (None, 999999)  # White wins
            else: return (None, -999999)                # Black wins
        bestWEval = -999999 # start off on worst possible values for each side
        bestBEval = 999999
        bestWMove = None # which move produces most positive eval delta
        bestBMove = None # which move produces most negative eval delta
        for move in movepool:
            board.push(move)
            (m, e) = self.think(board, d - 1)
            board.pop()
            if e >= bestWEval:
                bestWEval = e
                bestWMove = move
            if e <= bestBEval:
                bestBEval = e
                bestBMove = move
        if board.turn: return (bestWMove, bestWEval)
        else:          return (bestBMove, bestBEval)