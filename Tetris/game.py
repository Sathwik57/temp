import pygame
import time
from components import Block
from utils import is_gameover, create_grid, clear_rows

SCREEN_HEIGHT, SCREEN_WIDTH = 800, 700
G_HEIGHT, G_WIDTH = 600, 300 
x_pos = (SCREEN_WIDTH - G_WIDTH)//2
y_pos = (SCREEN_HEIGHT - G_HEIGHT)//2
block_size = 30

pygame.font.init()
pygame.display.set_caption('Tetris')
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
default_font = pygame.font.SysFont('comicsans', 30)


def is_valid(grid, block):
    for y, x in block.pos:
        grid_x = block.x + x * block_size
        grid_y = block.y + y * block_size
        if grid_y + 20 >= y_pos + G_HEIGHT:
            return False
        if grid_x > x_pos + G_WIDTH - 30:
            return False
        elif grid_x < x_pos:
            return False
        grid_x -= x_pos
        grid_y = grid_y - y_pos + 20
        if grid[grid_y//block_size][grid_x//block_size] != (0, 0, 0) and grid_y > 0:
            return False
    return True


def draw_next_shape(screen, block):
    label = default_font.render('Next Shape', True, (255, 255, 255))
    y_position = G_HEIGHT // 2
    x_position = SCREEN_WIDTH - x_pos // 2 - 60
    screen.blit(label, (x_position - 20, y_position - 10))
    for x, y in block.pos:
        obj = pygame.Rect(x_position + y * 30, y_position + x * 30, 30, 30)
        pygame.draw.rect(screen, block._color, obj)
    pygame.display.update()


def draw_grid(screen, grid):
    for i in range(len(grid)+1):
        pos_0 = (x_pos, y_pos + i * block_size)
        pos_1 = (x_pos + G_WIDTH, y_pos + i * block_size)
        pygame.draw.line(screen, (128, 128, 128), pos_0, pos_1)

    for i in range(len(grid[0])+1):
        pos_0 = (x_pos + i * block_size, y_pos)
        pos_1 = (x_pos + i * block_size, y_pos + G_HEIGHT)
        pygame.draw.line(screen, (128, 128, 128), pos_0, pos_1)
    pygame.draw.rect(screen, (255, 0, 0), (x_pos, y_pos, G_WIDTH + 1, G_HEIGHT + 1), 3)


def draw_window(screen, grid, block, score):
    screen.fill((0, 0, 0))
    title = default_font.render('Tetris', True, (255, 255, 255))
    win.blit(title, (SCREEN_WIDTH // 2 - len('Name') * 10, y_pos // 3))
    score_font = pygame.font.SysFont('comicsans', 25)
    label = score_font.render(f'Score {score}', True, (255, 255, 255))
    screen.blit(label, (20, y_pos * 3))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            # if grid[i][j] != (0, 0, 0):
            pygame.draw.rect(
                screen, grid[i][j],
                (x_pos + j*block_size, y_pos + i*block_size, block_size, block_size), 0
            )
    draw_grid(screen, grid)
    block.draw(screen)


def main():
    block = Block(260, 0)
    new_block = Block(260, 0)
    grid = create_grid()
    filled = {}
    score = 0
    
    running = True
    clock = pygame.time.Clock()
    while running:
        change_block = False
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
        keys_pressed = pygame.key.get_pressed()
        
        if keys_pressed[pygame.K_UP]:
            block.right_rotate()
            if not is_valid(grid, block):
                block.left_rotate()
        if keys_pressed[pygame.K_RIGHT]:
            block.x += 30
            if not is_valid(grid, block):
                block.x -= 30
        if keys_pressed[pygame.K_LEFT]:
            block.x -= 30
            if not is_valid(grid, block):
                block.x += 30
        if keys_pressed[pygame.K_DOWN]:
            block.y += 10
            if not is_valid(grid, block):
                block.y -= 10
                change_block = True 
        
        block.y += 10
        if not is_valid(grid, block):
            block.y -= 10
            change_block = True
        
        if change_block:
            for y, x in block.pos:
                x_grid = (block.x + x * block_size - x_pos)//block_size
                y_grid = (block.y + y * block_size - y_pos)//block_size
                grid[y_grid][x_grid] = block._color
                pos = (y_grid, x_grid)
                filled[pos] = block._color
            
            clock.tick(2)
            block = new_block
            new_block = Block(260, 0)
            score += clear_rows(grid) * 20

        if is_gameover(grid):
            s = 'Game Over'
            label = pygame.font.SysFont('comicsans', 60).render(f'{s}!', True, (255, 255, 255))
            win.blit(label, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            pygame.display.update()
            time.sleep(2)
            running = False
        
        draw_window(win, grid, block, score)
        draw_next_shape(win, new_block)
        pygame.display.update()


if __name__ == '__main__':
    main()
