__author__ = 'littlegustv'

import gameobject
import pyglet
import speech
import shader

class Player(gameobject.GameObject):

    type = "Player"
    gravity = 600
    speed = 200
    jumpstrength = 300

    right = False
    left = False
    frames = []
    frame = 0
    animation = 2
    velX = 0
    velY = 0
    jump = False

    subghosts = []

    speechtimer = 0.0
    bubble = speech.Speech("", 0, 0)

    c = (-0.7, -0.384)

    def draw(self):
        #tx = self.sprite.image.get_texture()

        self.sprite.x = int(self.x)
        self.sprite.y = int(self.y)
        #self.shader.bind()
        #self.shader.uniformf('C', *self.c)
        self.sprite.draw()
        #tx.blit(self.x, self.y)
        #self.shader.unbind()
        if (self.speechtimer > 0):
            self.bubble.draw()

#        if len(self.subghosts) > 0:
#            for i in range(len(self.subghosts)):
#                self.subghosts[i].draw()

    def do_jump(self):
        if self.jump:
            self.velY = self.jumpstrength
            for i in range(len(self.subghosts)):
                self.subghosts[i].jumptimer = 0.3 * (i + 1)

    def update(self, dt):

        for col in self.collided:
            col -= 1

        self.jump = False

        if self.right:
            self.animation = 2
            self.velX = self.speed
        elif self.left:
            self.animation = 1
            self.velX = -self.speed
        else:
            if self.velX > 10:
                self.velX *= 7/8
            elif self.velX < -10:
                self.velX *= 7/8
            else:
                self.velX = 0

        if abs(self.velX) > 10:
            self.frame += 1
            self.sprite = pyglet.sprite.Sprite(self.frames[self.animation * 2 + int(self.frame / 10) % 2], x=self.x, y=self.y)
        else:
            self.frame = 0
            self.sprite = pyglet.sprite.Sprite(self.frames[self.animation * 2 + int(self.frame / 10) % 2], x=self.x, y=self.y)

        if len(self.subghosts) > 0 and self.type == "Player":
            if self.right:
                self.subghosts[0].destX = self.x - 32
            elif self.left:
                self.subghosts[0].destX = self.x + 32
            for i in range(1, len(self.subghosts)):
                if self.right:
                    self.subghosts[i].destX = self.subghosts[i - 1].x - 32
                elif self.left:
                    self.subghosts[i].destX = self.subghosts[i - 1].x  + 32

        if self.speechtimer > 0:
            self.speechtimer -= dt
            self.bubble.x = self.x
            self.bubble.y = self.y
            self.bubble.update(dt)
            self.bubble.opacity = min(255, int(255 * (self.speechtimer / 1.0)))

    def handle_collision(self, other):

        if not self.collideable:
            return

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
                    self.jump = True
                    #print "top"
                elif (self.y < other.y):
                    self.velY = min(self.velY, 0)
                    self.y = int(other.y - other.height / 2 - self.height / 2)
                    #print "bottom"
            elif (other.y - dy < self.y < other.y + dy):
                if (other.x > self.x):
                    self.velX = min(0, self.velX)
                elif (other.x < self.x):
                    self.velX = max(0, self.velX)
                #print "side"
        elif self.collides_with(other) and other.type == "JumpThru":
            dx = int(other.width + self.width)/2 - 2
            dy = int(other.height + self.height)/2 - 2
            if (other.x - dx < self.x < other.x + dx):
                if (self.y > other.y + dy / 2 and self.velY < 0):
                    self.velY = max(self.velY, 0)
                    self.gravity = 0
                    self.y = int(other.y + other.height / 2 + self.height / 2)
                    self.jump = True
                elif (self.y >= other.y + dy):
                    self.velY = max(self.velY, 0)
                    self.gravity = 0
                    self.y = int(other.y + other.height / 2 + self.height / 2)
                    self.jump = True

        elif self.collides_with(other) and other.type == "Subghost" and other not in self.subghosts and self.type == "Player":
            #other.cleanup = True
            print "hey"
            self.subghosts.append(other)
            other.collected = True

            #hazard - lose ghost if collide.
        elif self.collides_with(other) and other.type == "Hazard":
            if len(self.subghosts) > 0:
                self.speechtimer = 2.0
                self.bubble = speech.Speech("Could you come on, man?", self.x, self.y)
                sg = self.subghosts.pop()
                sg.collected = False
                self.animation = 0

        elif self.collides_with(other) and other.type == "Spirit" and self.type == "Player":
            if len(self.subghosts) >= other.rank:
                for i in range(len(self.subghosts)):
                    self.subghosts[i].set_circle(5.0 + 0.3 * (i + 1), other.x, other.y, other.width * 2)
            else:
                self.animation = 0
                self.speechtimer = 2.0
                self.bubble = speech.Speech("Could you cool it?", self.x, self.y)
                if len(self.subghosts) > 0:
                    sg = self.subghosts.pop()
                    sg.collected = False
