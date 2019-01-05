import cv2 as cv
import numpy as np
import subprocess as sp
import requests
from base64 import b64encode
from auth import USERNAME, PASSWORD

from socketIO_client_nexus import SocketIO, LoggingNamespace

cap = cv.VideoCapture(0)

socket = SocketIO('127.0.0.1', 9091, headers={'Authorization': 'Basic ' + str(b64encode('{}:{}'.format(USERNAME, PASSWORD).encode('ascii')))[2:]})

def nothing(x):
	pass

def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
 
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
 
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
 
	# return the ordered coordinates
	return rect

def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
 
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
 
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
 
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
 
	# compute the perspective transform matrix and then apply it
	M = cv.getPerspectiveTransform(rect, dst)
	warped = cv.warpPerspective(image, M, (maxWidth, maxHeight))
 
	# return the warped image
	return warped

def process_camera_input():
	# pipe = sp.Popen("gphoto2 --capture-movie --stdout | ffmpeg -i pipe:0 -pix_fmt bgr24 -vcodec rawvideo -an -sn -f image2pipe -", stdout = sp.PIPE, bufsize=10**8, shell=True)

	cv.namedWindow('frame')
	# cv.createTrackbar('thresh', 'frame', 117, 255, nothing)
	# cv.createTrackbar('neighbor', 'frame', 25, 255, nothing)
	# cv.createTrackbar('c', 'frame', 10, 255, nothing)


	while(True):
		# raw_image = pipe.stdout.read(960*640*3)
		ret, frame = cap.read()
		# transform the byte read into a numpy array
		# frame =  np.fromstring(raw_image, dtype='uint8')
		if len(frame) != 0:
				# frame = frame.reshape((640,960,3))          # Notice how height is specified first and then width
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
					im2, contours, hierarchy = cv.findContours(th3, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

					cv.drawContours(frame, contours, -1, (0,255,0), 3)

					points = np.array([(15,106),(926,105),(884,440),(61,443)])
					transform = four_point_transform(frame, points)

					# cv.imshow('frame', frame)
					x_vals = []
					y_vals = []
					i=0
					for contour in contours:
						for point in contour:
							# if i%10 == 0:
								# print(type(int(point[0][1])))x
							y_vals.append(int(point[0][1]))
							x_vals.append(int(point[0][0]))
							# i+=1

					socket.emit('point-vals', {'points': {'x': x_vals, 'y': y_vals}})
					# requests.post('http://localhost:9091/points', json={'points': {'x': x_vals, 'y': y_vals}})
					# print(x_vals)
					# all_vals = [point[0] for contour in contours for point in contour]

					# print(all_vals)

				key = cv.waitKey(1)
				if key & 0xFF == ord('q'):
					break
				# save image 
				elif key & 0xFF == ord(' '):
					retval, output_image = cv.imencode('.jpg', transform)

				# pipe.stdout.flush()

	cv.destroyAllWindows()

process_camera_input()