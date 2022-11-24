import random


Score = {'K': 0, "P": 1, "H": 3, "B": 3, "R": 5, "Q": 9}                                                                # per piece there's a score,king = 0, as no one can actually take the king
CHECKMATE = 100                                                                                                         # if you lead to checkmate you win
STALEMATE = 0                                                                                                           # if you're winning you'll try to avoid getting 0, if you're losing you'll try to get 0 or higher
DEPTH = 2                                                                                                               # nr of moves AI thinks ahead


def findRandomMove(validMoves):                                                                                         # returns a random move
    if len(validMoves) > 0:
        return validMoves[random.randint(0, len(validMoves) - 1)]


def aiMove(game, validMoves):                                                                                           # finds the next best move
    global nextMove                                                                                                     # stores the next move here
    nextMove = None
    random.shuffle(validMoves)                                                                                          # bug found, randomizing moves seems to do the trick
    AlphaBetaPruning(game, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if game.whiteToMove else -1)                     # uses AlphaBetaPruning
    return nextMove                                                                                                     # returns the next best move


def AlphaBetaPruning(game, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * boardScore(game)
    maxScore = -CHECKMATE                                                                                               # start from the bottom
    for move in validMoves:                                                                                             # looks at all moves ahead by depth and makes them
        game.makeMove(move)
        nextMoves = game.getValidMoves()
        score = -AlphaBetaPruning(game, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)                             # each move will have a score by adding all pieces left on the board
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        game.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def boardScore(game):                                                                                                   # sees the pieces as the score, not as objects
    if game.checkMate:
        if game.whiteToMove:
            return -CHECKMATE                                                                                           # black won
        else:
            return CHECKMATE                                                                                            # white won
    if game.staleMate:
        return STALEMATE                                                                                                # draw by stalemate
    score = 0
    for row in game.board:                                                                                              # adds up the scores for white and black pieces
        for square in row:
            if square[0] == 'w':
                score += Score[square[1]]                                                                               # for each piece adds the piece's score for white
            elif square[0] == 'b':
                score -= Score[square[1]]                                                                               # for each piece adds the piece's score for white
    return score
