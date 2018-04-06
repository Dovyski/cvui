# Include the directory where cvui is so we can load it
import sys
sys.path.append('../../../')

import numpy as np
import cv2
import cvui

cvui.random_number_generator(1, 2)

 # Create a black image
img = np.zeros((512,512,3), np.uint8)

cv2.namedWindow('Window')

# Draw a diagonal blue line with thickness of 5 px
cv2.line(img,(0,0),(511,511),(255,0,0),5)

cv2.rectangle(img,(384,0),(510,128),(0,255,0),3)
cv2.circle(img,(447,63), 63, (0,0,255), -1)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)

cv2.imshow('Window', img)

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()
