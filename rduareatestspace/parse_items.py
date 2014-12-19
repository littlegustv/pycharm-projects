import re
import string

areas = ["cantina", "dwarven", "moria", "midennir", "midgaard", "schooltr"]

os = ""

for a in areas:

    fp = open(r"C:\Users\littlegustv\Downloads\rd_dev_pack\area\\"+a+".are", "r")

    contents = fp.read()

    i1 = contents.index("#OBJECTS")
    i2 = contents.index("#0", i1 + 1)

    item_contents = contents[i1:i2]

    items = item_contents.split("#")
    items = items[2:]

    m_attr = {'0':'none',
              'A':'glow',
              'B':'hum',
              'C':'dark',
              'D':'UNKNOWN',
              'E':'evil',
              'F':'invis',
              'G':'magic',
              'H':'nodrop',
              'I':'bless',
              'J':'antigood',
              'K':'antievil',
              'L':'antineutral',
              'M':'noremove',
              'N':'UNKNOWN',
              'O':'nopurge',
              'P':'rotdeath',
              'Q':'UNKNOWN',
              'R':'UNKNOWN',
              'S':'nonmetal',
              'T':'nolocate',
              'U':'meltdrop',
              'V':'UNKNOWN',
              'W':'sellextract',
              'X':'UNKNOWN',
              'Y':'burnproof',
              'Z':'nouncurse',
              'a':'warrior',
              'b':'mage',
              'c':'thief',
              'd':'cleric',
              'e':'soundproof'}

    #ce -> vampiric vorpal
    m_flags = {'0':'none',
               'A':'flaming',
               'B':'frost',
               'C':'vampiric',
               'D':'sharp',
               'E':'vorpal',
               'F':'twohanded',
               'G':'shocking',
               'H':'poison',
               'I':'dragonslaying',
               'J':'dull',
               'K':'blunt',
               'L':'corrosive',
               'M':'flooding',
               'N':'infected',
               'O':'UNKNOWN',
               'P':'souldrain',
               'Q':'holy',
               'R':'unholy',
               'S':'polar',
               'T':'phasing',
               'U':'antimagic',
               'V':'entropic',
               'W':'psionic',
               'X':'demonic',
               'Y':'intelligent'}

    m_worn = {'0':-1,
              'A':'take',
              'B':3,
              'C':7,
              'D':9,
              'E':5,
              'F':6,
              'G':2,
              'H':4,
              'I':0,
              'J':8,
              'K':1,
              'L':10,
              'M':11,
              'N':15,
              'O':13,
              'P':'ignore',
              'Q':12,
              'R':'ignore',
              'T':'ignore',
              'Y':'ignore',
              'Z':'ignore',
              'c':'newbie',
              }

    m_stats = ['',          #0
               'str',
               'dex',
               'wis',
               'int',
               'con',       #5
               'sex',
               '',
               '',
               'age',
               '',          #10
               '',
               'mp',
               'hp',
               'mv',
               '',          #15
               '',
               'ac',
               'hit',
               'dam',
               'saves',     #20, but ALSO 23 and 24 (spel and breath saves - just put them all here.)
               '',
               '',
               'saves',
               'saves',
               '',          #25
               'damred',
               'magdam',
               'maxstr',
               'maxdex',
               'maxcon',    #30
               'maxint',
               'maxwis',
               'atkspd']

    for item in items:

        n1 = item.index('~')
        n2 = item.index('~', n1 + 1)
        n3 = item.index('~', n2 + 1)
        n4 = item.index('~', n3 + 1)
        
        vnum = item[:n1].split('\n')[0]
        keywords = item[:n1].split('\n')[1]
        name = item[n1 + 1:n2].strip('\n')
        desc = item[n2 + 1:n3].strip('\n')
        material = item[n3 + 1:n4].strip('\n')

        data = item[n4+2:].split('\n')
        #print (data)

        itemtype = data[0].split(' ')[0]
        #if itemtype in ["container", "portal", "throwing", "fountain", "jewelry"]:
        #    continue

        attributes = []
        for a in list(data[0].split(' ')[1]):
            try:
                if m_attr[a] is not "UNKNOWN":
                    attributes.append(m_attr[a])
                else:
                    print("FOUND UNKNOWN", name,keywords,a)
            except:
                print("KEY NOT FOUND", name,keywords, a)

        worn = ""
        for w in list(data[0].split(' ')[2]):
            try:
                if m_worn[w] not in ['ignore', 'take']:
                    worn += str(m_worn[w]) + " "
                elif m_worn[w] is 'none':
                    worn = "-1 "
            except KeyError:
                print("WORN KEYERROR:",keywords,vnum,w)

        buffer = ""

        if itemtype == "weapon":
            w_data = data[1].split(' ')
            buffer += "weapon_type:^:" + w_data[0] + "\n"
            buffer += "dice:^:" + w_data[1] + "\n"
            buffer += "sides:^:" + w_data[2] + "\n"
            buffer += "noun:^:" + w_data[3] + "\n"
            flags = ""
            for f in list(w_data[4]):
                flags += m_flags[f] + " "
            buffer += "flag:^:" + flags + "\n"
        elif itemtype == "armor":
            a_data = data[1]
            buffer += "armor_class:^:" + a_data + "\n"
            
        os += "--- START " + itemtype.upper() + " ---\n"
        
        os += "vnum:^:" + vnum + "\n"
        os += "keywords:^:" + keywords + "\n"
        os += "name:^:" + name + "\n"
        os += "desc:^:" + desc + "\n"
        os += "material:^:" + material + "\n"
        os += buffer

        last = 2
        for j in range(2,len(data)):
            if data[j][:1] == 'A' or data[j][:1] == 'E':
                last = j - 1
                break

        misc = data[last].split(' ')
        os += "level:^:(*int)" + misc[0] + "\n"
        os += "weight:^:(*int)" + misc[1] + "\n"
        os += "worth:^:(*int)" + misc[2] + "\n"
        os += "wear_loc:^:" + str(worn) + "\n"

        #ADD STAT MODIFIERS (A), READ TARGETS (E)
        stats = {}
        read = ""
        for j in range(last, len(data)):
            if data[j] == 'A':
                j += 1
                key = data[j].split(' ')[0]
                value = data[j].split(' ')[1]
                if m_stats[int(key)] is not "":
                    try:
                        stats[m_stats[int(key)]] += int(value)
                    except:
                        stats[m_stats[int(key)]] = int(value)
            #"READ" -> (E) tags:
            if data[j] == 'E':
                j += 1
                read += "read:^:" + data[j][:len(data[j]) - 1] + ":^:"
                j += 1
                while '~' not in data[j] and j < len(data) - 1:
                    #print("HERE:",data[j],j,len(data))
                    read += data[j].strip('\n') + "<br>"
                    j += 1
                read += "\n"

        for k,v in stats.items():
            os += k + ":^:(*int)" + str(v) + "\n"
        os += read

    #    print (itemtype)
        combat = data[1].split(' ')
        
        os += "--- END ITEM ---\n"

    fp.close()  

print (os)

fw = open(r"C:\Users\littlegustv\PycharmProjects\rdu\data\items.dat", "w")
#
fw.write(os)
fw.close()

