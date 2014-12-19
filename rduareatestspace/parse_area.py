import re
import string

files = ['cantina','dwarven','moria','midennir','midgaard','schooltr']

for fn in files:

    fp = open(r'C:\Users\littlegustv\Downloads\rd_dev_pack\area\\'+fn+'.are', "r")

    contents = fp.read()

    i1 = contents.index("#ROOMS")
    i2 = contents.index("#0", i1)

    area_contents = contents[i1:i2]

    rooms = area_contents.split("#")
    rooms = rooms[2:]

    os = ""

    for room in rooms:

        n1 = room.index('~')
        n2 = room.index('~', n1 + 1)

        os += "--- START ROOM ---\n"
        vnum = room[:n1].split('\n')[0]
        os += "vnum:^:" + room[:n1].split('\n')[0] + "\n"
        os += "name:^:" + room[:n1].split('\n')[1] + "\n"
        os += "desc:^:" + room[n1 + 1:n2].strip('\n') + "\n"
        data = room[n2:]

        rx = re.compile("(D[0-9])")
        data = re.split(rx, data)
        
        for i in range(0, len(data)):
            if data[i][:1] == "D" and len(data[i]) == 2:
                ex_dir = data[i][1:]
                i += 1
                info = data[i].split('\n')[1:]
                if info[0] != "~":
                    info.remove(info[1])
                #print(info)
                ex_desc = info[0].strip('~')
                ex_door = info[1].strip('~')
                ex_data = info[2].split(' ')
                print (vnum, ex_data)
                ex_locked = ex_data[0]
                ex_key = ex_data[1]
                ex_dest = ex_data[2]

                os += "exit:^:" + ex_dir + ":^:" + ex_dest + "\n"
                
        os += "---  END ROOM  ---\n"


    i1 = contents.index("#RESETS")
    i2 = contents.index("#", i1 + 1)

    os += "---START RESETS---\n"

    reset_contents = contents[i1:i2]

    resets = reset_contents.split('\n')

    for r in resets:
        mr = r.split(' ')
        if mr[0] == "M":
            os += "mobile:^:" + mr[2] + " " + mr[4] + "\n"
        elif mr[0] == "G":
            os += "carry:^:" + mr[2] + "\n"
        elif mr[0] == "E":
            os += "wield:^:" + mr[2] + "\n"

    os += "--- END RESETS ---\n"

    fp.close()

    fw = open(r"C:\Users\littlegustv\PycharmProjects\rdu\data\areas\\"+fn+".are", "w")

    fw.write(os)
    fw.close()
