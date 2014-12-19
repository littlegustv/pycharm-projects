__author__ = 'littlegustv'

import pyglet

def center_image(image):
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2

pyglet.resource.path = ['./resources']
pyglet.resource.reindex()

#images

player_image = pyglet.resource.image("ghost1.png")
subghost_image = pyglet.resource.image("smallghost1.png")
salamander_image = pyglet.resource.image("salamander.png")
sprite_image = pyglet.resource.image("sprite.png")

salamander_frames = pyglet.image.ImageGrid(salamander_image, 2, 2)
subghost_frames = pyglet.image.ImageGrid(subghost_image, 2, 2)
player_frames = pyglet.image.ImageGrid(player_image, 3, 2)
sprite_frames = pyglet.image.ImageGrid(sprite_image, 3, 2)

tile_image = pyglet.resource.image("tile2.png")

for i in range(len(player_frames)):
    center_image(player_frames[i])
for i in range(len(sprite_frames)):
    center_image(sprite_frames[i])
center_image(tile_image)
for i in range(len(subghost_frames)):
    center_image(subghost_frames[i])
for i in range(len(salamander_frames)):
    center_image(salamander_frames[i])

music = pyglet.resource.media('music.mp3')

pyglet.font.add_file("./resources/TulpenOne-Regular.ttf")
vt323 = pyglet.font.load("TulpenOne-Regular")