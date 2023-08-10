import cv2
import numpy as np
import glob
import RPi.GPIO as GPIO
import time
from HR8825 import HR8825

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cv2.startWindowThread()
cap = cv2.VideoCapture(0)
coordXList = []
yList = []

Motor1 = HR8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 5))
Motor2 = HR8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
Motor1.SetMicroStep('hardward','fullstep')
Motor2.SetMicroStep('hardward' ,'fullstep') 

def personDetect():
	global cap
	while True:
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		ret, img = cap.read()
		#img_rgb = cv2.cvtColor(src=img_yuyv, code=cv2.COLOR_YUV2BGR_YUYV)
		frame = cv2.cvtColor(src=img, code=cv2.COLOR_RGB2GRAY)
		resize = cv2.resize(frame, (1280, 720), interpolation=cv2.INTER_NEAREST)
		boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )
		boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
		for (xA, yA, xB, yB) in boxes:
			cv2.rectangle(frame, (xA, yA), (xB, yB), (105, 0, 0), 2)
			h = abs(xA - xB)
			w = abs(yB - yA)
			yList.append(yA)

		cv2.imshow('frame', resize)

		if len(boxes) == 1:
			print("I can see!")
			Motor1.Stop()
			Motor2.Stop()
			break
		else:
			print("nothng there")
			Motor1.Stop()
			Motor2.Stop()		
	return xA, yA, w, h

def tracking(d):
	global cap
	tracker = cv2.legacy.TrackerKCF_create()
	ok, img = cap.read()	
	#frame = cv2.cvtColor(src=img, code=cv2.COLOR_RGB2GRAY)	
	detected = tracker.init(img, d)
	while True:
		ok, img = cap.read()
		ok, d = tracker.update(img)

		if ok:
			(x, y, w, h) = [int(v) for v in d]	
			cv2.rectangle(img, (x, y), (x+w, y+h), (105, 0, 0), 2)
			resize = cv2.resize(img, (1280, 720), interpolation=cv2.INTER_NEAREST)
			cv2.imshow('tracker', resize)
			cent = (x + (x+w)) / 2
			coordXList.append(cent)
			print(cent)
			yList.append(y)
			
			if len(yList) > 1:
				if yList[0] > yList[1]-5:
					yList.pop(1)
					print("backing up")
					Motor1.TurnStep(Dir='backward', steps=10, stepdelay=0.005)
					time.sleep(0.005)
					Motor2.TurnStep(Dir='backward', steps=10, stepdelay=0.005)
					time.sleep(0.005)

					
				elif yList[0] < yList[1]+5:
					yList.pop(1)
					Motor1.TurnStep(Dir='forward', steps=10, stepdelay=0.005)
					time.sleep(0.005)
					print("going forward")
					Motor2.TurnStep(Dir='forward', steps=10, stepdelay=0.005)
					time.sleep(0.005)

								
				else:
					yList.pop(1)
					print("im good where i am")
					Motor1.Stop()
					Motor2.Stop()
			

			if len(coordXList) > 0:
				if coordXList[0] > 340:
					coordXList.pop(0)
					print("going right")
					Motor1.TurnStep(Dir='backward', steps=10, stepdelay=0.005)
					time.sleep(0.005)	
					Motor2.TurnStep(Dir='forward', steps=10, stepdelay=0.005)					
					time.sleep(0.005)
					
				elif coordXList[0] < 300:
					coordXList.pop(0)
					print("going left")
					Motor1.TurnStep(Dir='forward', steps=10, stepdelay=0.005)
					time.sleep(0.005)	
					Motor2.TurnStep(Dir='backward', steps=10, stepdelay=0.005)
					time.sleep(0.005)
												
				else:
					coordXList.pop(0)
					print("im good where i am")
					Motor1.Stop()
					Motor2.Stop()		
			
			if cv2.waitKey(1) & 0xFF == ord('q'):
				Motor1.Stop()
				Motor2.Stop()
				break
		else:
			d = personDetect()
			tracking(d)


while cv2.waitKey(1) & 0xFF != ord('q'):
	d = personDetect()
	tracking(d)
Motor1.Stop()
Motor2.Stop()	
cap.release()
cv2.destroyAllWindows()
