from pyglet import graphics
from pyglet.gl import *

class gameobject():

    def __init__(self, x, y, width, height, color=(255,255,255,255)):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        
    def draw(self):
        graphics.draw_indexed(4, gl.GL_TRIANGLES,
                      [0,1,2,0,2,3],
                      ('v2f', (self.x,self.y,
                               self.x + self.width, self.y,
                               self.x + self.width, self.y + self.height,
                               self.x, self.y + self.height)),
                              ('c4B', self.color * 4))      

    def update(self, dt):
        pass
