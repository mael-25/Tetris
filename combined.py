UPDATE = 1
LOCK = 2

BORDER = 64


LOCK_DELAY = 0

import random
import json
import pygame

lock = pygame.event.Event(LOCK)

class Piece():
    def __init__(self, gridsize) -> None:
        self.x, self.y = 4, 0
        self.rot = 0
        self.gridsize = gridsize
        self.is_locked = -1
        self.color = -1
        self.rotation_kick = json.load(open("rotation_tables_OTHER.json"))
        self.movements_left = 10
        

    def check_piece_validity(self, grid):
        """Returns True if piece is valid else False"""
        if self.outside_grid():
            return False
        if self.in_grid_tile(grid):
            return False
        return True

    def on_ground(self, grid):
        """Returns True if on ground else False"""
        self.y+=1
        coords = self.get_coords()
        on_ground = False
        for x,y in coords:
            if y >= self.gridsize[0]:
                on_ground = True
            elif grid[y,x] != 0:
                on_ground = True

        self.y -=1
        return on_ground
    
    def in_grid_tile(self, grid):
        """Returns True if the Piece is not inside empty spots"""
        coords = self.get_coords()
        for x,y in coords:
            if grid[y,x]!=0:
                return True
        return False

    def outside_grid(self):
        """Returns True if outside of grid else False"""
        coords = self.get_coords()
        for x,y in coords:
            if y<0 or y>=self.gridsize[0]:
                return True
            elif x<0 or x>=self.gridsize[1]:
                return True
        return False
    
    def down(self, grid):
        if self.on_ground(grid):
            return 0
        else:
            self.y+=1
            return 1

    
    def update(self, grid):
        # if self.lock_delay <= 0:
        #     if self.on_ground(grid):
        #         coords = self.get_coords()
        #         for x,y in coords:
        #             grid[y,x] = 1
        #         return 1#, grid
        if self.on_ground(grid):
            self.is_locked = 0
            if LOCK_DELAY==0:self.lock(grid);return True
            else: pygame.time.set_timer(lock, LOCK_DELAY, 1)
            
        else:
            self.down(grid)
            self.is_locked = -1
            self.movements_left = 10
            return False
    
    def lock(self, grid):
        if self.on_ground(grid):
            coords = self.get_coords()
            for x,y in coords:
                grid[y,x] = 1
            return True
        return False

    def rotate_clockwise(self, grid):
        self.rot = (self.rot+ 1 )%4
        suceed = False
        if not self.check_piece_validity(grid):
            for x in range(4):
                translation = self.rotation_kick[self.rot-1][x]
                self.x+=translation[0]
                self.y+=translation[1]
                if self.check_piece_validity(grid):
                    suceed = True
                    break
                else:
                    self.x-=translation[0]
                    self.y-=translation[1]

            if not suceed:
                self.rot = (self.rot- 1 )%4
        if (self.check_piece_validity(grid) or suceed) and self.is_locked == 0:
            pygame.time.set_timer(lock, LOCK_DELAY, 1)
            self.movements_left -=1
            

    def rotate_counterclockwise(self, grid):
        self.rot = (self.rot- 1 )%4
        if not self.check_piece_validity(grid):
            suceed = False
            for x in range(4):
                translation = self.rotation_kick[self.rot][x]
                translation[0] = -translation[0]
                translation[1] = -translation[1]
                self.x+=translation[0]
                self.y+=translation[1]
                if self.check_piece_validity(grid):
                    suceed = True
                    break
                else:
                    self.x-=translation[0]
                    self.y-=translation[1]

            if not suceed:
                self.rot = (self.rot- 1 )%4
        if (self.check_piece_validity(grid) or suceed) and self.is_locked == 0:
            pygame.time.set_timer(lock, LOCK_DELAY, 1)
            self.movements_left -=1
        

    def left(self, grid):
        self.x-=1
        if self.outside_grid() or self.in_grid_tile(grid):
            self.x+=1
        elif self.is_locked == 0:
            pygame.time.set_timer(lock, LOCK_DELAY, 1)
            self.movements_left -=1


    def right(self, grid):
        self.x+=1
        if self.outside_grid() or self.in_grid_tile(grid):
            self.x-=1
        elif self.is_locked == 0:
            pygame.time.set_timer(lock, LOCK_DELAY, 1)
            self.movements_left -=1

    def get_coords(self)->list[list[int]]:
        return [[..., ...]]

    @staticmethod
    def random_piece(gridsize):
        return random.choice([O,I,J,L,S,T,Z])(gridsize)


class O(Piece):
    def __init__(self, gridsize) -> None:
        super().__init__(gridsize)
        self.color = 1
        self.rotation_kick = None

    def get_coords(self):
        return [[self.x, self.y], [self.x+1, self.y], [self.x, self.y+1], [self.x+1, self.y+1]]
    
    def rotate_clockwise(self, grid):
        pass
    def rotate_counterclockwise(self, grid):
        pass

class I(Piece):
    def __init__(self, gridsize) -> None:
        super().__init__(gridsize)
        self.color = 2
        self.rotation_kick = json.load(open("rotation_tables_I.json"))
    def get_coords(self):
        if self.rot %2==0:
            pieces = [[self.x-1, self.y], [self.x, self.y], [self.x+1, self.y], [self.x+2, self.y]]
            if self.rot==2:
                pieces = [[x, y+1] for (x,y) in pieces]
  
        if self.rot %2==1:
            pieces = [[self.x+1, self.y-1], [self.x+1, self.y], [self.x+1, self.y+1], [self.x+1, self.y+2]]
            if self.rot==3:
                pieces = [[x-1, y] for (x,y) in pieces]

        return pieces
  
class J(Piece):
    def __init__(self, gridsize) -> None:
        super().__init__(gridsize)
        self.color = 3
    def get_coords(self):
        if self.rot == 0:
            return [[self.x-1, self.y], [self.x-1, self.y+1], [self.x, self.y+1], [self.x+1, self.y+1]]
        elif self.rot == 1:
            return [[self.x+1, self.y], [self.x, self.y], [self.x, self.y+1], [self.x, self.y+2]]
        elif self.rot == 2:
            return [[self.x-1, self.y+1], [self.x, self.y+1], [self.x+1, self.y+1], [self.x+1, self.y+2]]
        elif self.rot == 3:
            return [[self.x, self.y], [self.x, self.y+1], [self.x, self.y+2], [self.x-1, self.y+2]]
  
class L(Piece):
    def __init__(self, gridsize) -> None:
        super().__init__(gridsize)
        self.color = 4
    def get_coords(self):
        if self.rot == 0:
            return [[self.x+1, self.y], [self.x-1, self.y+1], [self.x, self.y+1], [self.x+1, self.y+1]]
        elif self.rot == 1:
            return [[self.x+1, self.y+2], [self.x, self.y], [self.x, self.y+1], [self.x, self.y+2]]
        elif self.rot == 2:
            return [[self.x-1, self.y+1], [self.x, self.y+1], [self.x+1, self.y+1], [self.x-1, self.y+2]]
        elif self.rot == 3:
            return [[self.x, self.y], [self.x, self.y+1], [self.x, self.y+2], [self.x-1, self.y]]
  
class S(Piece):
    def __init__(self, gridsize) -> None:
        super().__init__(gridsize)
        self.color = 5
    def get_coords(self):
        if self.rot %2 ==0:
            pieces = [[self.x, self.y], [self.x+1, self.y], [self.x, self.y+1], [self.x-1, self.y+1]]
            if self.rot==2:
                pieces = [[x, y+1] for (x,y) in pieces]
            return pieces
        else:
            pieces = [[self.x, self.y], [self.x, self.y+1], [self.x+1, self.y+1], [self.x+1, self.y+2]]
            if self.rot==3:
                pieces = [[x-1, y] for (x,y) in pieces]
            return pieces
  
class T(Piece):
    def __init__(self, gridsize) -> None:
        super().__init__(gridsize)
        self.color = 6
    def get_coords(self):
        if self.rot == 0:
            return [[self.x, self.y], [self.x-1, self.y+1], [self.x, self.y+1], [self.x+1, self.y+1]]
        elif self.rot == 1:
            return [[self.x, self.y], [self.x, self.y+1], [self.x+1, self.y+1], [self.x, self.y+2]]
        if self.rot == 2:
            return [[self.x, self.y+2], [self.x-1, self.y+1], [self.x, self.y+1], [self.x+1, self.y+1]]
        elif self.rot == 3:
            return [[self.x, self.y], [self.x, self.y+1], [self.x-1, self.y+1], [self.x, self.y+2]]
  
class Z(Piece):
    def __init__(self, gridsize) -> None:
        super().__init__(gridsize)
        self.color = 7
    def get_coords(self):
        if self.rot == 0:
            return [[self.x, self.y], [self.x-1, self.y], [self.x, self.y+1], [self.x+1, self.y+1]]
        elif self.rot == 1:
            return [[self.x+1, self.y], [self.x, self.y+1], [self.x+1, self.y+1], [self.x, self.y+2]]
        if self.rot == 2:
            return [[self.x, self.y+2], [self.x-1, self.y+1], [self.x, self.y+1], [self.x+1, self.y+2]]
        elif self.rot == 3:
            return [[self.x, self.y], [self.x, self.y+1], [self.x-1, self.y+1], [self.x-1, self.y+2]]

import copy
import json
import time
import numpy as np
import pygame


grid:np.ndarray = np.zeros([20, 10], dtype=np.uint8)

# print(grid)


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
                    down_pressed = True
                if x.key == pygame.K_SPACE:
                    piece.lock_delay = 0
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


