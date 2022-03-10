import pygame
from random import choices


class Snake:
    
    def __init__(self , body, direction, width = 10, height = 10):
        self.body = body
        self.width = int(width)
        self.height = int(height)
        self.direction = direction
    
    def set_dir(self , dir):
        x,y = self.direction
        if not(abs(x) == abs(dir[0]) and abs(y) == abs(dir[1])):
            self.direction = dir

    def move(self, pos):
        self.body = self.body[1:] + [pos]
    
    def head(self):
        return self.body[-1]

    def draw(self, screen):
        for i,(x,y) in enumerate(self.body[::-1]):
            b = pygame.Rect(x, y, self.width, self.height)
            pygame.draw.rect(screen, (255, 255 , 255), b)
            if i == 0:
                radius = 1.5
                left_eye = ( x + self.width/4, y + self.width/3)
                right_eye = ( x + 10 -self.width/4, y + self.width/3)
                pygame.draw.circle(screen, (211, 38, 38), left_eye, radius)
                pygame.draw.circle(screen, (211, 38, 38), right_eye, radius)   

class Block:

    def __init__(self, pos) -> None:
        self.pos = pos
        self.color = (255, 255, 255)

    @property    
    def position(self):
        return (self.pos)

    def draw(self, screen):
        a = pygame.Rect(*self.pos, 10, 10)
        pygame.draw.rect(screen, self.color, a)

class Food(Block):
    
    POINTS = {
        1 : (255, 255, 0), 
        5 : (200, 40, 0), 
        10 : (30, 190, 10)
    }
    WEIGHTS = [20, 2, 1]

    def __init__(self, pos):
        super(Food, self).__init__(pos)
        self.points = Food.get_points()
        self.color = self.get_color()

    @classmethod
    def get_points(cls):
        return choices(list(cls.POINTS.keys()), cls.WEIGHTS, k=1)[0]

    def get_color(self):
        return Food.POINTS[self.points]
