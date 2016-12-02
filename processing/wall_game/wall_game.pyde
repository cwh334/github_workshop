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
        self.vx += 0.05
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
        self.layers = [self.w, self.w, self.w]
        self.x = self.w
        self.x1 = self.w
        self.x2 = self.w
        self.vx = self.runner.vx
        self.vx1 = self.runner.vx * 0.9
        self.vx2 = self.runner.vx * 0.8
    
    def loadImage(self):
        pass
    
    def update(self):
        ratio = 1
        for layer in self.layers:
            speed = self.runner.vx * ratio
            if layer - speed < 0:
                layer = self.w - speed + layer
            else:
                layer -= speed
            ratio -= 0.1
        
        # self.x -= self.vx
        # self.x1 -= self.vx1
        # self.x2 -= self.vx2
        
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

def draw():
    background(0)
    game.display()
    
    