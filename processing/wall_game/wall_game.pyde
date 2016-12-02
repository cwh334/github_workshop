import os
path = os.getcwd()

class Runner:
    def __init__(self, x, y, ground):
        self.x = x
        self.y = y
        self.r = 35
        self.ground = ground
        self.vx = 1
        self.vy = 0
        
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
        self.vx += 0.1
        self.y += self.vy
        
    def display(self):
        self.update()
        ellipse(self.x, self.y, self.r * 2, self.r * 2)

class Game:
    def __init__(self):
        self.w = 1280
        self.h = 720
        self.ground = 650
        self.state = ""
        self.runner = Runner(self.w / 2, self.ground - 35, self.ground)
        self.x = self.w
        self.x1 = self.w
        self.x2 = self.w
    
    def loadImage(self):
        pass
    
    def scroll(self, border, percentage):
        speed = self.runner.vx * percentage
        if (border - speed) >= 0:
            border -= speed
        else:
            border = self.w - speed + border
    
    def update(self):
        self.scroll(self.x, 1)
        self.scroll(self.x1, 0.9)
        self.scroll(self.x2, 0.8)
        
    def display(self):
        self.runner.display()
        self.update()
        line(self.x, 0, self.x, self.h)
        line(self.x1, 0, self.x1, self.h)
        line(self.x2, 0, self.x2, self.h)
        
    
    
    
game = Game()
    
def setup():
    size(game.w, game.h)
    fill(255)
    stroke(255)
    background(0)
    line(game.x, 0, game.x, game.h)
def draw():
    background(0)
    game.display()
    