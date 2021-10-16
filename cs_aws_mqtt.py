from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
from cs_display import drawScreen
from cs_global import mensajes
import os

# Custom MQTT message callback
def appointmentCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    data = json.loads(message.payload.decode('utf-8'))
    mensajes.append(("b",data["m_doctor"],data["date"],int( time.time() )))
    drawScreen()
    os.system('/usr/bin/aplay /mnt/nas/proyectos/04.-curamSenes/Audio/newAppointment.wav')

def medicationCallback(client, userdata, message):
    print("Received a new medication: ")
    print(message.payload)
    data = json.loads(message.payload.decode('utf-8'))
    mensajes.append(("a",data["m_name"],data["id_dsm"],int( time.time() )))
    mens = {}
    id_medication = []
    id_medication.append( data["id_dsm"] )
    mens["id_dsm"]=id_medication
    mens["status"]="0"
    notifyMsgReceived(mens)
    drawScreen()
    os.system('/usr/bin/aplay /mnt/nas/proyectos/04.-curamSenes/Audio/newMedicine.wav')
    

def notifyMsgReceived(message):
    messageJson = json.dumps(message)
    print(messageJson)
    myAWSIoTMQTTClient.publish("0123b3712890bda201/rtn", messageJson, 0)

myAWSIoTMQTTClient = None
def initAwsMQTT():
    global myAWSIoTMQTTClient
    host            = "a3ie5pbyo9m77t-ats.iot.eu-west-1.amazonaws.com"
    rootCAPath      = "cert/root-CA.crt"
    certificatePath = "cert/eink-curamsenes-00001.cert.pem"
    privateKeyPath  = "cert/eink-curamsenes-00001.private.key"
    port            = 8883
    clientId        = "eink-curamsenes"
    topic1           = "0123b3712890bda201/medication"
    topic2           = "0123b3712890bda201/med_appointment"

    # Init AWSIoTMQTTClient
    
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, port)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)


    # AWSIoTMQTTClient connection configuration
    myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

    # Connect and subscribe to AWS IoT
    myAWSIoTMQTTClient.connect()
    myAWSIoTMQTTClient.subscribe(topic1, 1, medicationCallback)
    myAWSIoTMQTTClient.subscribe(topic2, 1, appointmentCallback)


