__author__ = 'littlegustv'

import player
import pyglet
import math
import random

class SubGhost(player.Player):

    type = "Subghost"
    jumptimer = 0
    jumpstrength = 308
    jump = False
    destX = 0

    circle_t = 0
    circle_a = 0
    circle_b = 0
    circle_r = 0

    frames = []
    frame = 0
    animation = 0

    collected = False
    rotateT = 0

    def draw(self):
        self.sprite.draw()
        if not self.collected:
            pyglet.graphics.draw(1, pyglet.gl.GL_POINTS, ('v2i', (int(self.x + random.randint(-10,10)), int(self.y + random.randint(-10,10)))))

    def move(self, dt):

        if self.collected:
            self.velY -= int(self.gravity * dt)
            self.x += int(self.velX * dt)
            self.y += int(self.velY * dt)
        else:
            a = 3
            b = math.pi / 2
            self.x += math.sin(self.rotateT) / 2
            self.y += math.sin(a * self.rotateT + b)

        if self.jumptimer > 0:
            self.jumptimer -= dt
        if self.jumptimer < 0:
            self.jumptimer = 0
            if self.jump:
                self.velY = self.jumpstrength


    def update(self, dt):

        self.jump = False

        if not self.collected:
            self.rotateT += dt * 2
        elif self.destX > self.x + 8:
            self.velX = self.speed
            self.animation = 1
        elif self.destX < self.x - 8:
            self.velX = -self.speed
            self.animation = 0
        else:
            self.velX = self.destX - self.x

        if abs(self.velX) > 10:
            self.frame += 1
            self.sprite = pyglet.sprite.Sprite(self.frames[self.animation * 2 + int(self.frame / 10) % 2], x=self.x, y=self.y)
        else:
            self.frame = 0
            self.sprite = pyglet.sprite.Sprite(self.frames[self.animation * 2 + int(self.frame / 10) % 2], x=self.x, y=self.y)

        if self.circle_t > 0:
            self.collideable = False
            self.gravity = 0
            self.do_circle(self.circle_t, self.circle_a, self.circle_b, self.circle_r)
            self.circle_t -= dt
        else:
            self.collideable = True

    def do_circle(self, t, a, b, r):
        self.x = a + r * math.cos(2*t)
        self.y = b + r * math.sin(2*t)

    def set_circle(self, t, a, b, r):
        if self.circle_t > 0:
            return
        self.circle_a = a
        self.circle_b = b
        self.circle_r = r
        self.circle_t = t