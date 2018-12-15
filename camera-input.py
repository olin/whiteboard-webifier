import cv2 as cv
import numpy as np
import subprocess as sp

# gphoto_pipe = sp.Popen("gphoto --capture-movie --stdout"), stdout=sp.PIPE, 

FFMPEG_BIN = "ffplay"
command = [ FFMPEG_BIN,
        '-i', 'fifo']            # fifo is the named pipe
        # '-pix_fmt', 'bgr24',      # opencv requires bgr24 pixel format.
        # '-vcodec', 'rawvideo',
        # '-an','-sn',              # we want to disable audio processing (there is no audio)
        # '-f', 'image2pipe']    
pipe = sp.Popen("gphoto2 --capture-movie --stdout | ffmpeg -i pipe:0 -pix_fmt bgr24 -vcodec rawvideo -an -sn -f image2pipe -", stdout = sp.PIPE, bufsize=10**8, shell=True)

# while True:
#     # Capture frame-by-frame
#     raw_image = pipe.stdout.read(960*640*3)
#     # transform the byte read into a numpy array
#     image =  np.fromstring(raw_image, dtype='uint8')
#     # print(image)
#     if len(image) != 0:
#         print(image.shape)
#         image = image.reshape((640,960,3))          # Notice how height is specified first and then width
#         if image is not None:
#             cv.imshow('Video', image)

#         if cv.waitKey(1) & 0xFF == ord('q'):
#             break
#         pipe.stdout.flush()

# cv2.destroyAllWindows()

def nothing(x):
    pass
cv.namedWindow('frame')
cv.createTrackbar('thresh', 'frame', 117, 255, nothing)
cv.createTrackbar('neighbor', 'frame', 25, 255, nothing)
cv.createTrackbar('c', 'frame', 10, 255, nothing)


while(True):
    raw_image = pipe.stdout.read(960*640*3)
    # transform the byte read into a numpy array
    frame =  np.fromstring(raw_image, dtype='uint8')
    if len(frame) != 0:
            frame = frame.reshape((640,960,3))          # Notice how height is specified first and then width
            if frame is not None:
                mask = np.zeros(frame.shape,np.uint8)

                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

                # ret,thresh1 = cv.threshold(gray,200,255,cv.THRESH_BINARY)

                thresh = cv.getTrackbarPos('thresh', 'frame')
                neighbor = (cv.getTrackbarPos('neighbor', 'frame')*2)+3
                c = cv.getTrackbarPos('c', 'frame')

                th3 = cv.adaptiveThreshold(gray,200,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,neighbor,c)
                im2, contours, hierarchy = cv.findContours(th3, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

                # Isolate one contour that we care about
                print(contours[1].squeeze())

                # Isolate one contour (for now)
                # cv.drawContours(mask, [contours[1]], -1, (0,255,0), 3)

                # print(frame.shape)
                # pixel_points = np.nonzero(mask)
                # point_tuples = list(zip(pixel_points[0], pixel_points[1]))
                # print(point_tuples)
                # print(pixel_points[0].shape)

                cv.imshow('frame', th3)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
            pipe.stdout.flush()

cv.destroyAllWindows()

