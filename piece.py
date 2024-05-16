import random
import json
import pygame
from constants import *

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