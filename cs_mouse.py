import struct
from cs_aws_mqtt import notifyMsgReceived
from cs_global import mensajes,rectangulos
from cs_display import drawScreen

def mouse(inicio):
    f = open( "/dev/input/mice", "rb" );
    X_fix = 0
    Y_fix = 0
    #f = open( "/dev/input/event1", "rb" );
    # Open the file in the read-binary mode
    while 1:
        data = f.read(3)  # Reads the 3 bytes
        X_fix += struct.unpack('3b',data)[1]
        Y_fix += struct.unpack('3b',data)[2]
        X_eink=(430 - X_fix)*0.889
        Y_eink=( Y_fix + 400)*0.75
        for idx,rect in enumerate(rectangulos):
            if (X_eink>rect[0][0]) and (X_eink<rect[1][0]):
                if (Y_eink>rect[0][1]) and (Y_eink<rect[1][1]):
                    if (len(mensajes)>idx):
                        print(mensajes[idx][1])
                        delFromMsg(idx)
                        

lastIndex=-3
def delFromMsg(index):
    global lastIndex
    if (index != lastIndex):
        lastIndex=index
        mens = {}
        id_medication = []
        id_medication.append(mensajes[index][2])
        mens["id_dsm"]=id_medication
        mens["status"]="1"
        notifyMsgReceived(mens)
        mensajes.remove(mensajes[index])
        drawScreen()
    