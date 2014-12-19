"""

TODO:

- add startx,y for subghost
- add "behavior" function that can be passed to hazard init() function


"""
from __future__ import division

from pyglet.window import key
from json_map import Map
import math
import pyglet
import resources
import solid
import subghost
import player
import hazard
import jumpthru
import spirit
import shader
from pyglet.gl import *
from math import pi, sin, cos, sqrt
from euclid import *

window = pyglet.window.Window(
    width=480,
    height=360,
    caption="Where The Light Breaks."
)

window.set_mouse_visible(False)
pyglet.gl.glClearColor(0.4, 0.4, 1, 1)

v_shader = open("./resources/shader/v2.sh", "r")
f_shader = open("./resources/shader/f2.sh", "r")

shader = shader.Shader([v_shader.read()], [f_shader.read()])

#pyglet.gl.glEnable(GL_BLEND)
#pyglet.gl.glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

player = player.Player(
    pyglet.sprite.Sprite(img = resources.player_frames[0], x=100, y=400, usage="dynamic"))
player.frames = resources.player_frames

game_objects = []

tile_batch = pyglet.graphics.Batch()

# load the map
fd = pyglet.resource.file("level1.json")
m = Map.load_json(fd)

# set the viewport to the window dimensions
m.set_viewport(0, 0, 64 * 32, 16 * 32)

m_height = m.p_height
m_width = m.p_width

for obj in m.objectgroups["Objects"].get_by_type("Wall"):
    game_objects.append(solid.Solid(obj.get(u'x') +  obj.get(u'width') / 2, m_height - obj.get(u'y') - obj.get(u'height') / 2, obj.get(u'height'), obj.get(u'width')))

for obj in m.objectgroups["Objects"].get_by_type("JumpThru"):
    game_objects.append(jumpthru.JumpThru(obj.get(u'x') +  obj.get(u'width') / 2, m_height - obj.get(u'y') - obj.get(u'height') / 2, obj.get(u'height'), obj.get(u'width')))

for obj in m.objectgroups["Objects"].get_by_type("Subghost"):
    sg = subghost.SubGhost(pyglet.sprite.Sprite(img = resources.subghost_frames[0], x=obj.get(u'x'), y=m_height - obj.get(u'y')))
    sg.frames = resources.subghost_frames
    game_objects.append(sg)

"""
sg = subghost.SubGhost(pyglet.sprite.Sprite(img = resources.subghost_frames[0], x=400, y=200))
sg.frames = resources.subghost_frames
game_objects.append(sg)
"""

for obj in m.objectgroups["Objects"].get_by_type("Hazard"):
    hz = hazard.Hazard(pyglet.sprite.Sprite(img = resources.salamander_frames[0], x=obj.get(u'x'), y=m_height - obj.get(u'y')))
    hz.frames = resources.salamander_frames
    game_objects.append(hz)

"""
sg = subghost.SubGhost(pyglet.sprite.Sprite(img = resources.subghost_frames[0], x=200, y=400))
sg.frames = resources.subghost_frames
game_objects.append(sg)
"""
#game_objects.append(subghost.SubGhost(pyglet.sprite.Sprite(img = resources.subghost_image, x=100, y=600)))

#game_objects.append(speech.Speech("Hi"))

sp = spirit.Spirit(pyglet.sprite.Sprite(img = resources.sprite_frames[0], x=200, y=m_height / 2 ))
sp.frames = resources.sprite_frames
game_objects.append(sp)


game_objects.append(player)

label = pyglet.text.Label('',
                          font_name='Times New Roman',
                          font_size=12,
                          x=player.x, y=player.y + 24)

#game_objects.append(label)

def on_resize(width, height):

    pyglet.gl.glViewport(0,0,width,height)

    pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
    pyglet.gl.glLoadIdentity()

    w = window._width/2
    h = window._height/2

    pyglet.gl.glOrtho(-w,w,-h,h,-1.0,1.0)

@window.event
def on_draw():
    window.clear()

    pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
    pyglet.gl.glLoadIdentity()

    #   Camera offset; doesn't scroll past the edges of the layout.     #

    tx = min(0, max(window.width - m_width, -player.x + window.width / 2))
    ty = min(0, max(window.height - m_height, -player.y + window.height / 2))

    #pyglet.gl.glScalef(2,2,0)
    pyglet.gl.glTranslatef(tx, ty, 0)

    shader.bind()
    m.draw()
    label.draw()
    pyglet.gl.glFlush()

    for i in range(len(game_objects)):
        pyglet.gl.glPushMatrix()
        game_objects[i].draw()
#        pyglet.graphics.draw(1,pyglet.gl.GL_POINTS, ('v2i', (int(game_objects[i].x), int(game_objects[i].y))))
#        pyglet.graphics.draw(1,pyglet.gl.GL_POINTS, ('v2i', (int(game_objects[i].x + int(game_objects[i].width / 2)), int(game_objects[i].y + int(game_objects[i].height / 2)))))
        pyglet.gl.glTranslatef(game_objects[i].x, game_objects[i].y, 0)
        pyglet.gl.glPopMatrix()
    shader.unbind()

@window.event
def on_key_press(symbol, modifiers):
    global right, left
    if symbol == key.LEFT:
        player.left = True
    elif symbol == key.RIGHT:
        player.right = True
    elif symbol == key.SPACE:
        player.velX = 0

    if symbol == key.UP:
        player.do_jump()

@window.event
def on_key_release(symbol, modifiers):
    global right, left
    if symbol == key.LEFT:
        player.left = False
    elif symbol == key.RIGHT:
        player.right = False

def distance(point1=(0,0), point2=(0,0)):
    return math.sqrt(
        (point1[0] - point2[0]) ** 2 +
        (point1[1] - point2[1]) ** 2
    )

    """
    collision_distance = (self.image.width / 2 + other.image.width / 2) / 2
    actual_distance = distance(self.position, other.position)
    return (actual_distance <= collision_distance)
"""

def update(dt):

    #cleanup
    game_objects[:] = [value for value in game_objects if not value.cleanup]

    #update
    for i in range(len(game_objects)):
        game_objects[i].update(dt)

    #collisions
    for i in range(len(game_objects)):
        for j in range(len(game_objects)):
            if i == j:
                continue
            else:
                game_objects[i].handle_collision(game_objects[j])

    for obj in game_objects:
        obj.move(dt)

    label.x = player.x
    label.y = player.y
#resources.music.play()
# Define a simple function to create ctypes arrays of floats:
def vec(*args):
    return (GLfloat * len(args))(*args)

def setup () :
    # One-time GL setup
    global light0pos
    global light1pos
    global togglewire

    light0pos = [100.0,   100.0, 100.0, 1.0] # positional light !
    light1pos = [-20.0, -20.0, 20.0, 1.0] # infinitely away light !

    #glClearColor(1, 1, 1, 1)
    glColor4f(1.0, 0.0, 0.0, 0.5 )
    #glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    # Uncomment this line for a wireframe view
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Simple light setup.  On Windows GL_LIGHT0 is enabled by default,
    # but this is not the case on Linux or Mac, so remember to always
    # include it.
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    glLightfv(GL_LIGHT0, GL_POSITION, vec(*light0pos))
    glLightfv(GL_LIGHT0, GL_AMBIENT, vec(0.3, 0.3, 0.3, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(0.9, 0.9, 0.9, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, vec(1.0, 1.0, 1.0, 1.0))

    glLightfv(GL_LIGHT1, GL_POSITION, vec(*light1pos))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(.6, .6, .6, 1.0))
    glLightfv(GL_LIGHT1, GL_SPECULAR, vec(1.0, 1.0, 1.0, 1.0))

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(0.4, 0.4, 0.3, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(1, 1, 1, 1))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50)

setup()

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/120)
    pyglet.app.run()