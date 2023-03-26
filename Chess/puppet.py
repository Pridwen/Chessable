import pygame as p
import button
import os
import sys

x = 300
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
p.init()
p.display.set_caption("Chessable Project")


menu_height = 500                                                                                                       # sizes of menu
menu_width = 800
menu = p.display.set_mode((menu_width, menu_height))
menu_font = p.font.SysFont('Verdana', 21, True, False)
humW = menu_font.render("White is Human", True, p.Color("Dark Red"))
humB = menu_font.render("Black is Human", True, p.Color("Dark Red"))
aiW = menu_font.render("White is AI", True, p.Color("Dark Red"))
aiB = menu_font.render("Black is AI", True, p.Color("Dark Red"))
SiegeOn = menu_font.render("Siege Mode:On", True, p.Color("Dark Red"))
SiegeOff = menu_font.render("Siege Mode:Off", True, p.Color("Dark Red"))
CastAI = menu_font.render("Vs AI: Castling Disabled", True, p.Color("Dark Red"))
CastHum = menu_font.render("Vs Human: Castling Enabled", True, p.Color("Dark Red"))
whitePlayer_img = p.image.load('Menu/White.png').convert_alpha()
blackPlayer_img = p.image.load('Menu/Black.png').convert_alpha()
logo = p.image.load("Menu/Logo.png")
Siege = p.image.load('Menu/Siege.png').convert_alpha()
Siege = button.Button(30, 30, Siege, 0.4)
white = button.Button(100, 300, whitePlayer_img, 0.6)
black = button.Button(470, 300, blackPlayer_img, 0.6)


how_to = p.image.load('Menu/How to.png').convert_alpha()
how_to = button.Button(650, 50, how_to, 0.5)

start = p.image.load('Menu/Start.png').convert_alpha()
start = button.Button(340, 430, start, 0.45)

Arrow = p.image.load('Menu/Arrow.png').convert_alpha()
Arrow = button.Button(200, 200, Arrow, 0.6)


def main():
    playerBlack = False
    playerWhite = False
    counterBlack = 1
    counterWhite = 1
    run_menu = True
    menu_pause = True
    menu_state = "menu"
    while run_menu:
        menu.fill(p.Color("Dark Blue"))
        if menu_pause:
            if menu_state == "menu":
                menu.blit(logo, (290, 20))
                menu.blit(aiW, (160, 270))
                menu.blit(aiB, (530, 270))
                if white.draw(menu):
                    playerWhite = True
                    counterWhite += 1
                    if counterWhite % 2 != 0:
                        playerWhite = False
                if black.draw(menu):
                    playerBlack = True
                    counterBlack += 1
                    if counterBlack % 2 != 0:
                        playerBlack = False
                if start.draw(menu):
                    run_menu = False
                if Siege.draw(menu):
                    print("siege")
                if how_to.draw(menu):
                    menu_pause = True
                    menu_state = "instr"
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
                for event in p.event.get():
                    if event.type == p.QUIT:
                        p.quit()
                        sys.exit()
                p.display.update()
            elif menu_state == 'instr':
                if Arrow.draw(menu):
                    menu_state = "menu"
                for event in p.event.get():
                    if event.type == p.QUIT:
                        p.quit()
                        sys.exit()
                p.display.update()


if __name__ == '__main__':
    main()
