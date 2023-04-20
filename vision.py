import cv2
import numpy as np
import glob

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cv2.startWindowThread()
cap = cv2.VideoCapture(0)
coordXList = []
areaList = []

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
			cv2.rectangle(frame, (xA, yA), (xB, yB), (255, 0, 0), 2)
			coordXList.append(xA)
			h = abs(xA - xB)
			w = abs(yB - yA)
			area0 = w * h
			areaList.append(area0)

		cv2.imshow('frame', resize)

		if len(boxes) == 1:
			print("I can see!")
			break
		else:
			print("nothng there")		
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
			cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
			resize = cv2.resize(img, (1280, 720), interpolation=cv2.INTER_NEAREST)
			cv2.imshow('tracker', resize)
			coordXList.append(x)
			area = w * h
			areaList.append(area)
			if len(coordXList) > 1:
				if coordXList[0] > coordXList[1]:
					coordXList.pop(1)
					print("going right")
					
				elif coordXList[0] < coordXList[1]:
					coordXList.pop(1)
					print("going left")
							
				else:
					coordXList.pop(1)
					print("im good where i am")
		

			if len(areaList) > 1:
				if areaList[0] > areaList[1]:
					areaList.pop(1)
					print("backing up")

				elif areaList[0] < areaList[1]:
					areaList.pop(1)
					print("going forward")
			
				else:
					areaList.pop(1)
					print("im good where i am")

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		else:
			d = personDetect()
			tracking(d)



while True:
	cv2.waitKey(1)
	d = personDetect()
	tracking(d)
	
cap.release()
cv2.destroyAllWindows()
