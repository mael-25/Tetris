import copy
import json
import time
import numpy as np
import pygame
from constants import *
from piece import *


grid:np.ndarray = np.zeros([20, 10], dtype=np.uint8)

# print(grid)
# accelerated_drop = False


piece = Piece.random_piece(grid.shape)
next_piece = Piece.random_piece(grid.shape)

def check_full_row(grid):
    full_lines = []
    for i, y in enumerate(grid):
        full = True
        for x in y:
            if x == 0:
                full = False
        if full:
            full_lines.append(i)

    cleared = len(full_lines)

    for y in full_lines:
        grid[y]=0
        for r in range(y, 0, -1):
            grid[r] = grid[r-1]
        grid[0] = 0

    return cleared


def show_grid(grid):
    for i,y in enumerate(grid):
        for i2,x in enumerate(y):
            if x!=0:
                pygame.draw.rect(screen, (0,0,0), (i2*24+64, i*24+64, 24,24))

# grid[2,2]=1

pygame.init()
pygame.font.init() 
screen = pygame.display.set_mode((10*24+64+256, 20*24+128))
# while 1:
#     pygame.display.update()
#     events = pygame.event.get()
#     show_grid(grid)
update = pygame.event.Event(UPDATE)

pygame.time.set_timer(update, 1000)

# pygame.key.get_pressed()
down_pressed = False

points = 0

level = 0
# level = 7

lines = 0

highscores = json.load(open("highscore.json"))

speed = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 5, 5, 5, 4,4,4, 3,3,3, 2,2,2,2,2,2,2,2,2,2, 1]

pygame.time.set_timer(update, (speed[min(level, 29)]*1000)//60)

font = pygame.font.Font("PressStart2P-Regular.ttf", 20)

clock = pygame.time.Clock()
if __name__=="__main__":
    while 1:
        grid2 = grid.copy()
        coords = piece.get_coords()
        for x,y in coords:
            grid2[y,x]  = 1
        # print(grid2)
        # print(piece.x, piece.y)
        screen.fill((255,255,255))
        show_grid(grid2)
        pygame.draw.rect(screen, (0,0,0), (64,64,10*24, 20*24), 3)
        pygame.draw.rect(screen, (0,0,0), (64+240+32,64,192, 96), 3)

        pygame.draw.rect(screen, (0,0,0), (64+240+32,64,192, 96), 3)
        screen.blit(font.render("Score", 0, (0,0,0)), (64+240+32+12,64+12))
        screen.blit(font.render("{:08d}".format(points), 0, (0,0,0)), (64+240+32+12,64+12+32))

        pygame.draw.rect(screen, (0,0,0), (64+240+32,64+128,96, 96), 3)
        screen.blit(font.render("Next", 0, (0,0,0)), (64+240+32+8,64+128+8))
        next_piece_copy = copy.copy(next_piece)
        next_piece_copy.x = 1
        next_piece_copy.y = 0

        coords = next_piece_copy.get_coords()

        for (x,y) in coords:
            x*=20
            y*=20
            x+=64+240+32+8
            y+=64+128+8+24
            pygame.draw.rect(screen, (0,0,0), (x,y,20,20))



        pygame.display.update()
        # a = input("")
        # if a == "l":
        #     piece.left(grid)
        # elif a == "r":
        #     piece.right(grid)
        # elif a=="tr":
        #     piece.rotate_clockwise()
        # elif a=="tl":
        #     piece.rotate_counterclockwise()
        # time.sleep(1)
        
        clock.tick(60)
        events = pygame.event.get()
        moved = False
        for x in events:
            if x.type == pygame.KEYDOWN:
                if x.key == pygame.K_LEFT and not moved:
                    piece.left(grid)
                    moved = True
                if x.key == pygame.K_RIGHT and not moved:
                    piece.right(grid)
                    moved = True
                if x.key == pygame.K_a:
                    piece.rotate_counterclockwise(grid)
                if x.key == pygame.K_d or x.key == pygame.K_UP:
                    piece.rotate_clockwise(grid)
                if x.key == pygame.K_DOWN:
                    # continue # for beginners
                    down_pressed = True
                if x.key == pygame.K_SPACE:
                    # continue # for beginners
                    while not piece.on_ground(grid):
                        piece.down(grid)
                        points += 2
                    piece.update(grid)
            if x.type == pygame.KEYUP:
                if x.key == pygame.K_DOWN:
                    down_pressed = False
            if x.type == pygame.QUIT:
                print(points)
                # if score>highscores[]
                print("Lines: %d" %lines)
                print("Level: %d" % level)
                exit()
            if x.type == UPDATE:
                r = piece.update(grid)
                if r:
                    piece = next_piece
                    next_piece = Piece.random_piece(grid.shape)
                    if not piece.check_piece_validity(grid):
                        print("GAME OVER")
                        time.sleep(1.5)
                        pygame.event.get()
                        pygame.time.set_timer(pygame.QUIT, 1)
                    # piece = L(grid.shape)
                    cleared = check_full_row(grid)
                    lines += cleared

                    points += (200*cleared-100)*(level+1)
                    if cleared == 4 or cleared == 0:
                        points +=100*(level+1)
                    
                    print(points, end="\r")

                    if lines >= (level+1)*10:
                        level += 1
                        pygame.time.set_timer(update, (speed[min(level, 29)]*1000)//60)
                        print("LEVEL UP")
            if x.type == LOCK:
                r = piece.lock(grid)
                if r:
                    piece = next_piece
                    next_piece = Piece.random_piece(grid.shape)
                    if not piece.check_piece_validity(grid):
                        print("GAME OVER")
                        time.sleep(1.5)
                        pygame.event.get()
                        pygame.time.set_timer(pygame.QUIT, 1)
                    # piece = L(grid.shape)
                    cleared = check_full_row(grid)
                    lines += cleared

                    points += (200*cleared-100)*(level+1)
                    if cleared == 4 or cleared == 0:
                        points +=100*(level+1)
                    
                    print(points, end="\r")

                    if lines > (level+1)*10:
                        level += 1
                        pygame.time.set_timer(update, (speed[min(level, 29)]*1000)//60)
                        print("LEVEL UP")
                        

        if down_pressed:
            if piece.down(grid):
                points+=1
                print(points, end="\r")


