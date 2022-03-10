from random import choice, randint

class Snake:
    def __init__(self , body , direction):
        self.body = body
        self.direction = direction
    
    def set_dir(self , dir):
        self.direction = dir

    def move(self , pos):
        self.body = self.body[1:] + [pos]
    
    def head(self):
        return self.body[-1]
    

class Apple():
    def __init__(self ,p = 1) -> None:
        self.p = p
    
    def location(self , w , h , s):
        while True:
            self.x, self.y = randint(0, h), randint(0, w)
            if not (self.x,self.y) in s:
                return (self.x, self.y)


class Game :
  def __init__(self, width , height): 
    self.width = width
    self.height = height
    self.snake = Snake([(0,0),(0,1),(0,2)], Right)
    self.score = 0

  def board_matrix(self):
    l = [['' for i in range(self.width)] for j in range(self.height)]
    b =  self.snake.body[:-1]
    for x in b:
        i , j = x
        l[i][j] = 'O'
    i , j = self.snake.head()
    l[i][j] = 'X'
    return l

  def render(self , loc) :
    matrix = self.board_matrix()
    print(matrix)
    matrix[loc[0]][loc[1]] = '*'
    char = 'Score: ' + str(self.score)
    print(char.rjust(self.width)) 
    print('+' + '-' * self.width + '+')
    for row in matrix:
        print('|', end ='',sep ='')
        for x in range(self.width):
            if not row[x]: w = ' '
            else: w = row[x]
            print(w, end = '' ,sep = '')
        print('|')
    print('+' + '-' * self.width + '+')

def  is_gameover( l):
        h = l[-1]
        for x in  l[:-1]:
            if x == h:
                return False
        return True

if __name__ == '__main__':
    Left = (0 , -1)
    Up  = (-1 , 0)
    Right =(0 , 1)
    Down  = (1 , 0)
    i ={
        'w' : Up, 
        'a' : Left,
        's' : Down,
        'd' : Right,
    }
    game = Game(20, 10)
    apple = Apple()
    l = apple.location(game.width , game.height , game.snake.body)
    game.render(l)         

    while True:
        enter = input().lower()
        if enter == 'q': break
        if not enter: x = game.snake.direction      
        else: x = i[enter]
        h0 , h1 = game.snake.head()
        v = h0 + x[0]
        z = h1 + x[1]
        if v < 1 : v += 10
        if z < 1 : z += 20
        if v == game.height : v=0
        if z == game.width: z = 0
        game.snake.set_dir(x) 
        pos = (v , z)
        game.snake.move(pos)
        if game.snake.head() == l:
            l = apple.location(game.width , game.height , game.snake.body)
            b = game.snake.body[0]
            game.snake.body.insert(0,b)
            game.score += 1
        if not is_gameover(game.snake.body):
            print('Your Score is: ', game.score )
            print('Game over')
            break
        game.render(l)
