#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import picamera
import picamera.array

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (224, 224)
        camera.start_preview()
        time.sleep(2)
        camera.capture(stream, 'rgb')
        camera.capture('image.jpg')
        print(stream.array.shape)
        camera.stop_preview()
        
from imageio import imread
import numpy as np
img = imread("image.jpg")
img = img/255.0
img = img.reshape((1,224,224,3))

import tensorflow as tf
with open('model87.json','r') as f:
  json_file = f.read()
loaded_model = tf.keras.models.model_from_json(json_file)
# load weights into new model
loaded_model.load_weights("model87.h5")
print("Loaded model from disk")
loaded_model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

pred = loaded_model.predict(img)
print(pred)

import board
import neopixel
import time
#Initialisiere den NeoPixel auf Pin D18 mit einer Länge von 8 Pixeln
pixels=neopixel.NeoPixel(board.D18,8, brightness=0.1)
print(pred[0][0])
if pred[0][0]<=0.5:
   pixels[0]=(255,0,0) #Erster Pixel rot
else:
   pixels[1]=(0,255,0) #Zweiter Pixel grün

time.sleep(5)
#Alle Pixel ausschalten
for i in range(0,8):
   pixels[i]=(0,0,0)

