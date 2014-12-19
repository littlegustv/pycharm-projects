__author__ = 'littlegustv'

import gameobject

class Solid(gameobject.GameObject):

    type = "Solid"

    def __init__(self, x, y, height, width):
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.position = (x, y)

    def draw(self):
        return
        #self.sprite.draw()