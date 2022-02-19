import numpy as np
import pygame
import time
import read_grid
pygame.init()
print_every=0.001
screen_width,screen_height=1200,800
square_size=min(screen_height//9,screen_width//9)
x_offset=(screen_width-9*square_size)//2
y_offset=(screen_height-9*square_size)//2
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Solver")

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, color=(0,0,0)):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
last_print=time.time()

r'''
grid=[[1,5,0,2,0,9,0,0,4],
    [0,4,0,0,0,6,0,0,0],
    [0,0,0,0,4,0,0,6,3],
    [0,7,0,0,0,0,8,0,6],
    [6,0,0,0,0,0,0,0,5],
    [2,0,8,0,0,0,0,1,0],
    [4,6,0,0,8,0,0,0,0],
    [0,0,0,6,0,0,0,7,0],
    [8,0,0,5,0,1,0,4,9]]'''

grid=read_grid.readGrid()
print("owo")
#grid=[[0 for x in y] for y in grid]

init_grid=[[x for x in y] for y in grid]

def display_grid(screen,solved=False):
    global grid
    global last_print
    screen.fill((255, 255, 255))
    for x_big in range(3):
        for y_big in range(3):
            pygame.draw.rect(screen,(0,0,0),(x_offset+x_big*square_size*3,y_offset+y_big*square_size*3,3*square_size,3*square_size),width=4)
    for x_pos in range(9):
        for y_pos in range(9):
            pygame.draw.rect(screen,(0,0,0),(x_offset+x_pos*square_size,y_offset+y_pos*square_size,square_size,square_size),width=1)
            if init_grid[y_pos][x_pos]!=0:
                draw_text(screen,str(grid[y_pos][x_pos]),30,x_offset+(x_pos+0.5)*square_size,y_offset+(y_pos+0.35)*square_size)
            elif grid[y_pos][x_pos]!=0:
                if not solved:
                    draw_text(screen,str(grid[y_pos][x_pos]),30,x_offset+(x_pos+0.5)*square_size,y_offset+(y_pos+0.35)*square_size,(0,204,204))
                else:
                    draw_text(screen,str(grid[y_pos][x_pos]),30,x_offset+(x_pos+0.5)*square_size,y_offset+(y_pos+0.35)*square_size,(51,255,51))
    pygame.display.flip()
    last_print=time.time()

def possible(y,x,n):
    global grid
    for i in range(9):
        if grid[i][x]==n:
            return False
        if grid[y][i]==n:
            return False
    for i in range(3):
        for j in range(3):
            if grid[int(y/3)*3+i][int(x/3)*3+j]==n:
                return False
    return True

def solve():
    global grid
    global last_print
    for y in range(9):
        for x in range(9):
            if grid[y][x]==0:
                for n in range(1,10):
                    if possible(y,x,n):
                        grid[y][x]=n
                        if time.time()-last_print>print_every:
                            display_grid(screen)
                        solve()
                        #print(np.matrix(grid))
                        grid[y][x]=0
                return
    display_grid(screen,True)
    input("More?")

solve()

pygame.quit()
