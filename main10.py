# Copyright (c) 2019 Leechy inc.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import cv2
import pickle
import xlsxwriter
from imutils import rotate_bound
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from PIL import Image, ImageTk
import os, os.path

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

print(color.BOLD + color.RED + '\nLeechy Labs | Spectrum Analyser\n' + color.END)


drunkdatanum = 0
not_drunkdatanum = 0

DRUNK_DIR = 'data/graph/drunk'
drunkdatanum = len([name for name in os.listdir(DRUNK_DIR) if os.path.isfile(os.path.join(DRUNK_DIR, name))])

NOT_DRUNK_DIR = 'data/graph/not_drunk'
not_drunkdatanum = len([name for name in os.listdir(DRUNK_DIR) if os.path.isfile(os.path.join(NOT_DRUNK_DIR, name))])

row = 1

sensetivity = 615
x1 = 480
y1 = 1000
x2 = 578
y2 = 1040
angle = 52.5
flip = False
plot_graph = False

cmp_graph = [500]
nor_color = (0, 0, 1)
mouse_rectangle = False
clear = True
live = False
auto = False

plt.ion()

def rotate_clockwise(matrix, degree=90):
	try:
		return matrix if not degree else rotate_clockwise(zip(*matrix[::-1]), degree-90)
	except TypeError:
		return [[0]]

def mouse_event(event,x,y,flags,param):
	global x1, x2, y1, y2, mouse_rectangle

	if event == cv2.EVENT_LBUTTONDOWN:
		mouse_rectangle = True
		x1,y1 = x,y
	elif event == cv2.EVENT_MOUSEMOVE:
		if mouse_rectangle == True:
			x2,y2 = x, y
	elif event == cv2.EVENT_LBUTTONUP:
		x2,y2 = x, y

		if x2 < x1:
			x1,x2 = x2,x1

		if y2 < y1:
			y1,y2 = y2,y1

		mouse_rectangle = False

cv2.namedWindow("Spectrum Analyser", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Spectrum Analyser", mouse_event)

vc = cv2.VideoCapture(0)

SHEET_DIR = "data/sheet"
sheet_name = "data"

if len([name for name in os.listdir(SHEET_DIR) if os.path.isfile(os.path.join(SHEET_DIR, name))])-1 > 0:
	sheet_name = sheet_name + str(len([name for name in os.listdir(SHEET_DIR) if os.path.isfile(os.path.join(SHEET_DIR, name))])-1)

workbook = xlsxwriter.Workbook('data/sheet/' + sheet_name + '.xlsx')
worksheet = workbook.add_worksheet()

worksheet.set_column("A1:J5", 52)
worksheet.set_default_row(220)
worksheet.write(0,1, "Graph")
worksheet.write(0,2, "Status")
worksheet.write(0,3, "Image")
worksheet.write(0,4, "Settings")
worksheet.write(0,5, "Date")

if row < 0 :
	print("row can't be less then 0!")
	exit()

def AddToWorksheet(row,status):
	worksheet.insert_image(row,1, 'data/graph/' + str(status) + '/' + (str(not_drunkdatanum) if status=="not_drunk" else str(drunkdatanum)) + '.png', {'x_scale': 0.47,'y_scale': 0.5,'x_offset': 2,'y_offset': 2,'positioning': 1})
	worksheet.insert_image(row,3, 'data/frames/' + str(status) + '/' + (str(not_drunkdatanum) if status=="not_drunk" else str(drunkdatanum)) + '.png', {'x_scale': 0.47,'y_scale': 0.5,'x_offset': 2,'y_offset': 2,'positioning': 1})
	worksheet.write(row, 0, row)
	worksheet.write(row, 2, status)
	worksheet.write(row, 4, str(settingsJson))
	worksheet.write(row, 5, str(datetime.datetime.now()))

	print("\n----------------\nSaved!" + "\nRow:" + str(row) + "\nNot Drunk Data Num:" + str(not_drunkdatanum) + "\nDrunk Data Num:" + str(drunkdatanum))


def AutoSpectrumFinder(frame):

	frame = (rotate_bound(frame, angle))
	height, width = frame.shape[:2]

	start_row, start_col = 0, 0
	end_row, end_col = height, width // 2

	frame = frame[start_row:end_row , start_col:end_col]

	grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	ret,th = cv2.threshold(grayscale,127,255, 0)
	
	contours, hierarchy = cv2.findContours(th, 2, 1)
	cnt = contours
	big_contour = []
	max = 0
	for i in cnt:
		area = cv2.contourArea(i)
		if(area > max):
			max = area
			big_contour = i

	final = cv2.drawContours(frame, big_contour, -1, (0,255,0), 3)
	point = big_contour[int(len(big_contour)/2)][0]

	x = point[0]
	y = point[1]
	# cv2.imshow('mask', final)

	return x - 50, y - 20, x + 50, y + 10


if vc.isOpened():
	rval, frame = vc.read()
else:
	rval = False

while rval:
	frame = (rotate_bound(frame, angle))
	prntframe = frame.copy()
	cv2.rectangle(prntframe, (x1, y1), (x2, y2), (0,100,0), 2)
	prntframe = prntframe
	try:
		cutframe = cv2.cvtColor(frame[y1:y2, x1:x2], cv2.COLOR_BGR2GRAY)
	except cv2.error:
		cutframe = [[0]]
	cv2.imshow("Spectrum Analyser", prntframe)
	key = cv2.waitKey(500)
	rval, frame = vc.read()

	graph = [500]

	if plot_graph:

		if not mouse_rectangle:

			if live == False:
				plot_graph = False
			else:
				plt.clf()

			for line in list(rotate_clockwise(cutframe)):
				bright = 0

				for point in line:
					bright += point

				graph.append(bright)

			graph.append(500)
			plt.ylim(top=max(graph))
			plt.ylim(bottom=min(graph))
			if not cmp_graph == [500]:
				plt.plot(cmp_graph[::-1] if flip else cmp_graph, color=(0, 0, 0))
				plt.ylim(top=max([max(cmp_graph), max(graph)]))
				plt.ylim(bottom=min([min(cmp_graph), min(graph)]))

				nor_color = (0, 1, 0)

				for i, x in enumerate(graph):
					if abs(cmp_graph[i] - x) < sensetivity:
						nor_color = (1, 0, 0)

			plt.plot(graph[::-1] if flip else graph, color=nor_color)
			plt.draw()
			plt.pause(0.001)
		else:
			plt.draw()

	if key == ord("w"):
		y1 -= 2
	elif key == ord("s"):
		y2 += 2
	elif key == ord("l"):
		if live:
			live = False
		else:
			live = True

		print("Live = " + str(live))
	elif key == ord("/"):
		print("Searching...")
		try:
			x1, y1, x2, y2 = AutoSpectrumFinder(frame)
			print("Found", (x1, y1, x2, y2))
		except:
			print("Could'nt find, please select manually")
		
	elif key == ord("\\"):
		cv2.destroyWindow("mask")
	elif key == ord("a"):
		x1 -= 2
	elif key == ord("d"):
		x2 += 2
	elif key == ord("z"):
		y1 += 2
	elif key == ord("x"):
		y2 -= 2
	elif key == ord("q"):
		x1 += 2
	elif key == ord("e"):
		x2 -= 2
	elif key == ord("r"):
		angle -= 0.5
		if angle <= 0:
			angle = 360

		print("Angle = " + str(angle))
	elif key == ord("t"):
		angle += 0.5
		if angle >= 360:
			angle = 0

		print("Angle = " + str(angle))
	elif key == ord("y"):
		angle += 180
		sleep(0.1)
		if angle <= 0:
			angle = 360
		if angle >= 360:
			angle = 0
		print("Angle = " + str(angle))
	elif key == ord("n"):
		sensetivity -= 10
		print("sensitivity = " + str(sensetivity))
	elif key == ord("m"):
		sensetivity += 10
		print("sensitivity = " + str(sensetivity))
	elif key == ord("o"):
		plot_graph = False
		plt.clf()
		plt.close()
		print("\nGraph: Closed")
	elif key == ord("p"):
		plot_graph = True
		plt.clf()
		print("\nGraph: Plotting...")
	elif key == ord("v"):
		flip = not flip
		sleep(0.1)
		print("Flip = " + str(flip))
	elif key == ord("c"):
		print("System: Closed")
		save = ""
		while save != 'y' or save != 'n':
			save = input("Do you want to save the sheet? (y/n)")

			if save == "n":
				workbook.close()
				os.remove("data/sheet/" + sheet_name + ".xlsx")
				print("Deleted!")
				break
			else:
				workbook.close()
				break
		break
	
	elif key == ord("k"):
		cmp_graph = graph
		nor_color = (0,1,0)
	elif key == ord("j"):
		cmp_graph = [500]
		nor_color = (1, 0, 0)
	elif key == ord("h"):
		pickle.dump({"sensitivity": sensetivity, "x1": x1, "y1": y1, "x2": x2, "y2": y2, "angle": angle, "flip": flip}, open("settings.p", "wb"))
	elif key == ord("g"):
		try:
			print("Paused graph, press CTRL+C while focused on the terminal to resume it.")
			plt.pause(10000000)
		except KeyboardInterrupt:
			print("Resumed program")
	elif key == ord("]") and not live:
		print("Recorded Drunk!")

		plt.savefig('data/graph/drunk/' + str(drunkdatanum) + '.png')
		cv2.imwrite("data/frames/drunk/" + str(drunkdatanum) + '.png', cutframe)

		AddToWorksheet(row,"drunk")

		drunkdatanum += 1
		row += 1
	elif key == ord("[") and not live:
		print("Recorded Not Drunk!")

		plt.savefig('data/graph/not_drunk/' + str(not_drunkdatanum) + '.png')
		cv2.imwrite("data/frames/not_drunk/" + str(drunkdatanum) + '.png', cutframe)

		AddToWorksheet(row,"not_drunk")

		not_drunkdatanum += 1
		row += 1

cv2.destroyWindow("Infrared spectrometer")
workbook.close()