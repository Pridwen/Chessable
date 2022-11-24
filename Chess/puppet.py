import pygame
import string

pygame.init()

screen = pygame.display.set_mode((300, 600))
intermediate = pygame.surface.Surface((300, 1200))
y = 20
f = pygame.font.SysFont('', 17)
for i in range(1000):
    intermediate.blit(f.render(str(i), True, (255, 255, 255)), (10, y))
    y += 20
clock = pygame.time.Clock()
run = False

scroll_y = 0

while not run:
    run = pygame.event.get(pygame.QUIT)
    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 4:
                scroll_y = min(scroll_y + 15, 0)
            if e.button == 5:
                scroll_y = max(scroll_y - 15, -300)

    screen.blit(intermediate, (0, scroll_y))
    pygame.display.flip()
    clock.tick(60)
