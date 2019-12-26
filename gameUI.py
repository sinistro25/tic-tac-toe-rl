import pygame
from pygame.locals import *
import sys
from enum import Enum

from utilities import *

SQUARESIZE = 150
WIDTH = HEIGHT = 600
XMARGIN = (WIDTH - 3*SQUARESIZE) // 2
YMARGIN = (HEIGHT - 3*SQUARESIZE) // 2
DSURF = pygame.display.set_mode((HEIGHT,WIDTH))

global mouse_x
global mouse_y
mouse_x,mouse_y = None,None

pygame.init()
pygame.font.init()
FONTPATH = pygame.font.get_default_font()
FONTSIZE =  80
FONT = pygame.font.Font(FONTPATH,FONTSIZE)
LINEWIDTH = 10
class Color(Enum):
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    GRAY  = (150,150,150)
    RED = (255,0,0)

BGCOLOR = Color.WHITE.value

def pixel_to_tile(pos):
    x,y = pos
    if x < XMARGIN or y < YMARGIN: 
        # Mouse out of the board
        return None,None
    x = (x-XMARGIN) // SQUARESIZE
    y = (y-YMARGIN) // SQUARESIZE 
    
    if x >= 3 or y >= 3:
        # Mouse out of the board
        return None,None
    return x,y
def draw_board(board):
    DSURF.fill(BGCOLOR)
    if mouse_x is not None and board[mouse_y][mouse_x] is None:
        pygame.draw.rect(DSURF,Color.GRAY.value,(XMARGIN + mouse_x*SQUARESIZE,YMARGIN + mouse_y*SQUARESIZE,SQUARESIZE,SQUARESIZE))

    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                continue
            text = FONT.render(str(board[i][j]), True, Color.BLACK.value)
            textrect = text.get_rect()
            textrect.center = (XMARGIN + j*SQUARESIZE + SQUARESIZE/2,YMARGIN + i*SQUARESIZE + SQUARESIZE/2)
            DSURF.blit(text, textrect)
    pygame.draw.line(DSURF,Color.BLACK.value,(XMARGIN,YMARGIN+SQUARESIZE),(WIDTH-XMARGIN, YMARGIN+SQUARESIZE),LINEWIDTH)
    pygame.draw.line(DSURF,Color.BLACK.value,(XMARGIN,YMARGIN+2*SQUARESIZE),(WIDTH-XMARGIN, YMARGIN+2*SQUARESIZE),LINEWIDTH)
    pygame.draw.line(DSURF,Color.BLACK.value,(XMARGIN+SQUARESIZE,YMARGIN),(XMARGIN+SQUARESIZE,HEIGHT-YMARGIN),LINEWIDTH)
    pygame.draw.line(DSURF,Color.BLACK.value,(XMARGIN+2*SQUARESIZE, YMARGIN),(XMARGIN+2*SQUARESIZE, HEIGHT-YMARGIN),LINEWIDTH)
    
    
    pygame.display.update()
def handle_events(game):
    global mouse_x
    global mouse_y
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if game.finished():
            continue
        if event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pixel_to_tile(event.pos)
            if mouse_x is None:
                continue
            game.mark(mouse_x, mouse_y)
            
        if event.type == MOUSEMOTION:
           mouse_x,mouse_y = pixel_to_tile(event.pos)

