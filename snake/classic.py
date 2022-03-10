import pygame
import tkinter as tk
from tkinter import messagebox
import time

from components import Snake, Food
from utils import  random_block

pygame.font.init()

HEIGHT, WIDTH = 500, 500
SPEED = 10
UP, DOWN = (0, -SPEED), (0, SPEED)
LEFT, RIGHT = (-SPEED, 0), (SPEED, 0)

screen = pygame.display.set_mode((HEIGHT, WIDTH))
score_font = pygame.font.SysFont('comicsans' , 20)

def get_position(x, y):
    if x < 0: 
        x += 500
    elif x >= 500: 
        x -= 500
    if y < 0:
        y += 500
    elif y >= 500: 
        y -= 500 
    return (x, y)

def draw_window(snake, food, screen, score):
    screen.fill((0, 0, 0))
    score = score_font.render(f'Score:{score} ', 1 , (255 , 255 ,255))
    food.draw(screen)
    snake.draw(screen)
    screen.blit(score, (10 , 10))
    pygame.display.update()

def is_gameover(snake):
    if snake.head() in snake.body[:-1]:
        return True
    return False

def main():
    time.sleep(1)
    score = 0
    clock = pygame.time.Clock()
    running = True
    s = Snake([(-10, 0), (0, 0)], RIGHT)
    pos = random_block(s.body)
    food = Food(pos)  
    x, y = 10, 0

    while running:

        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score
        
        draw_window(s, food, screen, score)
        keys_pressed = pygame.key.get_pressed()
        
        if keys_pressed[pygame.K_SPACE]:
            continue
        elif keys_pressed[pygame.K_ESCAPE]:
            return score
        elif keys_pressed[pygame.K_UP]:
            s.set_dir(UP)
        elif keys_pressed[pygame.K_DOWN]:
            s.set_dir(DOWN)
        elif keys_pressed[pygame.K_LEFT]:
            s.set_dir(LEFT)
        elif keys_pressed[pygame.K_RIGHT]:
            s.set_dir(RIGHT)

        x += s.direction[0]
        y += s.direction[1]
        s.move(get_position(x,y))

        if is_gameover(s): return score

        if food.position == s.head():
            s.body.insert(0, s.body[0])
            score += food.points
            pos = random_block(s.body)
            food = Food(pos)
        
        draw_window(s, food, screen, score)


if __name__ == '__main__':
    GAME = True
    while GAME:
        score = main()
        root = tk.Tk()
        root.withdraw()
        GAME = messagebox.askyesno(
            title='Game Over', 
            message=f'You scored {score}!!\n Do u wish to play again'
        )
    
