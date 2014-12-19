import gameobject
from pyglet import *
from pyglet import font

class person (gameobject.gameobject):

    def __init__(self, floor, destFloor, img, name="", faction="Neutral"):
        
        self.floor = floor
        self.destFloor = destFloor
        self.y = (floor + 1)* 50
        self.x = 200
        self.width = 10
        self.height = 20
        self.floorLabel = text.Label('', 
                          font_name='Tulpen One',
                          font_size=18,
                          x=self.x + self.width/2, y=self.y + self.height,
                          width=10, color=(0,0,0,255), bold=True, multiline=True, halign="center")
        self.waiting = 0.1
        self.highlight = False
        self.name = name
        self.faction = faction
        self.frame = 0
        self.frames = image.ImageGrid(img, 1, 3)
        for f in self.frames:
            f.anchor_x = f.width / 2
        self.moving = False
        self.destX = 0
        self.flip = False
        if faction == "Opener":
            self.color = (150,220,150,255)
        elif faction == "Closer":
            self.color = (150,150,220,255)
        else:
            self.color = (200,200,200,255)

    def draw(self):
        offset = 17
        graphics.draw_indexed(4, gl.GL_TRIANGLES,
                      [0,1,2,0,2,3],
                      ('v2f', (self.x,self.y + offset,
                               self.x + self.width, self.y + offset,
                               self.x + self.width, self.y + self.height + offset,
                               self.x, self.y + self.height + offset)),
                              ('c4B', self.color * 4))
        self.floorLabel.draw()
        #self.sprite.draw()
        if self.flip:
            self.frames[int(self.frame) % 2].get_texture().get_transform(flip_x = True).blit(self.x + 4, self.y - 1)
        else:
            self.frames[int(self.frame) % 2].blit(self.x + 4, self.y - 1)
        if self.highlight > 0:
            graphics.draw(3, gl.GL_TRIANGLES,
                        ('v2f', (self.x + 2, self.y + self.height + 10 + offset,
                                 self.x + self.width - 2, self.y + self.height + 10 + offset,
                                 self.x + self.width/2, self.y + self.height + 2 + offset)),
                        ('c4B', (220,0,0,255)*3))
            '''graphics.draw_indexed(4, gl.GL_LINES,
                          [0,1,1,2,2,3,3,0],
                          ('v2f', (self.x - 4, self.y - 4,
                                   self.x + self.width + 4, self.y - 4,
                                   self.x + self.width + 4, self.y + self.height + 4,
                                   self.x - 4, self.y + self.height + 4)),
                          ('c4B', (255,0,0,255)*4))
            graphics.draw_indexed(4, gl.GL_LINES,
                          [0,1,1,2,2,3,3,0],
                          ('v2f', (self.x - 3, self.y - 3,
                                   self.x + self.width + 3, self.y - 3,
                                   self.x + self.width + 3, self.y + self.height + 3,
                                   self.x - 3, self.y + self.height + 3)),
                          ('c4B', (255,0,0,255)*4))
            '''

    def update(self, dt):
        if self.x < self.destX - 2:
            self.moving = True
            self.x += 25*dt
            self.flip = False
        elif self.x > self.destX + 2:
            self.moving = True
            self.x -= 25*dt
            self.flip = True
        else:
            self.moving = False
            self.frame = 0
            self.x = self.destX
        if self.moving:
            self.frame += dt * 3
#        self.sprite.image = self.frames[int(self.frame)%2]
#        self.sprite.x = self.x
#        self.sprite.y = self.y
        self.floorLabel.text = str(self.destFloor) + "\n"
        self.floorLabel.x = self.x
        self.floorLabel.y = self.y + 18
        if not self.floor == self.destFloor:
            self.waiting += dt
        '''
        if self.waiting > 16:
            self.color = (200,50,50,255)
        elif self.waiting > 12:
            self.color = (200,100,100,255)
        elif self.waiting > 6:
            self.color = (200,150,150,255)
        else:
            self.color = (200,200,200,255)
        '''
        if self.highlight >= 0:
            self.highlight -= dt
