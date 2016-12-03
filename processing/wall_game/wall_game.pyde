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
        self.hammer = False
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
        self.vx += 0.01
                
        if self.jump:
            self.vy -= 0.5

        self.y += self.vy

    def display(self):
        self.update()
        ellipse(self.x, self.y, self.r * 2, self.r * 2)
        
class Wall:
    def __init__(self, x = 1280, game_w = 1280, game_h = 720):
        self.w = randint(60, 80)
        self.h = randint(300, 560)
        self.x = x
        self.y = game_h - self.h
    
    def loadImage(self):
        pass

class Hammer:
    def __init__(self, x, y):
        self.x = x
        self.y = randint(50, 600)
        self.r = 25
        
    def loadImage(self):
        pass

class Game:
    def __init__(self):
        self.w = 1280
        self.h = 720
        self.ground = 650
        self.state = ""
        self.runner = Runner(self.w / 2, self.ground - 35, self.ground)
        self.layers = [self.w, self.w, self.w]
        self.walls = [Wall(), Wall(1920)]

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
            if wall.x <= 0:
                del self.walls[0]
                self.walls.append(Wall())
        
    def display(self):
        self.runner.display()
        self.update()

        line(self.layers[0], 0, self.layers[0], self.h)
        line(self.layers[1], 0, self.layers[1], self.h)
        line(self.layers[2], 0, self.layers[2], self.h)
    
        for wall in self.walls:
            rect(wall.x, wall.y, wall.w, wall.h)
    
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
        
def keyReleased():
    game.runner.jump = False



    