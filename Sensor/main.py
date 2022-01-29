
import cv2
from datetime import *
import time
import logging
import base64
import sys
import os
import shutil

import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import datetime
import sys
import re
from typing import NamedTuple

import json


import os


log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
print('Hello 1')


def on_connect(client, userdata, flags, rc):
    """ The callback for when the client receives a CONNACK response from the server."""
    print('Connected with result code ' + str(rc))
    client.subscribe('topic')
# The callback for when a PUBLISH message is received from the server.
def save_influx(json_body, body):
    print(" Saving data of : ", sys.getsizeof(str(body)), ' bytes')
    influx_client.write_points(json_body)
def on_message(client, userdata, msg):
    #current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = str(int(time.time()))
    #print(msg.topic + ' ' + str(msg.payload))

    #sensor_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    #if sensor_data is not None:
    #    _send_sensor_data_to_influxdb(sensor_data)
    print("a")
    #splits_ = str(msg.payload).split('XXX')
    #splits_ = str(msg.payload).split('XXX')
    #for i in range(len(splits_)):
    json_body = [
    {
        "measurement": "t_1_4",
        "tags": {
            "camera_id": camera_id,
        },
        #"time": timestamp,
        "transmitdelay":transmitdelay,
        "JPGQuality":JPGQuality,
        "fields": {
            "value": str(msg.payload) #str(msg.payload)
        }
    }
    ]
    save_influx(json_body, str(msg.payload))
    #print(msg.topic, str(msg.payload))
    #thinktime or sleep aftersending

    client.loop_stop()  # Stop loop
    client.disconnect()  # disconnect

    #if splits_[i] == 'refresh':
    #client.reinitialise()
    #camera = Camera(camera_id, destination_cluster_ip, JPGQuality, transmitdelay, './imagesout')
    #camera.processVideoStream()
    #time.sleep(1)

    #val = splits_[1].replace('"', '')
    #print('recieved id: ', val)
    #if int(val) == 2222:
    #    camera = Camera(camera_id, destination_cluster_ip, JPGQuality, transmitdelay, './imagesout')
    #    camera.processVideoStream()

def _init_influxdb_database():
    databases = influx_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influx_client.create_database(INFLUXDB_DATABASE)
    influx_client.switch_database(INFLUXDB_DATABASE)

def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
class Camera():
    def __init__(self,camera_id,destination_cluster_ip,JPGQuality,transmitdelay, folder):
        self.camera_id = camera_id
        self.destination_cluster_ip = destination_cluster_ip
        self.JPGQuality = JPGQuality
        self.transmitdelay = transmitdelay
        start = time.time()
        self.folder = folder



    def cleanup(self):


        folder = './imagesout'
        for the_file in os.listdir ('./imagesout'):
            file_path = os.path.join ('./imagesout', the_file)
            try:
                if os.path.isfile (file_path):
                    os.unlink (file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print (e)



    def processVideoStream(self, thread=0):


            
            vidcap = cv2.VideoCapture('black.mp4')
            success, image = vidcap.read ()
            count = 0
            success = True

            day_date= date.today()

            start = time.time ()
            #i = self.JPGQuality
            print('JPGQuality:', self.JPGQuality)


            list_image_base64 = []


            list_image_base64_str = ''
            image_base64_last = ''
            while success:
                #for i in range(9):
                #self.JPGQuality = i + 1
                cv2.imwrite("./imagesout/frame%d.jpg" % count, image, [int(cv2.IMWRITE_JPEG_QUALITY), self.JPGQuality])  # save frame as JPEG file
                imageFileNameandPath =  ("./imagesout/frame%d.jpg" % count)
                image_base64 = self.convertToBase64(imageFileNameandPath)
                success, image = vidcap.read ()
                print ('Read a new frame: ', success,  ' thread number:', thread)

                timestamp = str(int(time.time()))
                frame_id = timestamp+str(count)
                end = time.time()
                runtime_seconds = end - start
                data = {'camera_id':str(self.camera_id), 'frame_id':str(frame_id), 'timestamp':timestamp, 'duration':str(int(runtime_seconds)) }
                #self.cassandraclient.saveToCassandra(self.camera_id, frame_id, timestamp,day_date ,image_base64)
                #self.kafkaclient.saveToKafka(self.camera_id, frame_id, timestamp, day_date, image_base64)

                #list_image_base64.append(str(image_base64))
                list_image_base64_str += str(image_base64)+'XXX'
                image_base64_last = str(image_base64)


                cname = "Client" + str(count)
                client = mqtt.Client(cname)

                client.on_connect = on_connect
                client.on_message = on_message
                client.connect("132.207.170.59", 1883, 60)
                client.subscribe("topic", qos=1)

                client.publish(topic="topic", payload=str(image_base64), qos=1, retain=False)
                #client.loop_forever()
                client.loop_start()
                time.sleep(1)
                #list_image_base64_str = ''
                #print(count)
                count += 1

                print('Experiment Runtime (seconds): ' + str(int(runtime_seconds)))
                print('Images written per (second): ' + str(count/runtime_seconds))


            self.cleanup()


    def convertToBase64(self,fileNameandPath):

        with open(fileNameandPath, "rb") as imageFile:
            str = base64.b64encode(imageFile.read())
        return str

camera_id = 123# sys.argv[1]  # 123
destination_cluster_ip = '132.207.170.59' #sys.argv[2]  # '132.207.170.59'
JPGQuality = 50 #int(sys.argv[3] ) # 20
transmitdelay = 10 # int(sys.argv[4])  # 10

check_looping = 0

INFLUXDB_DATABASE = 'sensorslog'
influx_client = InfluxDBClient('132.207.170.25', 8086, database='sensorslog')
_init_influxdb_database()



#while True:
camera = Camera(camera_id, destination_cluster_ip, JPGQuality, transmitdelay, './imagesout')
camera.processVideoStream()
