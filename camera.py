import cv2
import time
import paho.mqtt.client as mqtt
import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, storage
from playsound import playsound

# MQTT settings
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "home/camera_motion"

# Firebase settings
FIREBASE_CREDENTIALS_PATH = "ServiceAccountKey.json"
FIREBASE_STORAGE_BUCKET = "only-motion-detector.appspot.com"
# Alarm sound file path
ALARM_SOUND_PATH = "alarm.mp3" 

# Initialize Firebase Admin SDK
cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred, {'storageBucket': FIREBASE_STORAGE_BUCKET})
bucket = storage.bucket()

# Initialize MQTT client
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT)

# Initialize the camera
macbook_camera = cv2.VideoCapture(0)
iphone_camera = cv2.VideoCapture(1)

# Get the video frame width and height for camera
macbook_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 740)
macbook_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

iphone_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 740)
iphone_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_width_macbook = int(macbook_camera.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height_macbook = int(macbook_camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

frame_width_iphone = int(iphone_camera.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height_iphone = int(iphone_camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

