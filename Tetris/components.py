import pygame
from random import choice
from shapes import cube, line, l_joint, left_l_joint, s_joint, t_joint

SCREEN_HEIGHT, SCREEN_WIDTH = 800, 700
G_HEIGHT, G_WIDTH = 600, 300
x_pos = (SCREEN_WIDTH - G_WIDTH) // 2
y_pos = (SCREEN_HEIGHT - G_HEIGHT) // 2


class Block:
    block_shapes = [cube, line, l_joint, left_l_joint, s_joint, t_joint]
    shape_colors = [
        (81, 214, 214), (255, 255, 0),
        (128, 0, 128), (0, 220, 0), (255, 0, 0),
        (0, 0, 220), (255, 127, 0), (127, 127, 127)
    ]

    def __init__(self, row, col):
        self.x = row
        self.y = col
        self.rotation = 0
        self.set_shape()
        self.get_position()

    def set_shape(self):
        self._shape = choice(Block.block_shapes)
        self._color = choice(Block.shape_colors)

    def right_rotate(self):
        self.rotation += 1
        self.rotation %= len(self._shape)
        self.get_position()

    def left_rotate(self):
        self.rotation -= 1
        self.rotation %= len(self._shape)
        self.get_position()

    def move(self):
        self.y += 10

    def get_position(self):
        self.pos = []
        for i, y_value in enumerate(self._shape[self.rotation]):
            for j, x_value in enumerate(y_value):
                if x_value == '0':
                    self.pos.append((i, j))
        self.pos.sort()

    def draw(self, screen):
        for x, y in self.pos:
            y_position = self.y + x * 30
            if y_position < 100:
                continue
            obj = pygame.Rect(self.x + y * 30, y_position, 30, 30)
            pygame.draw.rect(screen, self._color, obj)
