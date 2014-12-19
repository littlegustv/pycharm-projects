import gameobject
import math
from pyglet import *
from pyglet.gl import *

class elevator(gameobject.gameobject):

    velY = 0.0
    maxSpeed = 200.0
    direction = 0
    acelY = 1000.0
    passengers = []
    floor = 0

    def draw(self):
        graphics.draw_indexed(4, gl.GL_TRIANGLES,
                      [0,1,2,0,2,3],
                      ('v2f', (self.x,self.y,
                               self.x + self.width, self.y,
                               self.x + self.width, self.y + self.height,
                               self.x, self.y + self.height)),
                              ('c4B', self.color * 4))
        graphics.draw_indexed(3, gl.GL_TRIANGLES,
                      [0,1,2,0],
                      ('v2f', (self.x + 2 * self.width / 3,self.y,
                               self.x + self.width, self.y,
                               self.x + self.width, self.y + self.height)),
                              ('c4B', (51,32,10,255) * 3))
        graphics.draw_indexed(3, gl.GL_TRIANGLES,
                      [0,1,2,0],
                      ('v2f', (self.x, self.y + self.height,
                               self.x + self.width, self.y + self.height,
                               self.x + self.width/2, self.y + 3*self.height /4)),
                              ('c4B', (100,100,100,255) * 3))
        for p in self.passengers:
            p.draw()

    def update(self, dt):
        move = True
        if self.y  < 50:
            self.velY = max(0, self.velY)
            self.y = 50
        elif self.y > 10 * 50:
            self.velY = min(0, self.velY)
            self.y = 10 * 50
        self.y += self.velY * dt
        for p in self.passengers:
            p.destX = self.x + 12 * (self.passengers.index(p)) + 2
            p.y = self.y + 2
            p.update(dt)
            if p.moving:
                move = False
        if not self.direction == 0 and move:
            if abs(self.velY) < self.maxSpeed:
                self.velY += self.direction * self.acelY * dt
        elif move:
            if self.y % 50 < 5:
                self.velY = 0
                self.y = self.y - self.y % 50
                self.floor = int(self.y / 50) - 1
            elif self.y % 50 > 45:
                self.velY = 0
                self.y = (self.y - self.y % 50) + 50
                self.floor = int(self.y / 50) - 1
        else:
            self.floor = - 1        
