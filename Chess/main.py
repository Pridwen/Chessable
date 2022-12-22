import pygame as p
import Engine
import AI
import button
import os

x = 300
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
p.init()
p.display.set_caption("Chessable")

board_width = board_height = hist_log_height = 832                                                                      # size of chess board
hist_log_width = 250                                                                                                    # sizes of history log
size = 8                                                                                                                # just like the chess board 8 x 8
sqr = board_width // size                                                                                               # around 100 pixels for each square, just like my images for the pieces
fps = 60                                                                                                                # FPS cap
imgs = {}

menu_height = 500                                                                                                       # sizes of menu
menu_width = 800
menu = p.display.set_mode((menu_width, menu_height))
menu_font = p.font.SysFont('Verdana', 21, True, False)                                                                  # set menu font
humW = menu_font.render("White is Human", True, p.Color("Dark Red"))
humB = menu_font.render("Black is Human", True, p.Color("Dark Red"))
aiW = menu_font.render("White is AI", True, p.Color("Dark Red"))
aiB = menu_font.render("Black is AI", True, p.Color("Dark Red"))
CastAI = menu_font.render("Vs AI: Castling Disabled", True, p.Color("Dark Red"))
CastHum = menu_font.render("Vs Human: Castling Enabled", True, p.Color("Dark Red"))
whitePlayer_img = p.image.load('Menu/White.png').convert_alpha()                                                        # img for white pieces
blackPlayer_img = p.image.load('Menu/Black.png').convert_alpha()                                                        # img for black pieces
start = p.image.load('Menu/Start.png').convert_alpha()                                                                  # img for start button
logo = p.image.load("Menu/Logo.png")                                                                                    # logo for menu
white = button.Button(100, 300, whitePlayer_img, 0.6)                                                                   # white button
black = button.Button(470, 300, blackPlayer_img, 0.6)                                                                   # black button
start = button.Button(340, 430, start, 0.45)                                                                            # start button
miniwP = p.image.load("Mini/wP.png")
minibP = p.image.load("Mini/bP.png")
miniwR = p.image.load("Mini/wR.png")
minibR = p.image.load("Mini/bR.png")
miniwH = p.image.load("Mini/wH.png")
minibH = p.image.load("Mini/bH.png")
miniwB = p.image.load("Mini/wB.png")
minibB = p.image.load("Mini/bB.png")
miniwQ = p.image.load("Mini/wQ.png")
minibQ = p.image.load("Mini/bQ.png")
miniwK = p.image.load("Mini/wK.png")
minibK = p.image.load("Mini/bK.png")
coordnrfont = p.font.SysFont('Verdana', 24, True, False)
coordA = coordnrfont.render('a', False, p.Color('Dark Red'))
coordB = coordnrfont.render('b', False, p.Color('Dark Red'))
coordC = coordnrfont.render('c', False, p.Color('Dark Red'))
coordD = coordnrfont.render('d', False, p.Color('Dark Red'))
coordE = coordnrfont.render('e', False, p.Color('Dark Red'))
coordF = coordnrfont.render('f', False, p.Color('Dark Red'))
coordG = coordnrfont.render('g', False, p.Color('Dark Red'))
coordH = coordnrfont.render('h', False, p.Color('Dark Red'))
nr1 = coordnrfont.render('1', False, p.Color('Dark Red'))
nr2 = coordnrfont.render('2', False, p.Color('Dark Red'))
nr3 = coordnrfont.render('3', False, p.Color('Dark Red'))
nr4 = coordnrfont.render('4', False, p.Color('Dark Red'))
nr5 = coordnrfont.render('5', False, p.Color('Dark Red'))
nr6 = coordnrfont.render('6', False, p.Color('Dark Red'))
nr7 = coordnrfont.render('7', False, p.Color('Dark Red'))
nr8 = coordnrfont.render('8', False, p.Color('Dark Red'))



def loadImages():
    pieces = ['wP', 'wR', 'wH', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bH', 'bB', 'bQ', 'bK']
    for piece in pieces:
        imgs[piece] = p.image.load("Piece/" + piece + ".png")


def drawGameState(screen, game, validMoves, currSqr, histLogFont):
    drawBoard(screen)
    highlight(screen, game, validMoves, currSqr)
    drawPieces(screen, game.board)
    drawMoveLog(screen, game, histLogFont)


def drawMoveLog(screen, game, font):
    histLogRect = p.Rect(board_width, 0, hist_log_width, hist_log_height)
    p.draw.rect(screen, p.Color('Dark Blue'), histLogRect)
    histLog = game.histLog
    moveText = []
    paddingX = 5
    paddingY = 5
    Spacing = 5
    moveInRow = 1
    whX = 5
    whY = 5
    blX = 110
    blY = 5
    for i in range(0, len(histLog), 2):
        moveIndex = "        " + str(histLog[i]) + "                "
        if i + 1 < len(histLog):
            moveIndex += str(histLog[i+1])
        moveText.append(moveIndex)
    for i in range(0, len(moveText), moveInRow):
        text = ""
        for j in range(moveInRow):
            if i + j < len(moveText):
                text += moveText[i+j]
        if not game.whiteToMove:
            if text[8] == 'R':
                piece = miniwR
            elif text[8] == 'H':
                piece = miniwH
            elif text[8] == 'B':
                piece = miniwB
            elif text[8] == 'Q':
                piece = miniwQ
            elif text[8] == 'K':
                piece = miniwK
            else:
                piece = miniwP
        elif game.whiteToMove:
            if text[25] == 'R' or text[26] == 'R' or text[27] == 'R':
                piece = minibR
            elif text[25] == 'H' or text[26] == 'H' or text[27] == 'H':
                piece = minibH
            elif text[25] == 'B' or text[26] == 'B' or text[27] == 'B':
                piece = minibB
            elif text[25] == 'Q' or text[26] == 'Q' or text[27] == 'Q':
                piece = minibQ
            elif text[25] == 'K' or text[26] == 'K' or text[27] == 'K':
                piece = minibK
            else:
                piece = minibP
        textObject = font.render(text, False, p.Color('Dark Red'))
        textLocation = histLogRect.move(paddingX, paddingY)
        whLocation = histLogRect.move(whX, whY)
        blLocation = histLogRect.move(blX, blY)
        whY = whY + 30
        blY = blY + 30
        if whY > hist_log_height:
            screen.fill(p.Color("Dark Blue"), (832, 0, 250, 900))
            whY = 5
            blY = 5
            paddingY = -25
        screen.blit(piece, blLocation) if game.whiteToMove else screen.blit(piece, whLocation)
        screen.blit(textObject, textLocation)
        paddingY += textObject.get_height() + Spacing


def drawText(screen, text):
    font = p.font.SysFont("Verdana", 36, True, False)
    textObject = font.render(text, False, p.Color('Black'))
    textLocation = p.Rect(0, 0, board_width, board_height).move(board_width//2 - textObject.get_width()//2, board_width//2 - textObject.get_height()//2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, False, p.Color('Dark Red'))
    screen.blit(textObject, textLocation.move(2, 2))


def drawPieces(screen, board):
    for r in range(size):
        for c in range(size):
            piece = board[r][c]
            if piece != '--':
                screen.blit(imgs[piece], p.Rect(sqr * c, sqr * r, sqr, sqr))


def drawBoard(screen):
    global colors
    colors = [p.Color('white'), p.Color(135, 190, 232)]
    for r in range(size):
        for c in range(size):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(sqr * c, sqr * r, sqr, sqr))
    screen.blit(coordA, (85, 725))
    screen.blit(coordB, (185, 725))
    screen.blit(coordC, (290, 725))
    screen.blit(coordD, (390, 725))
    screen.blit(coordE, (495, 725))
    screen.blit(coordF, (605, 725))
    screen.blit(coordG, (705, 725))
    screen.blit(coordH, (805, 725))
    screen.blit(nr1, (5, 725))
    screen.blit(nr2, (5, 625))
    screen.blit(nr3, (5, 525))
    screen.blit(nr4, (5, 415))
    screen.blit(nr5, (5, 315))
    screen.blit(nr6, (5, 205))
    screen.blit(nr7, (5, 105))
    screen.blit(nr8, (5, 1))


def highlight(screen, game, validMoves, currSqr):
    if currSqr != ():
        r, c = currSqr
        if game.board[r][c][0] == ('w' if game.whiteToMove else 'b'):                                                       # currSqr is a moveable piece
            s = p.Surface((sqr, sqr))                                                                           # highlight square
            s.set_alpha(55)
            s.fill(p.Color('Red'))
            screen.blit(s, (c*sqr, r*sqr))
            s.fill(p.Color('Purple'))                                                                                   #highlight moves of piece
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*sqr, move.endRow*sqr))


def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frames = 10
    frameCount = (abs(dR) + abs(dC)) * frames
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSQR = p.Rect(move.endCol*sqr, move.endRow*sqr, sqr, sqr)
        p.draw.rect(screen, color, endSQR)
        if move.pieceCaptured != '--':
            if move.isEnpassant:
                EPRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSQR = p.Rect(move.endCol*sqr, EPRow*sqr, sqr, sqr)
            screen.blit(imgs[move.pieceCaptured], endSQR)
        screen.blit(imgs[move.pieceMoved], p.Rect(c*sqr, r*sqr, sqr, sqr))
        p.display.flip()
        clock.tick(60)


def main():
    playerBlack = False
    playerWhite = False
    run = True
    while run:
        menu.fill(p.Color("Dark Blue"))
        menu.blit(logo, (290, 20))
        menu.blit(aiW, (160, 270))
        menu.blit(aiB, (530, 270))
        if white.draw(menu):
            playerWhite = True
        if playerWhite:
            menu.fill(p.Color("Dark Blue"), (130, 270, 200, 30))
            menu.blit(humW, (130, 270))
        if playerBlack:
            menu.fill(p.Color("Dark Blue"), (500, 270, 200, 30))
            menu.blit(humB, (500, 270))
        if playerBlack or playerWhite:
            menu.blit(CastAI, (270, 230))
        if playerBlack and playerWhite:
            menu.fill(p.Color("Dark Blue"), (270, 230, 290, 30))
            menu.blit(CastHum, (260, 230))
        if black.draw(menu):
            playerBlack = True
        if start.draw(menu):
            run = False
        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
        p.display.update()

    screen = p.display.set_mode((board_width + hist_log_width, board_width))
    # screen.blit()
    clock = p.time.Clock()
    screen.fill(p.Color('white'))
    histLogFont = p.font.SysFont("Helvetica", 21, True, False)

    game = Engine.GameState()
    validMoves = game.getValidMoves()
    moveMade = False
    animation = False
    loadImages()
    running = True
    currSqr = ()
    playerClicks = []                                                                                                   # log of player clicks in tuple form
    gameOver = False
    while running:
        playerTurn = (game.whiteToMove and playerWhite) or (not game.whiteToMove and playerBlack)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and playerTurn:
                    location = p.mouse.get_pos()                                                                        # x, y coords of mouse
                    col = location[0] // sqr
                    row = location[1] // sqr
                    if currSqr == (row, col) or col >= 8:                                                            # user clicks twice the same square
                        currSqr = ()                                                                                 # resets the variable
                        playerClicks = []                                                                               # removes it from log of player clicks
                    else:
                        currSqr = (row, col)
                        playerClicks.append(currSqr)                                                                 # adds 1st and 2nd click
                        if len(playerClicks) == 2:                                                                      # after the 2nd click these happen
                            move = Engine.Move(playerClicks[0], playerClicks[1], game.board)
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    game.makeMove(validMoves[i])
                                    moveMade = True
                                    animation = True
                                    currSqr = ()
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [currSqr]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:                                                                                      # undo a move when you press z
                    game.undoMove()
                    moveMade = True
                    animation = False
                    gameOver = False
                if e.key == p.K_x:                                                                                      # resets the game when you press x
                    game = Engine.GameState()
                    validMoves = game.getValidMoves()
                    currSqr = ()
                    playerClicks = []
                    moveMade = False
                    animation = False
                    gameOver = False
        if not gameOver and not playerTurn:
            AIMove = AI.aiMove(game, validMoves)
            if AIMove is None:
                AIMove = AI.findRandomMove(validMoves)
            game.makeMove(AIMove)
            moveMade = True
            animation = True
        if moveMade:
            if animation:
                animateMove(game.histLog[-1], screen, game.board, clock)
            validMoves = game.getValidMoves()
            moveMade = False
            animation = False
        drawGameState(screen, game, validMoves, currSqr, histLogFont)
        if game.checkMate:
            gameOver = True
            if game.whiteToMove:
                drawText(screen, 'Checkmate,Black Wins')
            else:
                drawText(screen, 'Checkmate,White Wins')
        elif game.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate due to insufficient material')
        clock.tick(fps)
        p.display.flip()


if __name__ == '__main__':
    main()
