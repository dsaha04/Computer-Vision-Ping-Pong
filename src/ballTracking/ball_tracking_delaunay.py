# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import random
from delaunay2D import Delaunay2D

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the color of
# ball in the HSV color space, then initialize the
# list of tracked points
lowerColor = (0, 142, 135)
upperColor = (179, 255, 255)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)

queue = []

# keep looping
frameCount = 0;
while True:
	frameCount += 1
	# grab the current frame
	frame = vs.read()
	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	width = int(600)
	height = int(600 * vs.get(4) / vs.get(3))
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, lowerColor, upperColor)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None

	# draws points for delaunay triangulation

	for seed in queue:
		cv2.circle(frame, (seed[0], seed[1]), 1, (255, 255, 255), 5)

	dt = Delaunay2D()
	for p in queue:
		dt.addPoint(p)
	triangles = dt.exportTriangles()
	for triangle in triangles:
		p1 = queue[triangle[0]]
		p2 = queue[triangle[1]]
		p3 = queue[triangle[2]]
		cv2.line(frame, p1, p2, (255, 255, 255), 1)
		cv2.line(frame, p1, p3, (255, 255, 255), 1)
		cv2.line(frame, p2, p3, (255, 255, 255), 1)


	if frameCount % 8 == 0:
		random.shuffle(queue)
		queue.pop(0)
		queue.append(np.random.randint(0, [width, height]))

	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		# DRAWING

		seeds = np.random.randint(0, [width, height])
		# FILL IN EMPTY POINTS AT START
		if len(queue) == 0:
			for i in range(20):
				seed = np.random.randint(0, [width, height])
				queue.append(seed)
				dt.addPoint(seed)

		if frameCount % 3 == 0:
			random.shuffle(queue)
			queue.pop(0)
			queue.append([int(x), int(y)])

		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius), (255, 255, 255), 0)
			cv2.circle(frame, center, 5, (0, 255, 255), -1)
	# update the points queue
	pts.appendleft(center)
	# loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		# cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()
# otherwise, release the camera
else:
	vs.release()
# close all windows
cv2.destroyAllWindows()