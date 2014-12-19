from pyglet import *
from pyglet.window import key
from pyglet.window import mouse
from pyglet import font

import gameobject
import floor
import elevator
import person
import button
import random
import resources

#setup gameobject and data

window = window.Window(360,640,caption="Lifts.")

gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

objects = []

waitqueue = []

keys = {"up": False, "down": False}

font.add_file('VT323-Regular.ttf')
font.add_file('TulpenOne-Regular.ttf')

floors = []

for i in range(10):
    floors.append(floor.floor(i))

waitTime = {"Opener": 0.0, "Closer": 0.0, "Neutral": 0.0}

endings = {"Opener": u"The Elder Ones are unleashed and the world enters into a new DARK AGE.  Or does it?",
           "Closer": u"The rift is sealed, until another day.  Until then, the everyday tedium, misery and march towards death continues.",
           "Neutral": u"With much regret, but for the greater good, the advance of Machine intelligence is destroyed to protect the Human race.\n\n\u03EE"
           }

avgWaitTime = 0.0
avgNumber = 0

success = {"Opener": 0.0, "Closer": 0.0, "Neutral": 0.0}

gamestate = "Menu"

menuImage = []

#creating game objects

#GAME MENU TEXT

menuLabel = text.Label("The Red Tower\n", font_name="Tulpen One", font_size=48, color=(120,0,0,255),x=0, y=window.height - 80, halign='center', width=window.width, height=12, multiline=True)
#menuLabel.set_style('align', 'center')

endLabel = text.Label("ENDING\n", font_name="Tulpen One", font_size=36, color=(255,255,255,255), width = window.width - 40, multiline=True, halign='center', x = 20, y = window.height / 2 + 100)

building = gameobject.gameobject(80.0,46.0,200,506, (255,255,255,255))
ground = gameobject.gameobject(0.0,46.0,360,2)
shaft1 = gameobject.gameobject(108.0,50.0,44,500, (230,230,230,255))
shaft2 = gameobject.gameobject(202.0,50.0,44,500, (230,230,230,255))

elev1 = elevator.elevator(110.0,50.0,40,45,(92,66,36,255))

elev2 = text.Label("OUT OF\nSERVICE\n", font_name="Tulpen One", font_size=14, color=(0,0,0,255), x=200, y=82, bold=True, halign='center', width=44, multiline=True)

floorsLabel = text.Label("9\n8\n7\n6\n5\n4\n3\n2\n1\nM", font_name="Tulpen One", font_size=34, color=(255,255,255,255), x=50, y=515, halign='center', width=20, multiline=True)

#load data from files

df = open("defaultperson.txt", "r")
lines = df.readlines()
df.close()

nf = open("names.txt", "r")
names = nf.readlines()
nf.close()

dialogue = text.Label("", font_name="Tulpen One", font_size=20, color=(255,255,255,255), x=0,y=24,width=360,multiline=True, halign='center')

#alarmButton = text.Label("ALARM", font_name="VT323", color=(255,255,255,255), x=300,y=500,halign='center')

person1 = person.person(0, 5,  resources.person_image, "Steve")
person2 = person.person(2, 5,  resources.person_image, "Rachel")

talking = ""

#add to objects list

#objects.append(building)

for i in range(0, 10):
    w = gameobject.gameobject(78.0, 50.0 + i * 50 + 4, 4, 42, (255,255,255,255))
    menuImage.append(w)
    w2 = gameobject.gameobject(278.0, 50.0 + i * 50 + 4, 4, 42, (255,255,255,255))
    menuImage.append(w2)

for i in range(0, 10):
    for j in range(0,8):
        cvar = (i * 10 + j * 10) / 2
        w = gameobject.gameobject(80 + 25 * j + 4, 50 + i * 50 + 4, 17, 42, (cvar,0,0,255))
        menuImage.append(w)
    

objects.append(shaft1)
objects.append(shaft2)
objects.append(ground)
menuImage.append(ground)

for i in range(0,9):
    f = gameobject.gameobject(80.0, 100.0 + i * 50, 200, 2, (0,0,0,255))
    objects.append(f)

floors[0].append(person1)
floors[2].append(person2)

objects.append(elev1)

def elevator_alarm():
    global elev1
    if elev1.floor == 0:
        return
    elif elev1.y % 50 < 25:
        elev1.velY = 0
        elev1.y = elev1.y - elev1.y % 50
        elev1.floor = int(elev1.y / 50) - 1
    elif elev1.y % 50 >= 25:
        elev1.velY = 0
        elev1.y = (elev1.y - elev1.y % 50) + 50
        elev1.floor = int(elev1.y / 50) - 1
    for p in elev1.passengers:
        p.destFloor = elev1.floor
#        elev1.passengers.remove(p)
#        floors[elev1.floor].append(p)
#        waitTime[p.faction] += p.waiting
#        p.waiting = 0.0
#        p.floor = elev1.floor
#        waitqueue.append(p)


def start_game():
    global gamestate
    gamestate = "Game"

menuButton = button.button(window.width / 2 - 30, window.height/2 - 126, "PLAY", start_game)

alarmButton = button.button(296,500,"ALARM",elevator_alarm)
objects.append(alarmButton)

def person_spawn():
    if random.randint(0,100) < 1:
        name = names[random.randint(0,len(names)-1)]
        name = name[:len(name) - 1]
        fc = random.randint(0,6)
        if fc <= 1:
            faction = "Opener"
        elif fc <= 3:
            faction = "Closer"
        else:
            faction = "Neutral"
        pnew = person.person(0, random.randint(1,9), resources.person_image, name, faction)
        floors[0].append(pnew)

@window.event
def on_draw():
    gl.glClearColor(0.01,0,0.07,1)
    window.clear()
    if gamestate == "Menu":
        building.draw()
        for e in menuImage:
            e.draw()
        menuLabel.color = (255,255,255,255)
        menuLabel.draw()
        menuButton.draw()
#        floorsLabel.draw()
    elif gamestate == "Game":    
        for floor in floors:
            floor.draw()
        for obj in objects:
            obj.draw()
        elev2.draw()
        for floor in floors:
            for p in floor.persons:
                p.draw()
        dialogue.draw()
        floorsLabel.draw()
    elif gamestate == "Ending":
        graphics.draw_indexed(4, gl.GL_TRIANGLES,
                              [0,1,2,0,2,3],
                              ('v2f', (10,10,
                                       10, window.height - 10,
                                       window.width - 10, window.height - 10,
                                       window.width - 10, 10)),
                              ('c4B', 4*(225,225,225,255)))
        graphics.draw_indexed(4, gl.GL_TRIANGLES,
                              [0,1,2,0,2,3],
                              ('v2f', (15,15,
                                       15, window.height - 15,
                                       window.width - 15, window.height - 15,
                                       window.width - 15, 15)),
                              ('c4B', 4*(0,0,0,255)))
        endLabel.draw()
        
@window.event
def on_mouse_press(x,y,button,modifiers):
    if gamestate == "Game":
        if button == mouse.LEFT:
            if x > alarmButton.x and x < alarmButton.x + 40 and y > alarmButton.y and y < alarmButton.y + 40:
                alarmButton.press()
    elif gamestate == "Menu":
        if button == mouse.LEFT:
            if x > menuButton.x and x < menuButton.x + 40 and y > menuButton.y and y < menuButton.y + 40:
                menuButton.press()
            
    
@window.event
def on_key_press(symbol, modifiers):
    global gamestate
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
    global talking, gamestate, avgNumber, avgWaitTime
    #print "Openers:" + str(success["Opener"])
    #print "Closers:" + str(success["Closer"])
    #check waittimes, to make sure it hasn't been too slow
    for faction,waiting in waitTime.iteritems():
        #de-increment the waittime - needs to be tweaked
        waiting -= dt
        if waiting >= 1000:
            endLabel.text = endings[faction]
            gamestate = "Ending"
            break
    if gamestate == "Game":
#elevator movement
        if keys["up"]:
            elev1.direction = 1
        elif keys["down"]:
            elev1.direction = -1
        else:
            elev1.direction = 0
        for obj in objects:
            obj.update(dt)
        for floor in floors:
            floor.update(dt)
            for p in floor.persons:
                p.y = (1 + floors.index(floor)) * 50 + 2
#person gets ON the elevator from their floor
                if p.floor == elev1.floor and not p.floor == p.destFloor and len(elev1.passengers) < 3 and elev1.velY == 0:
                    floor.remove(p)
                    waitTime[p.faction] += p.waiting
                    avgWaitTime = (p.waiting + avgWaitTime * avgNumber) / (avgNumber + 1)
                    avgNumber += 1
                    success[p.faction] += p.waiting / avgWaitTime
                    p.waiting = 0.0
                    elev1.passengers.append(p) 
                elif p.destFloor == 0 and p.floor == 0:                  
                    if p.x > window.width or p.x < 0:
                        floor.remove(p)
                        if p is talking:
                            talking = ""
                        if p in waitqueue:
                            waitqueue.remove(p)
                    elif p.x > window.width / 2:
                        p.destX = window.width + 100
                    else:
                        p.destX = -100
                else:
                    p.destX = floor.persons.index(p) * 20 + 90
                p.update(dt)

#passengers in elevator
        for p in elev1.passengers:
            p.update(dt)
#person gets OFF the elevator, to their floor
            if p.destFloor == elev1.floor:
                elev1.passengers.remove(p)
                floors[elev1.floor].append(p)
                waitTime[p.faction] += p.waiting
                avgWaitTime = (p.waiting + avgWaitTime * avgNumber) / (avgNumber + 1)
                avgNumber += 1
                success[p.faction] += p.waiting / avgWaitTime
                floors[elev1.floor].factionate(p.faction, p.waiting / avgWaitTime)
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
        if random.randint(0,100) < 10 and len(waitqueue) > 0 and talking == "":
            talking = waitqueue[random.randint(0,len(waitqueue) - 1)]
            talking.highlight = 6.0
            line = lines[random.randint(0,len(lines) - 1)]
            line = line[:len(line) - 1]
            dialogue.text = talking.name + ": '" + line +"'"
        try:
            if talking.highlight <= 0:
                talking = ""
                dialogue.text = ""
        except:
            pass
        person_spawn()

clock.schedule_interval(update, 0.01)

app.run()
