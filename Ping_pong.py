import pygame
import os

from pygame.version import PygameVersion
pygame.font.init()

from pygame import key

WIDTH , HEIGHT = 900, 500 
win =  pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption('Tennis')

ball_x = WIDTH//2 
ball_y = HEIGHT //2
ball_r = 20
bar_width ,bar_height = 20 , 50
vel = 5
bul_vel_x = 5
bul_vel_y = 5
red_hit = pygame.USEREVENT + 1
blue_hit = pygame.USEREVENT + 2

Lives_font = pygame.font.SysFont('comicsans' , 40)
Winner_font = pygame.font.SysFont('comicsans' , 100)
border = pygame.Rect( WIDTH // 2 - 5 , 0 , 10 , HEIGHT)
space_bg = pygame.transform.scale(pygame.image.load(os.path.join('123','space.png')) , (WIDTH ,HEIGHT))


def draw_window(red , blue , red_points , blue_points ,ball):
    win.blit(space_bg , (0 ,0))
    win.blit(space_bg , (border.x + 10 ,WIDTH))
    pygame.draw.rect(win , (255 , 0 , 0), red)
    pygame.draw.rect(win , (0 , 0, 255), blue)
    pygame.draw.rect(win , (0 , 0 , 0), border)
    red_score = Lives_font.render("Points: " + str(red_points) , 1 , (255 , 255 ,255))
    blue_score = Lives_font.render("Points: " + str(blue_points) , 1 , (255 , 255 ,255))
    win.blit(red_score , (10 , 10))
    win.blit(blue_score , (border.x + border.width + 10  , 10))
    # print('Ball:'+ str(ball.x) , str(ball.y) + "\n", str(red.x) , str(red.y) + str(blue.x) , str(blue.y))
    pygame.draw.rect(win , (255, 255, 255) , ball)
    pygame.display.update()

def red_movemnts(keys_pressed , red):
    if keys_pressed[pygame.K_w] and red.y - vel > 0: red.y -= vel
    if keys_pressed[pygame.K_s] and red.y + vel + red.height <= HEIGHT - 15: red.y += vel

def blue_movemnts(keys_pressed , blue):
    if keys_pressed[pygame.K_UP] and blue.y - vel > 0: blue.y -= vel
    if keys_pressed[pygame.K_DOWN]and blue.y + vel + blue.height <= HEIGHT: blue.y += vel


def handle_ball (ball , ball_r , red ,blue ):
    global bul_vel_y
    global bul_vel_x
    ball.x += bul_vel_x 
    ball.y += bul_vel_y 
    #Floor and ceiling
    if ball.y - ball_r <= 0: 
        bul_vel_y *= -1 
    if ball.y + ball_r >= HEIGHT -10: 
        bul_vel_y *= -1
    

    #bar collision
    if ball.x <= red.x + red.width and (red.y <= ball.y <= red.y + bar_height or
     red.y <= ball.y + ball_r <= red.y + bar_height):
        bul_vel_x *= -1
    if ball.x + ball_r >= blue.x and (blue.y <= ball.y <= blue.y + bar_height or
     blue.y <= ball.y + ball_r <= blue.y + bar_height):
        bul_vel_x *= -1
    

    if ball.x + ball_r >= WIDTH:
        ball.x = WIDTH//2 - ball_r //2
        ball.y = HEIGHT//2 - ball_r //2
        red.x = 0 
        red.y =  HEIGHT//2 - bar_height//2
        blue.x = WIDTH - bar_width 
        blue.y =  HEIGHT//2 - bar_height//2
        pygame.event.post(pygame.event.Event(red_hit))
        pygame.time.delay(1000)
    if ball.x <= 0 :
        ball.x = WIDTH//2 - ball_r //2
        ball.y = HEIGHT//2 - ball_r //2
        pygame.event.post(pygame.event.Event(blue_hit))
        pygame.time.delay(1000)
    
def draw_winner(text):
    win_text = Winner_font.render(text , 1 , (255, 255 , 255))
    win.blit(win_text , (WIDTH//2 - win_text.get_width()//2 , HEIGHT //2 - win_text.get_height()//2))
    pygame.display.update()  
    pygame.time.delay(3000)  

def main():
    red  = pygame.Rect(0 , HEIGHT//2 - bar_height//2 , bar_width , bar_height)
    blue  = pygame.Rect(900 - bar_width , HEIGHT//2 - bar_height//2 , bar_width , bar_height)
    ball = pygame.Rect( WIDTH//2 - ball_r //2 , HEIGHT//2 -  ball_r//2, ball_r , ball_r)

    red_points , blue_points = 0 , 0
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        # ball = pygame.draw.circle(win , (255, 255, 255) , (ball_x , ball_y) , ball_r)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False
                pygame.quit()
    
            if event.type == red_hit:
                red_points += 1
            if event.type == blue_hit:
                blue_points += 1
            
            winner_text = ""
            if red_points >= 10 :
                winner_text = "RED WON!"
            if blue_points >= 10: 
                winner_text = "BLUE WON!"
            if  winner_text:
                draw_winner(winner_text)
                run =False
                break

        keys_pressed = pygame.key.get_pressed()
        red_movemnts(keys_pressed , red)
        blue_movemnts(keys_pressed , blue)
        handle_ball(ball, ball_r ,red , blue )


        draw_window(red , blue   , red_points , blue_points ,ball )
    main()

if __name__ == '__main__':
    main()
