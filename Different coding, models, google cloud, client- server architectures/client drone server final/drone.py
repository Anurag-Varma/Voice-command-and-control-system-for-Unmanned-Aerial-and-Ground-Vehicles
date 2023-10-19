import socket
import struct
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time

import argparse  
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()

print('Connecting to vehicle on: %s' % args.connect)
vehicle = connect(args.connect, baud=57600, wait_ready=True)


import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import SpeechModels
import tensorflow as tf
import librosa
import numpy as np

from tensorflow.keras.models import Model, load_model
from kapre.time_frequency import Melspectrogram, Spectrogram
from kapre.utils import Normalization2D



commands=["unknown/silence","nine","yes","no","up","down","left","right","on","off","stop",
          "go","zero","one","two","three","four","five","six","seven","eight","backward",
          "bed","bird","cat","dog","follow","forward","happy","house","learn","marvin",
          "sheila","tree","visual","wow"]




model = load_model('./model-attRNN-35words.h5', custom_objects={'Melspectrogram': Melspectrogram, 'Normalization2D': Normalization2D })
print("Model loaded")





def addr_to_bytes(addr):
    return socket.inet_aton(addr[0]) + struct.pack('H', addr[1])

def bytes_to_addr(addr):
    return (socket.inet_ntoa(addr[:4]), struct.unpack('H', addr[4:])[0])

def arm_and_takeoff(aTargetAltitude):

  print ("Basic pre-arm checks")
  while not vehicle.is_armable:
    print (" Waiting for vehicle to initialise...")
    time.sleep(1)
        
  print( "Arming motors")
  vehicle.mode    = VehicleMode("GUIDED")
  vehicle.armed   = True

  while not vehicle.armed:
    print (" Waiting for arming...")
    time.sleep(1)

  print ("Taking off!")
  vehicle.simple_takeoff(aTargetAltitude)

  while True:
    print (" Altitude: ", vehicle.location.global_relative_frame.alt )
    if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
      print ("Reached target altitude")
      break
    time.sleep(1)


def send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration=0):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame Needs to be MAV_FRAME_BODY_NED for forward/back left/right control.
        0b0000111111000111, # type_mask
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # m/s
        0, 0, 0, # x, y, z acceleration
        0, 0)
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)

val=1024*4
CHUNK = val
CHANNELS = 1
RATE = 16000


HOST = '34.125.102.191'        
PORT = 40002            
soc = socket.socket()

try:
    soc.connect((HOST, PORT))
    soc.send(b"drone")
    print("connected")
    
    data = soc.recv(val)
    peer = bytes_to_addr(data)
    print('peer:', *peer)
    
    
    if 1:
        print("started receiving")
        while 1:
            
            fileName = "test audio.wav"
            print("Receiving file")
            bytes_read = soc.recv(val)
            with open(fileName, "wb") as f:
                print("inside while")
                i=0
                while True:
                    print(i)
                    if bytes_read[-4:]==bytes("stop",'utf-8'):
                        f.write(bytes_read[:-4])
                        break
                    f.write(bytes_read)
                    
                    bytes_read = soc.recv(val)
                    i=i+1
                    if i>100:
                        raise Exception("Connection closed")
            f.close()
            print("audio received")
            
            
            
            y, sr = librosa.load(fileName, sr=None)
            
            X = np.empty((1, 16000))  
            curX=y
            if curX.shape[0] == 16000:
                    X[0] = curX
            elif curX.shape[0] > 16000:
                    randPos = np.random.randint(curX.shape[0]-16000)
                    X[0] = curX[randPos:randPos+16000]
            else:
                    randPos = np.random.randint(16000-curX.shape[0])
                    X[0, randPos:randPos + curX.shape[0]] = curX

            print("Predicting model")
            y_predict = model.predict(X[:1])
            
            output=str(commands[np.argmax(y_predict,axis=1)[0]])
            print("Command is : "+output)
            
            if output=="on":
                arm_and_takeoff(10)
                print("Take off complete")
            elif output=="off":
                print("Now let's land")
                vehicle.mode = VehicleMode("RTL")
                vehicle.close()
            elif output=="right":
                velocity_x = 0
                velocity_y = 5
                velocity_z = 0
                duration = 5
                send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration)
            elif output=="left":
                velocity_x = 0
                velocity_y = -5
                velocity_z = 0
                duration = 5
                send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration)
            elif output=="up":
                velocity_x = 0
                velocity_y = 0
                velocity_z = -1.5
                duration = 1
                send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration)
            elif output=="down":
                velocity_x = 0
                velocity_y = 0
                velocity_z = 1.5
                duration = 1
                send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration)
            elif output=="backward":
                velocity_x = -5
                velocity_y = 0
                velocity_z = 0
                duration = 5
                send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration)
            elif output=="forward":
                velocity_x = 5
                velocity_y = 0
                velocity_z = 0
                duration = 5
                send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration)
            elif output=="stop":
                print("Now let's land")
                vehicle.mode = VehicleMode("RTL")
                vehicle.close()
                break
                
    
    soc.shutdown(socket.SHUT_RDWR)
    soc.close()            
                
except Exception as e:
        print("Error:",e)
        soc.shutdown(socket.SHUT_RDWR)
        soc.close()  
        print("Vehicle going home location due to error")
        vehicle.mode = VehicleMode("RTL")
        vehicle.close()
        
        