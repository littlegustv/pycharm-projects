from pyglet import *
import gameobject

class button(gameobject.gameobject):

    def __init__(self,x,y,txt,action):
        self.x = x
        self.y = y
        self.text = text.Label(txt + '\n', font_name="Tulpen One", font_size=24, color=(0,0,0,255),x=self.x,y=self.y + 18,width=58,multiline=True,halign='center', bold=True)
        self.action = action
        self.timeout = 0.0
        self.width = 58
        self.height = 60
        self.color = (0,0,0,255)
        self.thickness = 4

    def press(self):
        if self.timeout <= 0:
            self.timeout = 5.0
            self.color = (150,0,0,255)
            self.text.color = (255,255,255,255)
            self.action()


    def update(self,dt):
        if self.timeout > 0.0:
            self.timeout -= dt
            self.color = (int((5.0 - self.timeout) * 30),int((5.0 - self.timeout) * 30),int((5.0 - self.timeout) * 30),255)
            self.text.color = (int(self.timeout * 51),int(self.timeout * 51),int(self.timeout * 51),255)
        else:
            self.color = (0,0,0,255)
            self.text.color = (0,0,0,255)

    def draw(self):
        graphics.draw_indexed(4, gl.GL_TRIANGLES,
                      [0,1,2,0,2,3],
                      ('v2f', (self.x - self.thickness,self.y - self.thickness,
                               self.x + self.width + self.thickness, self.y - self.thickness,
                               self.x + self.width + self.thickness, self.y + self.height + self.thickness,
                               self.x - self.thickness, self.y + self.height + self.thickness)),
                              ('c4B', (255,255,255,255)*4))
        graphics.draw_indexed(4, gl.GL_TRIANGLES,
                      [0,1,2,0,2,3],
                      ('v2f', (self.x,self.y,
                               self.x + self.width, self.y,
                               self.x + self.width, self.y + self.height,
                               self.x, self.y + self.height)),
                              ('c4B', self.color * 4))
        #self.text.color = (0,0,0,255)
        #self.text.x -= 1
        #self.text.y -= 1
        #self.text.draw()
        self.text.color = (255,255,255,255)
        #self.text.x += 1
        #self.text.y += 1
        self.text.draw()
