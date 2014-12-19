import gameobject
from pyglet import graphics, gl

class floor(gameobject.gameobject):

    def __init__(self, floor):
        self.floor = floor
        self.x = 80
        self.y = 50 + floor * 50
        self.height = 50
        self.width = 200
        self.color = (255,255,255,255)
        self.persons = []
        self.faction = 0.0

    def draw(self):
        graphics.draw_indexed(4, gl.GL_TRIANGLES,
                      [0,1,2,0,2,3],
                      ('v2f', (self.x,self.y,
                               self.x + self.width, self.y,
                               self.x + self.width, self.y + self.height,
                               self.x, self.y + self.height)),
                              ('c4B', self.color * 4))
        graphics.draw_indexed(4, gl.GL_TRIANGLES,
                      [0,1,2,0,2,3],
                      ('v2f', (self.x - 2,self.y + 6,
                               self.x, self.y + 6,
                               self.x, self.y + self.height - 6,
                               self.x - 2, self.y + self.height - 6)),
                              ('c4B', self.color * 4))
        graphics.draw_indexed(4, gl.GL_TRIANGLES,
                      [0,1,2,0,2,3],
                      ('v2f', (self.x + self.width, self.y + 6,
                               self.x + self.width + 2, self.y + 6,
                               self.x + self.width + 2, self.y + self.height - 6,
                               self.x + self.width, self.y + self.height - 6)),
                              ('c4B', self.color * 4))

    def update(self, dt):
        cvar = min(int(abs(self.faction * 40)),100)
        if self.faction > 0:
            self.color = (150 - cvar, 150,150 - cvar,255)
        elif self.faction < 0:
            self.color = (150 - cvar,150 - cvar, 150, 255)
        else:
            self.color = (150,150,150,255)

    def append(self, obj):
        self.persons.append(obj)

    def remove(self, obj):
        return self.persons.remove(obj)

    def factionate(self, faction, amount):
        print self.faction
        if self.floor == 0:
            return
        if faction == "Opener":
            self.faction += amount
        elif faction == "Closer":
            self.faction -= amount
