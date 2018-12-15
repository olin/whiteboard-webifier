import cv2 as cv
import numpy as np
import subprocess as sp
from repo_update import update_yaml_link

def nothing(x):
    pass

def process_camera_input():
    pipe = sp.Popen("gphoto2 --capture-movie --stdout | ffmpeg -i pipe:0 -pix_fmt bgr24 -vcodec rawvideo -an -sn -f image2pipe -", stdout = sp.PIPE, bufsize=10**8, shell=True)

    cv.namedWindow('frame')
    # cv.createTrackbar('thresh', 'frame', 117, 255, nothing)
    # cv.createTrackbar('neighbor', 'frame', 25, 255, nothing)
    # cv.createTrackbar('c', 'frame', 10, 255, nothing)


    while(True):
        raw_image = pipe.stdout.read(960*640*3)
        # transform the byte read into a numpy array
        frame =  np.fromstring(raw_image, dtype='uint8')
        if len(frame) != 0:
                frame = frame.reshape((640,960,3))          # Notice how height is specified first and then width
                if frame is not None:
                    

                    mask = np.zeros(frame.shape,np.uint8)

                    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)


                    # thresh = cv.getTrackbarPos('thresh', 'frame')
                    # neighbor = (cv.getTrackbarPos('neighbor', 'frame')*2)+3
                    # c = cv.getTrackbarPos('c', 'frame')

                    thresh = 117
                    neighbor = 25
                    c = 10

                    th3 = cv.adaptiveThreshold(gray,200,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,neighbor,c)
                    # im2, contours, hierarchy = cv.findContours(th3, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

                    # Isolate one contour that we care about
                    # print(contours[1].squeeze())

                    cv.imshow('frame', th3)

                key = cv.waitKey(1)
                if key & 0xFF == ord('q'):
                    break
                # save image 
                elif key & 0xFF == ord('e'):
                    retval, output_image = cv.imencode('.jpg', frame)
                    print(type(output_image))
                    # cv.imwrite('test.jpg', frame)
                    # print(output_image)
                    break

                pipe.stdout.flush()

    cv.destroyAllWindows()

process_camera_input()