add_library("minim")
minim = Minim(this)
import os
from random import randint
path = os.getcwd()

r = open("ranking.txt", "r+")
ranking = []
for entry in r:
    tmp = []
    for item in entry:
        tmp.append(item)
    ranking.append(tmp)
print(ranking)

ground = 670
game_width = 1280
game_height = 720
img_wall = loadImage(path + "/wall.png")
img_transwall = loadImage(path + "/transwall.png")
img_hammer = loadImage(path + "/hammer.png")

def collision(a, b):
    # returns True if two targets collide. 
    # target argument in the order of: runner, hammer, wall
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
        
def gravity(obj, dis):
    # obj: the object applying gravity to
    # dis: the distance between obj.y and its bottom end
    if obj.y + dis < obj.ground:
        obj.vy += 0.1
        # to ensure runner cannot go under ground level
        if obj.y + dis + obj.vy > obj.ground:
            obj.vy = obj.ground - dis - obj.y
    else:
        obj.vy = 0

class Runner:
    def __init__(self, x, y, fly = False):
        self.x = x
        self.y = y
        self.r = 45
        self.ground = ground
        self.vx = 1 # runner keeps running to the right at the same speed throughout
        self.vy = 0
        self.hammers = [] # hammers obtained
        self.thrown = [] # hammers thrown
        self.jump = False
        self.fly = fly
        if self.fly:
            self.y = game_height
            self.vy = - 3
        self.frame_num = 0 # the current runner frame
        self.frame_total = 6 
        self.switch = 0 # control the speed of switching frames
        self.frame_num_f = 0 # the current flying frame
        self.frame_total_f = 2 
        self.img = loadImage(path + "/trump.png")
        self.img_fly = loadImage(path + "/trumpwings.png")

    def update(self):
        # for every 3 draws switch frame
        if self.switch == 2:
            self.frame_num = (self.frame_num + 1) % self.frame_total
            
        if not self.fly:
            gravity(self, self.r)
        
        self.vx += 0.002 # level gradually increases as the speed increases
                
        if self.jump:
            self.vy -= 0.5
        # when out of screen display flying character from ground
        if self.fly:
            self.x += self.vx
            if self.switch == 2:
                self.frame_num_f = (self.frame_num_f + 1) % self.frame_total_f
        
        self.switch = (self.switch + 1) % 3
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
        
        if self.fly:
            image(self.img_fly, self.x - self.r * 3, self.y - self.r, self.r * 6, self.r * 2,\
                  int(self.frame_num_f * self.r * 6), 0,\
                  int((self.frame_num_f + 1) * self.r * 6), self.r * 2)
            # ellipse(self.x, self.y, self.r * 2, self.r * 2)

        else:
            for hammer in self.hammers:
                hammer.display()
            for hammer in self.thrown:
                hammer.display()
            # ellipse(self.x, self.y, self.r * 2, self.r * 2)
            
            image(self.img, self.x - self.r, self.y - self.r, self.r * 2, self.r * 2,\
                  int(self.frame_num * self.r * 2), 0,\
                  int((self.frame_num + 1) * self.r * 2), self.r * 2)


class Wall:
    def __init__(self, x = game_width):
        # randomly assign width and height of walls
        self.w = randint(60, 90)
        self.h = randint(350, 550)
        self.x = x
        self.y = 0
        self.vy = 0
        self.ground = ground
        # when knocked down by a thrown hammer, no longer apply to collisions
        self.knocked_down = False
        self.img = img_wall
        self.transwall = img_transwall
                
    def update(self):
        gravity(self, self.h) # visual effect of building walls
        self.y += self.vy
    
    def display(self):
        self.update()
        if self.knocked_down:
            # display transparent walls if knocked down
            image(self.transwall, self.x, self.y, self.w, self.h)
        else:
            image(self.img, self.x, self.y, self.w, self.h)
            # rect(self.x, self.y, self.w, self.h)
    
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
        self.frame_num = 0 # current frame
        self.frame_total = 6
        self.img = img_hammer
    
    def update(self):
        # hammers only fly when thrown. otherwise stationed
        if self.throw:
            gravity(self, self.r)
            self.x += self.vx
            self.y += self.vy
            self.frame_num = (self.frame_num + 1) % self.frame_total
            
    def display(self):
        self.update()
        if self.throw:
            image(self.img, self.x - self.r, self.y - self.r, self.r * 2, self.r * 2,\
                  int(self.frame_num * self.r * 2), 0,\
                  int((self.frame_num + 1) * self.r * 2), self.r * 2)
        else:
            image(self.img, self.x - self.r, self.y - self.r, self.r * 2, self.r * 2,\
                  0, 0, self.r * 2, self.r * 2)
        # ellipse(self.x, self.y, self.r * 2, self.r * 2)

class Game:
    def __init__(self):
        self.w = game_width
        self.h = game_height
        self.ground = ground
        self.state = "menu" # menu, play, over, fly
        self.runner = Runner(self.w / 2, ground - 35)
        self.layers = [self.w, self.w, self.w] # start of each background layer
        self.walls = [Wall(), Wall(game_width * 1.5)] # create first 2 walls to display 
        self.hammers = [] # hammers available
        self.bg = [] # 3 background layers
        for i in range(3, 0, -1):
            img = loadImage(path + "/layer" + str(i) + ".png")
            self.bg.append(img)
        self.play_button = loadImage(path + "/play_button.png")
        self.gameover = loadImage(path + "/gameover.png")
        self.restart = loadImage(path + "/text.png")
        self.stars = loadImage(path + "/stars.png")
        self.sky = loadImage(path + "/sky.png")
        self.frame_num_s = 0 # current stars frame (to be displayed above runner)
        self.frame_total_s = 4
        self.switch = 0
        self.score = 0 # number of walls runner jumps pass
        self.sound_start = minim.loadFile(path + "/are_you_ready.mp3")
        self.sound_end = minim.loadFile(path + "/and_i_said.mp3")
        
    def update(self):
        if self.state == "play":
            ratio = 1
            for i in range(len(self.layers)):
                # the speed in which each layer moves (different ratios)
                speed = self.runner.vx * ratio
                if self.layers[i] - speed < 0:
                    self.layers[i] += (self.w - speed)
                else:
                    self.layers[i] -= speed
                ratio -= 0.15 # layers at the back moves slower
            
            # if runner goes out of screen, fly
            if self.runner.y < -self.runner.r:
                self.state = "fly"
                self.runner = Runner(self.w / 2, ground - 35, True)
            
            for wall in self.walls:
                wall.x -= self.runner.vx
                # check if runner hits the wall
                if collision(self.runner, wall) and not wall.knocked_down:
                    self.state = "over"
                # when a wall disappears out of screen, built another
                if wall.x < 0:
                    self.score += 1
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
                    
        if self.state == "fly":
            # when runner jumps out of screen, display flying character
            # when flying character flies out of screen, game over
            if self.runner.x > game_width or self.runner.y < 0:
                self.state = "over"
                
        if self.state == "over":
            # if runner hits the wall, display turing stars above
            if not self.runner.fly:
                if self.switch == 2:
                    self.frame_num_s = (self.frame_num_s + 1) % self.frame_total_s
                self.switch = (self.switch + 1) % 3
                self.runner.y = ground - 35
            for entry in ranking:
                if self.score > int(entry[0]):
                    self.name = input("Congratulations! Please enter your name: ")
                    ranking.insert(ranking.index(entry) - 1, [self.score, self.name])
                    ranking.pop()
                    break
            for entry in ranking:
                r.write(str(entry[0]) + "," + self.name + "\n")
            
    def display(self):
        self.update()
        if self.state == "play":
            
            for img in self.bg:
                loc = self.layers[self.bg.index(img)] # starting point
                image(img, loc, 0)
                image(img, loc - self.w, 0)
            self.runner.display()
            for wall in self.walls:
                wall.display()
            for hammer in self.hammers:
                hammer.display()
                
        elif self.state == "menu":
            # rect(600, 350, 80, 20)
            image(self.play_button, 580, 345, 120, 30)
            
        elif self.state == "over":
            text(self.score, 635, 380)
            image(self.gameover, 460, 110)
            image(self.restart, 460, 350)
            if not self.runner.fly:
                image(self.stars,\
                      self.runner.x - self.runner.r, self.runner.y - self.runner.r * 2,\
                      self.runner.r * 2, self.runner.r,\
                      int(self.frame_num_s * self.runner.r * 2), 0,\
                      int((self.frame_num_s + 1) * self.runner.r * 2), self.runner.r)
                image(self.runner.img,\
                      self.runner.x - self.runner.r, self.runner.y - self.runner.r,\
                      self.runner.r * 2, self.runner.r * 2,\
                      0, 0,\
                      self.runner.r * 2, self.runner.r * 2)
                self.sound_start.pause() # avoid sound overlap
                self.sound_end.play()
            tmp = 0
            for entry in ranking:
                text(str(entry[0]) + "\t" + entry[1], 0, tmp)
                tmp += 20
            
        else:
            image(self.sky, 0, 0)
            self.runner.display()
            self.sound_start.pause()
            self.sound_end.play()
    
game = Game() 

def setup():
    size(game.w, game.h, P2D)
    fill(255)
    background(0)

def draw():
    background(0)
    game.display()
    
def keyPressed():
    if game.state == "over":
        game.state = "menu"
    elif game.state == "play":
        if keyCode == UP: # jump
            game.runner.jump = True
        if keyCode == RIGHT: # throw first hammer
            if len(game.runner.hammers) > 0:
                game.runner.hammers[0].throw = True
            
def keyReleased():
    game.runner.jump = False

def mouseClicked():
    if game.state == "menu" and 600 < mouseX < 680 and 350 < mouseY < 370:
        game.__init__()
        game.sound_end.pause()
        game.sound_start.play()
        game.state = "play"