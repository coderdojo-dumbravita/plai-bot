# import the necessary packages
import picamera
import picamera.array
import time
import cv2
from pololu_drv8835_rpi import motors
from pprint import pprint 

# initialize the camera and grab a reference to the raw camera capture

# allow the camera to warmup
time.sleep(0.1)

# grab an image from the camera
# display the image on screen and wait for a keypress

#motors.setSpeeds(-480, 480)
#time.sleep(0.04)
#motors.setSpeeds(-90,90)
try:
    with picamera.PiCamera() as camera:
        camera.resolution=(320,240)
        camera.shutter_speed = 400
        camera.exposure_mode = 'off'

        with picamera.array.PiRGBArray(camera) as output:
            while True:
                for exposure_mode in picamera.PiCamera.EXPOSURE_MODES:
                    camera.exposure_mode = 'nightpreview'
                    print exposure_mode
                    camera.capture(output, format="bgr")
                    image = output.array
                    #print (image.shape)
                

                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    #th, dst = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
                    th2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                                cv2.THRESH_BINARY,11,2)
                    print (gray.shape)
                    #for x in range(gray.shape[0]):
                    print (range(gray.shape[0]))
                    sift = cv2.xfeatures2d.SIFT_create()
                    data = sift.detectAndCompute(gray, None)
                    a, b = data
                    if a!=None and b!=None:
                        print(len(a), len(b))

                    output.truncate(0)
                    cv2.imshow("Image", th2)
                    cv2.waitKey(25)
finally:
    motors.setSpeeds(0, 0)
    

    """
        # kps: 274, descriptors: (274, 128)
    >>> surf = cv2.xfeatures2d.SURF_create()
    >>> (kps, descs) = surf.detectAndCompute(gray, None)
    >>> print("# kps: {}, descriptors: {}".format(len(kps), descs.shape))
    # kps: 393, descriptors: (393, 64)
    """
