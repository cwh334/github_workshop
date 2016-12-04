import os
from random import randint
path = os.getcwd()

ground = 670
game_width = 1280
game_height = 720

def collision(a, b):
    # returns True if two targets collide. Target argument in the order of: runner, hammer, wall
    if (isinstance(a, Runner) and isinstance(b, Wall)) or (isinstance(a, Hammer) and (b, Wall)):
        if b.y + b.h + a.r > a.y > b.y - a.r and b.x - a.r < a.x < b.x + b.w + a.r:
            return True
        else:
            return False
    if isinstance(a, Runner) and isinstance(b, Hammer):
        if ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5\
            < a.r + b.r:
            return True
        else:
            return False

class Runner:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 45
        self.ground = ground
        self.vx = 1 # runner keeps running to the right at the same speed throughout
        self.vy = 0
        self.hammers = [] # hammers obtained
        self.thrown = [] # hammers thrown
        self.jump = False
        
    def loadImage(self):
        pass
        
    def gravity(self):
        if self.y + self.r < self.ground:
            self.vy += 0.1
            if self.y + self.r + self.vy > self.ground:
                self.vy = self.ground - self.r - self.y
        else:
            self.vy = 0

    def update(self):
        self.gravity()
        self.vx += 0.002 # level gradually increases as the speed increases
                
        if self.jump:
            self.vy -= 0.5

        self.y += self.vy
        
        for hammer in self.hammers:
            # obtained hammers displayed on the top left corner
            hammer.x = 30 + (60 * self.hammers.index(hammer))
            hammer.y = 30
            # Throw a hammer: hammer goes to another list "thrown" to stop looping
            if hammer.throw == True:
                hammer.x = hammer.owner.x
                hammer.y = hammer.owner.y
                hammer.vx = self.vx + 5
                hammer.vy = self.vy
                self.thrown.append(self.hammers.pop(0))     

    def display(self):
        self.update()
        ellipse(self.x, self.y, self.r * 2, self.r * 2)
        for hammer in self.hammers:
            hammer.display()
        for hammer in self.thrown:
            hammer.display()
        

class Wall:
    def __init__(self, x = game_width):
        # randomly assign width and height of walls
        self.w = randint(60, 90)
        self.h = randint(300, 525)
        self.x = x
        self.y = 0
        self.vy = 0
        self.ground = ground
        # when knocked down by a thrown hammer, no longer apply to collisions
        self.knocked_down = False
    
    def loadImage(self):
        pass
        
    def gravity(self):
        # visual effect of walls being built on spot
        if self.y + self.h < self.ground:
            self.vy += 0.1
            if self.y + self.h + self.vy > self.ground:
                self.vy = self.ground - self.h - self.y
        else:
            self.vy = 0
                
    def update(self):
        self.gravity()
        self.y += self.vy
    
    def display(self):
        self.update()
        if not self.knocked_down:
            rect(self.x, self.y, self.w, self.h)
        else:
            # display transparent walls if knocked down
           pass 
    
class Hammer:
    def __init__(self, x = game_width * 1.25):
        self.x = x
        self.y = randint(50, 600) # place hammers at random height
        self.r = 25
        self.ground = ground
        self.vx = 0
        self.vy = 0
        self.throw = False
        self.owner = ""
        
    def loadImage(self):
        pass
    
    def gravity(self):
        if self.y + self.r < self.ground:
            self.vy += 0.1
            if self.y + self.r + self.vy > self.ground:
                self.vy = self.ground - self.r - self.y
    
    def update(self):
        # hammers only fly when thrown. otherwise stationed
        if self.throw:
            self.gravity()
            self.x += self.vx
            self.y += self.vy
            
    def display(self):
        self.update()
        ellipse(self.x, self.y, self.r * 2, self.r * 2)

class Game:
    def __init__(self):
        self.w = game_width
        self.h = game_height
        self.ground = ground
        self.state = "play" # menu, play, over, fly
        self.runner = Runner(self.w / 2, ground - 35)
        self.layers = [self.w, self.w, self.w] # record start of each background layer
        self.walls = [Wall(), Wall(game_width * 1.5)]
        self.hammers = []

    def loadImage(self):
        pass
    
    def update(self):
        
        ratio = 1
        for i in range(len(self.layers)):
            # the speed in which each layer moves (different ratios)
            speed = self.runner.vx * ratio
            if self.layers[i] - speed < 0:
                self.layers[i] += (self.w - speed)
            else:
                self.layers[i] -= speed
            ratio -= 0.1 # layers at the back moves slower
        
        for wall in self.walls:
            wall.x -= self.runner.vx
            # check if runner hits the wall
            if collision(self.runner, wall) and not wall.knocked_down:
                self.state = "over"
            # when a wall disappears out of screen, built another
            if wall.x < 0:
                del self.walls[0]
                self.walls.append(Wall())
                # the chances of a hammer appearing after each wall
                prob = randint(1, 8)
                if prob == 1:
                    self.hammers.append(Hammer())
                    
            for hammer in self.runner.thrown:
                # when hammer hits wall, hammer disappears and wall knocked down
                if collision(hammer, wall) and not wall.knocked_down:
                    self.runner.thrown.remove(hammer)
                    wall.knocked_down = True
                    # self.knocked_down.append(self.walls.pop(self.walls.index(wall)))
        
        for hammer in self.hammers:
            hammer.x -= self.runner.vx  
            # runner obtains hammer upon collision
            if collision(self.runner, hammer):
                hammer.owner = self.runner
                self.runner.hammers.append(self.hammers.pop(self.hammers.index(hammer)))
            # remove hammer from list when disappears from screen unobtained
            if hammer.x < 0:
                self.hammers.remove(hammer)

    def display(self):
        
        self.update()
        # lines represent the background
        line(self.layers[0], 0, self.layers[0], self.h)
        line(self.layers[1], 0, self.layers[1], self.h)
        line(self.layers[2], 0, self.layers[2], self.h)
        self.runner.display()
    
        for wall in self.walls:
            wall.display()

        for hammer in self.hammers:
            hammer.display()
    
game = Game() 
    
def setup():
    size(game.w, game.h)
    fill(255)
    stroke(255)
    background(0)

def draw():
    background(0)
    game.display()
    
def keyPressed():
    if keyCode == UP: # jump
        game.runner.jump = True
    if keyCode == RIGHT: # throw first hammer
        if len(game.runner.hammers) > 0:
            game.runner.hammers[0].throw = True
            
def keyReleased():
    game.runner.jump = False



    