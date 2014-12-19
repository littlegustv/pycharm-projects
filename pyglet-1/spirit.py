__author__ = 'littlegustv'

import player
import pyglet

class Spirit(player.Player):

    type = "Spirit"
    gravity = 600
    speed = 20
    jumpstrength = 300

    #right = True
    right = True
    frames = []
    frame = 0
    animation = 2
    velX = 15
    velY = 0
    jump = False

    rank = 2

