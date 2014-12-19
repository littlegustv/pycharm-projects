import re
import string

areas = ["cantina", "dwarven", "moria", "midennir", "midgaard", "schooltr"]

os = ""

for a in areas:

    fp = open(r"C:\Users\littlegustv\Downloads\rd_dev_pack\area\\"+a+".are", "r")

    contents = fp.read()

    i1 = contents.index("#MOBILES")
    i2 = contents.index("#0", i1)

    mob_contents = contents[i1:i2]

    mobiles = mob_contents.split("#")
    mobiles = mobiles[2:]

    offense = {'0':'',
               'A':'area',
               'B':'backstab',
               'C':'bash',
               'D':'berserk',
               'E':'disarm',
               'F':'dodge',
               'G':'fade',
               'H':'fast',
               'I':'kick',
               'J':'kick_dirt',
               'K':'parry',
               'L':'rescue',
               'M':'tail',
               'N':'trip',
               'O':'crush',
               'P':'',
               'Q':'assist_align',
               'R':'assist_race',
               'S':'assist_players',
               'T':'assist_guard',
               'U':'assist_vnum',
               'V':'',
               'W':'',
               'X':'',
               'Y':'',
               'Z':'',
               'a':''}

    irv =  {'0':'',
                  'A':'summon',
               'B':'charm',
               'C':'magic',
               'D':'weapon',
               'E':'bash',
               'F':'piercing',
               'G':'disease',
               'H':'fire',
               'I':'cold',
               'J':'lightning',
               'K':'acid',
               'L':'poison',
               'M':'negative',
               'N':'holy',
               'O':'energy',
               'P':'mental',
               'Q':'disease',
               'R':'drowning',
               'S':'light',
               'T':'',
               'U':'',
               'V':'',
               'W':'',
               'X':'',
               'Y':'silver',
               'Z':'iron',
               'a':'rain',
                'b':'vorpal'}

    action = {'0':'',
              'A':'npc',
               'B':'sentinel',
               'C':'scavenger',
               'D':'',
               'E':'',
               'F':'aggressive',
               'G':'stay_area',
               'H':'wimpy',
               'I':'pet',
               'J':'train',
               'K':'practice',
               'L':'',
               'M':'',
               'N':'',
               'O':'undead',
               'P':'',
               'Q':'cleric',
               'R':'mage',
               'S':'thief',
               'T':'warrior',
               'U':'no_align',
               'V':'no_purge',
               'W':'',
               'X':'',
               'Y':'',
               'Z':'',
               'a':'healer',
              'b':'skill_train',
              'c':'',
              'd':'changer',
              'e':'banker'
              }
    affects =  {'0':'',
                'A':'',
               'B':'invisible',
               'C':'sanctuary',
               'D':'detect_invis',
               'E':'detect_magic',
               'F':'detect_hidden',
               'G':'water_breathing',
               'H':'berserk',
               'I':'faerie_fire',
               'J':'infrared',
               'K':'',
               'L':'grandeur',
               'M':'',
               'N':'prot_evil',
               'O':'prot_good',
               'P':'sneak',
               'Q':'hide',
               'R':'',
               'S':'',
               'T':'flying',
               'U':'',
               'V':'haste',
               'W':'calm',
               'X':'',
               'Y':'water_walk',
               'Z':'dark_vision',
               'a':'minimation',
                'b':'',
                'c':'',
                'd':'slow'}

    parts = {'0':'',
            'A':'head',
             'B':'arms',
             'C':'legs',
             'D':'heart',
             'E':'brains',
             'F':'guts',
             'G':'hands',
             'H':'feet',
             'I':'fingers',
             'J':'ears',
             'K':'eyes',
             'L':'long_tongue',
             'M':'eyestalks',
             'N':'tentacles',
             'O':'fins',
             'P':'wings',
             'Q':'tail',
             'R':'',
             'S':'',
             'T':'',
             'U':'claws',
             'V':'fangs',
             'W':'horns',
             'X':'scales',
             'Y':'none'
        }

    for mobile in mobiles:

        n1 = mobile.index('~')
        n2 = mobile.index('~', n1 + 1)
        n3 = mobile.index('~', n2 + 1)
        n4 = mobile.index('~', n3 + 1)
        n5 = mobile.index('~', n4 + 1)
        n6 = mobile.index('~', n5 + 1)
        
        os += "--- START MOBILE ---\n"
        vnum = mobile[:n1].split('\n')[0]
        os += "vnum:^:" + mobile[:n1].split('\n')[0] + "\n"
        keywords = mobile[:n1].split('\n')[1]
        os += "keywords:^:" + keywords + "\n"
        name =  mobile[n1 + 1:n2].strip('\n')
        os += "name:^:" + name + "\n"
        os += "desc:^:" + mobile[n2 + 1:n3].strip('\n') + "\n"
        os += "longdesc:^:" + mobile[n3 + 1:n4].strip('\n') + "\n"
        os += "race:^:" + mobile[n4 + 1:n5].strip('\n') + "\n"

        data = mobile[n5+2:n6].split('\n')
        #print (data)
        misc0 = data[0].split(' ')
        combat = data[1].split(' ')
        ac = data[2]
        combattags = data[3].split(' ')
        misc1 = data[4].split(' ')
        misc2 = data[5].split(' ')

        act = ""
        for a in list(misc0[0]):
            try:
                if action[a] is not '':
                    act += action[a] + " "
                elif a is not '0':
                    print("Action:", vnum, keywords, a)
            except KeyError:
                print("Action:", vnum, keywords, a)
        aff = ""
        for a in list(misc0[1]):
            try:
                if affects[a] is not '':
                    aff += affects[a] + " "
                elif a is not '0':
                    print("Affect:",vnum, keywords, a)
            except KeyError:
                print("Affect:", vnum, keywords, a)
        align = misc0[2]

        pos = misc1[0]
        wealth = misc1[3]
        size = misc2[2]

        os += "position:^:" + pos + "\n"
        os += "wealth:^:(*int)" + wealth + "\n"
        os += "size:^:" + size + "\n"
        os += "align:^:(*int)" + align + "\n"
        
        par = ""
        for a in list(misc2[1]):
            try:
                if parts[a] is not '':
                    par += parts[a] + " "
                elif a is not '0':
                    print("Parts:",vnum, keywords, a)
            except KeyError:
                print("Parts:",vnum, keywords, a)

        off = ""
        for a in  list(combattags[0]):
            try:
                if offense[a] is not '':
                    off += offense[a] + " "
                elif a is not '0':
                    print("Offense:",vnum, keywords, a)
            except KeyError:
                print("Offense:",vnum, keywords, a)
                
        imm = ""
        for a in  list(combattags[1]):
            try:
                if irv[a] is not '':
                    imm += irv[a] + " "
                elif a is not '0':
                    print("Immune:",vnum, keywords, a)
            except KeyError:
                print("Immune:",vnum, keywords, a)

        res = ""
        for a in  list(combattags[2]):
            try:
                if irv[a] is not '':
                    res += irv[a] + " "
                elif a is not '0':
                    print("Resist:",vnum, keywords, a)
            except KeyError:
                print("Resist:",vnum, keywords, a)
                
        vul = ""
        for a in  list(combattags[3]):
            try:
                if irv[a] is not '':
                    vul += irv[a] + " "
                elif a is not '0':
                    print("Vulnerable:",vnum, keywords, a)
            except KeyError:
                print("Vulnerable:",vnum, keywords, a)


        level = combat[0]
        hit = combat[1]
        hp = combat[2]
        mana = combat[3]
        damage = combat[4]
        noun = combat[5]

        os += "level:^:(*int)" + level + "\n"
        os += "max_hp:^:" + hp + "\n"
        os += "hit:^:(*int)" + hit + "\n"
        os += "dam:^:" + damage + "\n"
        os += "noun:^:" + noun + "\n"
        os += "ac:^:" + ac +"\n"
        os += "affects:^:" + aff + "\n"
        os += "actions:^:" + act + "\n"
        os += "offense:^:" + off + "\n"
        os += "vulnerable:^:" + vul + "\n"
        os += "resist:^:" + res + "\n"
        os += "immune:^:" + imm + "\n"
        os += "parts:^:" + par + "\n"
        os += "--- END MOBILE ---\n"

    fp.close()

print (os)

#fw = open(r"C:\Users\littlegustv\PycharmProjects\rdu\data\mobiles.dat", "w")

#fw.write(os)
#fw.close()
