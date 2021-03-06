#import opencv,Numpy,array(numpy)
import cv2
import time
import numpy as np

#preparation for writing the output video
fourcc=cv2.VideoWriter_fourcc(*'XVID')
out=cv2.VideoWriter('output1.mp4',fourcc,20.0,(640,480))

#reading from the webcAm
cap=cv2.VideoCapture(0)

#allow the system to sleep for 3 secs before the webcam starts
time.sleep(3)
count=0
background=0

#capture the background in range of 60
for i in range(60):
	ret,background=cap.read()
background=np.flip(background,axis=1)

##read every fraME FROM the webcam,until the camera is open
while(cap.isOpened()):
	ret,img=cap.read()
	if not ret:
		break
	count+=1
	img=np.flip(img,axis=1)

	#convert the colour space from BGR to hsv
	hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	##generate masks to detect yellow color
	lower_yellow=np.array([20,100,50])
	upper_yellow=np.array([30,255,255])
	mask1=cv2.inRange(hsv,lower_yellow,upper_yellow)

	lower_yellow=np.array([170,100,80])
	upper_yellow=np.array([180,255,255])
	mask2=cv2.inRange(hsv,lower_yellow,upper_yellow)
	mask1=mask1+mask2

	##open and dilate the mask image
	mask1=cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
	mask1=cv2.morphologyEx(mask1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))

	##create an inverted mask to segment out the red colour from the frame
	mask2=cv2.bitwise_not(mask1)

	##segment the red colour part out of the frame using the bitwise and the inverted mask
	res1=cv2.bitwise_and(img,img,mask=mask2)

	##create image showing static background frame pixels only for the masked region
	res2=cv2.bitwise_and(background,background,mask=mask1)

	##generating the final output and writing
	finalOutput=cv2.addWeighted(res1,1,res2,1,0)
	out.write(finalOutput)
	cv2.imshow("magic",finalOutput)
	cv2.waitKey(1)

cap.release()
out.release()
cv2.destroyAllWindows()



