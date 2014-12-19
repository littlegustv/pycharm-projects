from pyglet import *
from pyglet.window import key
from pyglet import font

import gameobject
import elevator
import person
import random

#setup gameobject and data

window = window.Window(360,640,caption="Lifts.")

objects = []

waitqueue = []

keys = {"up": False, "down": False}

font.add_file('VT323-Regular.ttf')

floors = [[],[],[],[],[],[],[],[],[]]

#creating game objects

building = gameobject.gameobject(80.0,50.0,200,500)
ground = gameobject.gameobject(0.0,50.0,360,2)
shaft1 = gameobject.gameobject(108.0,50.0,44,500, (230,230,230,255))
shaft2 = gameobject.gameobject(202.0,50.0,44,500, (230,230,230,255))

elev1 = elevator.elevator(110.0,50.0,40,45,(0,0,0,255))

elev2 = text.Label("OUT OF ORDER", font_name="VT323", color=(0,0,0,255), x=204, y=82, bold=True, halign='center', width=44, multiline=True)

#load data from files

df = open("defaultperson.txt", "r")
lines = df.readlines()
df.close()

nf = open("names.txt", "r")
names = nf.readlines()
nf.close()

dialogue = text.Label("", font_name="VT323", color=(255,255,255,255), x=20,y=32,width=360,multiline=True, halign='center')

person1 = person.person(0, 5, "Steve")
person2 = person.person(2, 5, "Rachel")

#add to objects list

objects.append(building)
for i in range(0, 10):
    w = gameobject.gameobject(78.0, 50.0 + i * 50 + 4, 4, 42, (255,255,255,255))
    objects.append(w)
    w2 = gameobject.gameobject(278.0, 50.0 + i * 50 + 4, 4, 42, (255,255,255,255))
    objects.append(w2)

objects.append(shaft1)
objects.append(shaft2)
objects.append(ground)

for i in range(0,9):
    f = gameobject.gameobject(80.0, 100.0 + i * 50, 200, 2, (0,0,0,255))
    objects.append(f)

floors[0].append(person1)
floors[2].append(person2)

objects.append(elev1)

def person_spawn():
    if random.randint(0,100) < 1:
        name = names[random.randint(0,len(names)-1)]
        name = name[:len(name) - 1]
        pnew = person.person(0, random.randint(0,8), name)
        floors[0].append(pnew)

@window.event
def on_draw():
    window.clear()
    for obj in objects:
        obj.draw()
    for floor in floors:
        for p in floor:
            p.draw()
    elev2.draw()
    dialogue.draw()
    
@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.UP:
        keys["down"] = False        
        keys["up"] = True
    elif symbol == key.DOWN:
        keys["up"] = False        
        keys["down"] = True

@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.UP:
        keys["up"] = False
    elif symbol == key.DOWN:
        keys["down"] = False 

def update(dt):
    if keys["up"]:
        elev1.direction = 1
    elif keys["down"]:
        elev1.direction = -1
    else:
        elev1.direction = 0
    for obj in objects:
        obj.update(dt)
    for floor in floors:
        for p in floor:
            p.y = (1 + floors.index(floor)) * 50 + 2
            destX = floor.index(p) * 20 + 90
            p.update(dt)
            if p.x < destX - 4:
                p.x += 100*dt
            elif p.x > destX + 4:
                p.x -= 100*dt
            else:
                p.x = destX
            if p.floor == elev1.floor and not p.floor == p.destFloor and len(elev1.passengers) < 3 and elev1.velY == 0:
                floor.remove(p)
                p.waiting = 0.0
                elev1.passengers.append(p)
            if p.destFloor == 0 and p.floor == 0:
                floor.remove(p)
#passengers in elevator
    for p in elev1.passengers:
        p.update(dt)
        if p.destFloor == elev1.floor:
            elev1.passengers.remove(p)
            floors[elev1.floor].append(p)
            p.waiting = 0.0
            p.floor = p.destFloor
            waitqueue.append(p)
#randomly determine when passenger on their chosen floor will want to go back down again
    if random.randint(0,100) < 1 and len(waitqueue) > 0:
        p = waitqueue.pop(random.randint(0,len(waitqueue) - 1))
        p.destFloor = 0
        #print p.destFloor
        #print waitqueue
#randomly select a person and give them some dialogue
    if random.randint(0,100) < 1 and len(waitqueue) > 0:
        p = waitqueue[random.randint(0,len(waitqueue) - 1)]
        p.highlight = 100
        line = lines[random.randint(0,len(lines) - 1)]
        line = line[:len(line) - 1]
        dialogue.text = p.name + ": '" + line +"'"
    person_spawn()

clock.schedule_interval(update, 0.01)

app.run()
