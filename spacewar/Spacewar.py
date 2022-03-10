import pygame
import os
pygame.font.init()

from pygame import key

WIDTH , HEIGHT = 900, 500 
win =  pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption('Space War')

space_width , space_height = 55 , 40 
vel = 5
bul_vel = 10
red_hit = pygame.USEREVENT + 1
yellow_hit = pygame.USEREVENT + 2

Lives_font = pygame.font.SysFont('comicsans' , 40)
Winner_font = pygame.font.SysFont('comicsans' , 100)

yellow_space_ship_img = pygame.image.load('spaceship_yellow.png')
yellow_spaceship = pygame.transform.rotate(
    pygame.transform.scale(
        yellow_space_ship_img , (space_width , space_height)), 270
    )

red_space_ship_img = pygame.image.load('spaceship_red.png')
red_spaceship = pygame.transform.rotate(
    pygame.transform.scale(red_space_ship_img , (space_width , space_height)), 90
    )

border = pygame.Rect( WIDTH // 2 - 5 , 0 , 10 , HEIGHT)
space_bg = pygame.transform.scale(pygame.image.load(os.path.join('123','space.png')) , (WIDTH ,HEIGHT))



def draw_window(red , yellow , red_bul , yell_bull , red_health , yellow_health):
    win.blit(space_bg , (0 ,0))
    win.blit(space_bg , (border.x + 10 ,WIDTH))
    pygame.draw.rect(win , (0 , 0 , 0), border)
    red_lives = Lives_font.render("Health: " + str(red_health) , 1 , (255 , 255 ,255))
    yellow_lives = Lives_font.render("Health: " + str(yellow_health) , 1 , (255 , 255 ,255))
    win.blit(red_lives , (10 , 10))
    win.blit(yellow_lives , (WIDTH - yellow_lives.get_width() - 10 , 10))
    win.blit(yellow_spaceship , (yellow.x ,yellow.y))
    win.blit(red_spaceship , (red.x ,red.y))
    for bullet in red_bul:
        pygame.draw.rect(win , (255 , 0 , 0), bullet)
    for bullet in yell_bull:
        pygame.draw.rect(win , (255 , 255 , 0), bullet)
    
    pygame.display.update()

def red_movemnts(keys_pressed , red):
    if keys_pressed[pygame.K_a] and red.x - vel > 0: red.x -= vel
    if keys_pressed[pygame.K_d] and red.x + vel + red.width< border.x + 10 : red.x += vel
    if keys_pressed[pygame.K_w] and red.y - vel > 0: red.y -= vel
    if keys_pressed[pygame.K_s] and red.y + vel + red.height < HEIGHT - 15: red.y += vel

def yellow_movemnts(keys_pressed , yellow):
    if keys_pressed[pygame.K_LEFT]and yellow.x - vel > border.x + 10: yellow.x -= vel
    if keys_pressed[pygame.K_RIGHT] and yellow.x + vel + yellow.width < WIDTH: yellow.x += vel
    if keys_pressed[pygame.K_UP] and yellow.y - vel > 0: yellow.y -= vel
    if keys_pressed[pygame.K_DOWN]and yellow.y + vel + yellow.height < HEIGHT - 15: yellow.y += vel

def handle_bullets(red_bull , yell_bull , red ,yellow):
    for bullet in red_bull:
        bullet.x += bul_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bull.remove(bullet)
        elif bullet.x == WIDTH:
            red_bull.remove(bullet)

    for bullet in yell_bull:
        bullet.x -= bul_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yell_bull.remove(bullet)
        elif bullet.x == 0:
            yell_bull.remove(bullet)

def draw_winner(text):
    win_text = Winner_font.render(text , 1 , (255, 255 , 255))
    win.blit(win_text , (WIDTH//2 - win_text.get_width()//2 , HEIGHT //2 - win_text.get_height()//2))
    pygame.display.update()  
    pygame.time.delay(3000)  

def main():
    red  = pygame.Rect(100 , 100 , space_width , space_height)
    yellow  = pygame.Rect(800 , 100 , space_width , space_height)

    red_health , yellow_health = 10 , 10
    red_bull , yell_bull = [] , []
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(red.x + red.width - 3 , red.y + red.height //2 + 5  , 10 , 5 )
                    red_bull.append(bullet)
                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect(yellow.x , yellow.y + yellow.height // 2 + 5 , 10 , 5 )
                    yell_bull.append(bullet)
            
            if event.type == red_hit:
                red_health -= 1
            if event.type == yellow_hit:
                yellow_health -= 1
            
            winner_text = ""
            if red_health <= 0 :
                winner_text = "YELLOW WON!"
            if yellow_health <= 0: 
                winner_text = "RED WON!"
            if  winner_text:
                draw_winner(winner_text)
                run =False
                break

        keys_pressed = pygame.key.get_pressed()
        red_movemnts(keys_pressed , red)
        yellow_movemnts(keys_pressed , yellow)
        handle_bullets(red_bull , yell_bull , red , yellow )


        draw_window(red , yellow , red_bull ,yell_bull , red_health , yellow_health)
    main()

if __name__ == '__main__':
    main()
