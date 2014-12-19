__author__ = 'littlegustv'

import gameobject
import pyglet

class Hazard(gameobject.GameObject):

    type = "Hazard"

    frames = []
    frame = 0
    animation = 0
    gravity = 600
    velX = 100

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        if abs(self.velX) > 10:
            self.frame += 1
            self.sprite = pyglet.sprite.Sprite(self.frames[self.animation * 2 + int(self.frame / 10) % 2], x=self.x, y=self.y)
        else:
            self.frame = 0
            self.sprite = pyglet.sprite.Sprite(self.frames[self.animation * 2 + int(self.frame / 10) % 2], x=self.x, y=self.y)

    def handle_collision(self, other):

        self.gravity = 600

        if self.collides_with(other) and other.type == "Solid":
#            print self.x, self.y, " >>> ", other.x / 32, other.y / 32
            dx = int(other.width + self.width)/2 - 2
            dy = int(other.height + self.height)/2 - 2
            if (other.x - dx < self.x < other.x + dx):
                if (self.y > other.y):
                    self.gravity = 0;
                    self.velY = max(self.velY, 0)
                    self.y = int(other.y + other.height / 2 + self.height / 2)
                    if (other.type == "Solid"):
                        self.jump = True
                    #print "top"
                elif (self.y < other.y):
                    self.velY = min(self.velY, 0)
                    self.y = int(other.y - other.height / 2 - self.height / 2)
                    #print "bottom"
            elif (other.y - dy < self.y < other.y + dy):
                self.velX *= -1
                if (other.x > self.x):
                    self.animation = 0
                else:
                    self.animation = 1
                """
                if (other.x > self.x):
                    self.velX = min(0, self.velX)
                elif (other.x < self.x):
                    self.velX = max(0, self.velX)
                """
                #print "side"