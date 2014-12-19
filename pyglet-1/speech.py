__author__ = 'littlegustv'

import pyglet
import gameobject
import resources

class Speech(gameobject.GameObject):

    text = ''
    width = 0
    height = 0

    def __init__(self, text, x=100, y=100):
        self.text = text
        self.x = x
        self.y = y
        self.opacity = 255
        self.label = pyglet.text.Label(text,
                          font_name='Tulpen One',
                          font_size=24,
                          x=x + 8, y=y + 60, width=160,
                          color=(0,0,0,self.opacity))

    def draw(self):
        self.drawbubble(192, 96)
        self.label.draw()
        pyglet.gl.glFlush()


    def update(self, dt):
        self.label.x = self.x + 8
        self.label.y = self.y + 60
        self.label.color = (0,0,0,self.opacity)
        return

    def rounded(self, x, y, radius):
        list = []
        for i in range(x, radius):
            list.append(x, (radius - x ** 2) ** (0.5))
        return list

    def drawbubble(self, w, h):
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
            ('v2i', (self.x + 13, self.y + 16,
                    self.x + 42, self.y + 48,
                    self.x + 86, self.y + 48,
                     self.x + 22, self.y + 16
                    )),
             ('c4B', (0, 0, 0, self.opacity) * 4)
        )
        pyglet.graphics.draw(8, pyglet.gl.GL_POLYGON,
            ('v2i', (
                 self.x + 14, self.y + 45,
                 self.x - 3, self.y + 61,
                 self.x - 3, self.y + h - 13,
                 self.x + 14, self.y + h + 3,
                 self.x + w + 1, self.y + h + 3,
                 self.x + w + 19, self.y + h - 16,
                 self.x + w + 19, self.y + 63,
                 self.x + w + 1, self.y + 45
                 )),
            ('c4B', (0, 0, 0, self.opacity) * 8)
        )
        pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLES,
            ('v2i', (self.x + 16, self.y + 16,
                    self.x + 48, self.y + 48,
                    self.x + 80, self.y + 48
                 )),
            ('c4B', (255, 255, 255, self.opacity) * 3)
        )
        pyglet.graphics.draw(8, pyglet.gl.GL_POLYGON,
            ('v2i', (
                 self.x + 16, self.y + 48,
                 self.x + 0, self.y + 64,
                 self.x + 0, self.y + h - 16,
                 self.x + 16, self.y + h,
                 self.x + w, self.y + h,
                 self.x + w + 16, self.y + h - 16,
                 self.x + w + 16, self.y + 64,
                 self.x + w, self.y + 48
                 )),
            ('c4B', (255, 255, 255, self.opacity) * 8)
        )