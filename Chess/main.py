import pygame as p
import Engine
import AI
p.init()

WIDTH = HEIGHT = 832    # size of window
MOVE_LOG_WIDTH = 425
MOVE_LOG_HEIGHT = HEIGHT
DIMENSION = 8  # 8*8 CHESS BOARD                                                                                        # 8 just like the chess board 8 x 8
SQ_SIZE = HEIGHT // DIMENSION                                                                                           # around 100 pixels for each square, just like my images for the pieces
MAX_FPS = 60                                                                                                            # FPS cap
IMAGES = {}


def loadImages():
    pieces = ['wP', 'wR', 'wH', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bH', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Piece/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    screen = p.display.set_mode((WIDTH + MOVE_LOG_WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    moveLogFont = p.font.SysFont("Helvetica", 21, True, False)

    gs = Engine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []                                                                                                   # log of player clicks in tuple form
    gameOver = False
    playerWhite = False                                                                                                  # if is True then white is player, if false its AI
    playerBlack = False                                                                                                # if is True then black is player, if false its AI
    while running:
        playerTurn = (gs.whiteToMove and playerWhite) or (not gs.whiteToMove and playerBlack)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and playerTurn:
                    location = p.mouse.get_pos()                                                                        # x, y coords of mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col) or col >= 8:                                                            # user clicks twice the same square
                        sqSelected = ()                                                                                 # resets the variable
                        playerClicks = []                                                                               # removes it from log of player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)                                                                 # adds 1st and 2nd click
                        if len(playerClicks) == 2:                                                                      # after the 2nd click these happen
                            move = Engine.Move(playerClicks[0], playerClicks[1], gs.board)
                            print(move.getChessNote())
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    animate = True
                                    sqSelected = ()
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:                                                                                      # undo a move when you press z
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_x:                                                                                      # resets the game when you press x
                    gs = Engine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
        if not gameOver and not playerTurn:
            AIMove = AI.findBestMoveYEP(gs, validMoves)
            if AIMove is None:
                AIMove = AI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Checkmate,Black Wins')
            else:
                drawText(screen, 'Checkmate,White Wins')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate due to insufficient material')
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)
    highlighter(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)


def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(WIDTH, 0, MOVE_LOG_WIDTH, MOVE_LOG_HEIGHT)
    p.draw.rect(screen, p.Color('Dark Blue'), moveLogRect)
    moveLog = gs.moveLog
    moveText = []
    paddingX = 5
    paddingY = 5
    Spacing = 5
    moveInRow = 3
    for i in range(0, len(moveLog), 2):
        moveIndex = str(i // 2 + 1) + ")" + " [" + str(moveLog[i]) + "]  "
        if i + 1 < len(moveLog):
            moveIndex += str(moveLog[i+1]) + "  "
        moveText.append(moveIndex)
    for i in range(0, len(moveText), moveInRow):
        text = " "
        for j in range(moveInRow):
            if i + j < len(moveText):
                text += moveText[i+j]
        textObject = font.render(text, False, p.Color('Dark Red'))
        textLocation = moveLogRect.move(paddingX, paddingY)
        screen.blit(textObject, textLocation)
        paddingY += textObject.get_height() + Spacing


def drawText(screen, text):
    font = p.font.SysFont("Verdana", 36, True, False)
    textObject = font.render(text, False, p.Color('Black'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH//2 - textObject.get_width()//2, HEIGHT//2 - textObject.get_height()//2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, False, p.Color('Dark Red'))
    screen.blit(textObject, textLocation.move(2, 2))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':
                screen.blit(IMAGES[piece], p.Rect(SQ_SIZE * c, SQ_SIZE * r, SQ_SIZE, SQ_SIZE))


def drawBoard(screen):
    global colors
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(SQ_SIZE * c, SQ_SIZE * r, SQ_SIZE, SQ_SIZE))


def highlighter(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):                                                       # sqSelected is a moveable piece
            s = p.Surface((SQ_SIZE, SQ_SIZE))                                                                           # highlight square
            s.set_alpha(55)
            s.fill(p.Color('Red'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('Purple'))                                                                                   #highlight moves of piece
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frames = 13
    frameCount = (abs(dR) + abs(dC)) * frames
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSQR = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSQR)
        if move.pieceCaptured != '--':
            if move.isEnpassant:
                EPRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSQR = p.Rect(move.endCol*SQ_SIZE, EPRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSQR)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
