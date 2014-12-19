__author__ = 'littlegustv'

import globals
import pyglet

class GameObject:

    type = ""
    cleanup = False
    x = 0
    y = 0
    velX = 0
    velY = 0
    gravity = 0

    #collided is a list of all objects currently collided with it...
    collided = {}
    collideable = True


    def __init__(self, sprite):
        self.sprite = sprite
        self.height = sprite.image.height
        self.width = sprite.image.width
        self.position = sprite.position
        self.x = sprite.x
        self.y = sprite.y

    def draw(self):
        return

    def update(self, dt):
        return

    def move(self, dt):
        self.x += int(self.velX * dt)
        self.y += int(self.velY * dt)
        self.velY -= int(self.gravity * dt)

    def collides_with(self, other):
        if (self == other):
            return False

        x_distance = int(self.width / 2 + other.width / 2) + 1
        y_distance = int(self.height / 2 + other.height / 2) + 1

        dx = int(abs(self.x - other.x))
        dy = int(abs(self.y - other.y))

        return (dx < x_distance and dy < y_distance)

    def handle_collision(self, other):
        return