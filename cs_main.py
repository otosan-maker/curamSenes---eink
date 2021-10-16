import threading
import time
from cs_aws_mqtt import initAwsMQTT,notifyMsgReceived
from cs_display  import drawScreen
from cs_mouse import mouse
from cs_global import mensajes
import os

x1 = threading.Thread(target=mouse, args=(1,))
x1.start()

drawScreen()
initAwsMQTT()

segundosRetencion=40
while True:
    time.sleep(20)
    bDrawScreen=False
    now = int( time.time() )
    print( now )
    for mensaje in mensajes:
        if (mensaje[0]=='a'):
            if (mensaje[3]+segundosRetencion < now):
                # Delete this medication
                print("Deleted medication")
                print(mensaje[3])
                mens = {}
                id_medication = []
                id_medication.append(mensaje[2])
                mens["id_dsm"]=id_medication
                mens["status"]="2"
                notifyMsgReceived(mens)
                mensajes.remove(mensaje)
                bDrawScreen=True
        if bDrawScreen:
            bDrawScreen=False
            os.system('/usr/bin/aplay /mnt/nas/proyectos/04.-curamSenes/Audio/medicationDeleted.wav')
            drawScreen()
