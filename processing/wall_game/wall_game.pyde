import os
from random import randint
path = os.getcwd()

class Runner:
    def __init__(self, x, y, ground):
        self.x = x
        self.y = y
        self.r = 45
        self.ground = ground
        self.vx = 1
        self.vy = 0
        self.hammers = []
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
        self.vx += 0.002
                
        if self.jump:
            self.vy -= 0.5

        self.y += self.vy
        
        for hammer in self.hammers:
            if hammer.throw == True:
                hammer.vx = self.vx + 5
                hammer.vy = self.vy

    def display(self):
        self.update()
        ellipse(self.x, self.y, self.r * 2, self.r * 2)
        
        ellipse(30, 30, 30, 30)
        ellipse(60, 30, 30, 30)

class Wall:
    def __init__(self, x = 1280, game_w = 1280, game_h = 720):
        self.w = randint(60, 80)
        self.h = randint(300, 550)
        self.x = x
        self.y = game_h - self.h
    
    def loadImage(self):
        pass
    
    def display(self):
        rect(self.x, self.y, self.w, self.h)    
    
class Hammer:
    def __init__(self, x = 1600):
        self.x = x
        self.y = randint(50, 600)
        self.r = 25
        self.vx = 0
        self.vy = 0
        self.throw = False
        self.collected = False
        
    def loadImage(self):
        pass
        
    def update(self):
        if self.throw:
            self.x += self.vx
            self.y += self.vy
        
    def display(self):
        if not self.collected or self.throw:
            ellipse(self.x, self.y, self.r * 2, self.r * 2)

class Game:
    def __init__(self):
        self.w = 1280
        self.h = 720
        self.ground = 670
        self.state = ""
        self.runner = Runner(self.w / 2, self.ground - 35, self.ground)
        self.layers = [self.w, self.w, self.w]
        self.walls = [Wall(), Wall(1920)]
        self.hammers = []
        self.state = "play"

    def loadImage(self):
        pass
    
    def update(self):
        ratio = 1
        for i in range(len(self.layers)):
            speed = self.runner.vx * ratio
            if self.layers[i] - speed < 0:
                self.layers[i] += (self.w - speed)
            else:
                self.layers[i] -= speed
            ratio -= 0.1
        
        for wall in self.walls:
            wall.x -= self.runner.vx
            if collision(self.runner, wall):
                self.state = "over"
                
            if wall.x < 0:
                del self.walls[0]
                self.walls.append(Wall())
                prob = randint(1, 2)
                if prob == 1:
                    self.hammers.append(Hammer())
        
        for hammer in self.hammers:
            hammer.x -= self.runner.vx  
            if collision(self.runner, hammer):
                self.runner.hammers.append(hammer)
                self.hammers.remove(hammer)
            if hammer.x < 0:
                del hammer

    def display(self):
        # self.runner.display()
        self.update()

        line(self.layers[0], 0, self.layers[0], self.h)
        line(self.layers[1], 0, self.layers[1], self.h)
        line(self.layers[2], 0, self.layers[2], self.h)
        self.runner.display()
    
        for wall in self.walls:
            wall.display()
        
        for hammer in self.hammers:
            hammer.display()
            
def collision(a, b, game_h = 720):
    if isinstance(a, Runner) and isinstance(b, Wall):
        if a.y > game_h - b.h - a.r and b.x - a.r < a.x < b.x + b.w + a.r:
            return True
        else:
            return False
    if isinstance(a, Runner) and isinstance(b, Hammer):
        if ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5\
            < a.r + b.r:
            return True
        else:
            return False
    if isinstanct(a, Hammer) and (b, Wall):
        if a.y > b.y and a.r > b.x - a.x:
            return True
        else:
            return False
    
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
    if keyCode == UP:
        game.runner.jump = True
    if keyCode == RIGHT:
        if len(game.runner.hammers) > 0:
            line(0, 0, 500, 500)
            game.runner.hammer[0].throw = True
        
def keyReleased():
    game.runner.jump = False



    