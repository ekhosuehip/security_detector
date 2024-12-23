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

recordings_folder = "recordings"
os.makedirs(recordings_folder, exist_ok=True)

# Generate a unique filename
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
mp4_video_path_macbook = os.path.join(recordings_folder, f'motion_detected_macbook_{timestamp}.mp4')

# Define the codec and create a VideoWriter object for MacBook camera
fourcc_macbook = cv2.VideoWriter_fourcc(*'mp4v')
out_macbook = cv2.VideoWriter(mp4_video_path_macbook, fourcc_macbook, 20.0, (frame_width_macbook, frame_height_macbook))

# Optional: Generate a unique filename with timestamp for iPhone camera
mp4_video_path_iphone = os.path.join(recordings_folder, f'motion_detected_iphone_{timestamp}.mp4')
fourcc_iphone = cv2.VideoWriter_fourcc(*'mp4v')
out_iphone = cv2.VideoWriter(mp4_video_path_iphone, fourcc_iphone, 20.0, (frame_width_iphone, frame_height_iphone))

# Give some time for cameras to warm up
time.sleep(2)

# Read the first frame from MacBook camera
ret_macbook, frame1_macbook = macbook_camera.read()
ret_macbook, frame2_macbook = macbook_camera.read()

# Read the first frame from iPhone camera (if available)
ret_iphone, frame1_iphone = iphone_camera.read()
ret_iphone, frame2_iphone = iphone_camera.read()