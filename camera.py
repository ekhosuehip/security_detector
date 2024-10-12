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