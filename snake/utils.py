from random import choice

HEIGHT, WIDTH = 500, 500

def random_block(body):
    while True:
        x, y = choice(range(0, WIDTH, 10)), choice(range(0, HEIGHT, 10))
        if not (x,y) in body:
            return (x, y)
