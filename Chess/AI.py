import random


pieceScore = {'K': 0, "P": 1, "H": 3, "B": 3, "R": 5, "Q": 9}                                                           # per piece there's a score,king = 0, as no one can actually take the king
CHECKMATE = 1000                                                                                                        # if you lead to checkmate you win
STALEMATE = 0                                                                                                           # if you're winning you'll try to avoid getting 0, if you're losing you'll try to get 0 or higher
DEPTH = 2                                                                                                               # depth for recursive calls


def findRandomMove(validMoves):
    if len(validMoves) > 0:
        return validMoves[random.randint(0, len(validMoves) - 1)]


def findBestMoveYEP(gs, validMoves):
    global nextMove                                                                                                     # to find the next move
    nextMove = None                                                                                                     # if there is no best next move to make it will get one random
    random.shuffle(validMoves)
    findMoveNegaMaxAlphaBetaPruning(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)          # uses AlphaBetaPruning
    return nextMove                                                                                                     # returns the next best move,


def findMoveNegaMaxAlphaBetaPruning(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * boardScore(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBetaPruning(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


def boardScore(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE                                                                                           # black won
        else:
            return CHECKMATE                                                                                            # white won
    if gs.staleMate:
        return STALEMATE                                                                                                # draw by stalemate
    score = 0
    for row in gs.board:                                                                                                # adds up the scores for white and black pieces
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]                                                                          # for each piece adds the piece's score for white
            elif square[0] == 'b':
                score -= pieceScore[square[1]]                                                                          # for each piece adds the piece's score for white
    return score
