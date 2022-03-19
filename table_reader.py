from PIL import Image, ImageTk
import pyocr
import numpy as np
import tkinter as tk
import pyautogui
from utils import is_float


class TableReader:
	SCALE_RATIO = 2

	def __init__(self, frontend):
		self.frontend = frontend
		self.engine = pyocr.get_available_tools()[0]

	def read_table(self):
		self.sub_window = tk.Toplevel()
		self.sub_window.title('Press Enter to confirm')

		# get screenshot and resize
		self.raw_screenshot = pyautogui.screenshot()
		self.resized_screenshot = \
			self.raw_screenshot.resize(
				size=(self.raw_screenshot.width // self.SCALE_RATIO, 
					self.raw_screenshot.height // self.SCALE_RATIO),
				resample=Image.BILINEAR
			)

		screenshot_tk = ImageTk.PhotoImage(self.resized_screenshot)
		self.canvas = tk.Canvas(
			self.sub_window,
			width=self.resized_screenshot.width,
			height=self.resized_screenshot.height,
		)
		self.canvas.create_image(0, 0, image=screenshot_tk, anchor=tk.NW)
		self.canvas.pack()

		# binded functions
		self.canvas.bind("<ButtonPress-1>", self.start_point_get)
		self.canvas.bind("<Button1-Motion>", self.draw_rect)
		self.canvas.bind("<ButtonRelease-1>", self.release_action)
		self.canvas.focus_set()
		self.canvas.bind("<Return>", self.get_screenshot)
		self.canvas.bind("<Escape>", self.destroy_window)
		self.canvas.bind("q", self.destroy_window)
		self.sub_window.mainloop()
	
	def start_point_get(self, event):
		self.canvas.delete("rect")

		self.canvas.create_rectangle(
			event.x, event.y,
			event.x+1, event.y + 1,
			outline="red", tag="rect"
		)
		self.start_x, self.start_y = event.x, event.y

	def draw_rect(self, event):
		if event.x < 0:
			self.end_x = 0
		else:
			self.end_x = min(self.resized_screenshot.width, event.x)
		if event.y < 0:
			self.end_y = 0
		else:
			self.end_y = min(self.resized_screenshot.height, event.y)

		self.canvas.coords("rect", self.start_x, self.start_y, self.end_x, self.end_y)
	
	def release_action(self, event):
		self.start_x, self.start_y, self.end_x, self.end_y = [
			round(n * self.SCALE_RATIO) for n in self.canvas.coords("rect")
		]
		self.start_x, self.end_x = min(self.start_x, self.end_x), max(self.start_x, self.end_x)
		self.start_y, self.end_y = min(self.start_y, self.end_y), max(self.start_y, self.end_y)

	def get_screenshot(self, event):
		cropped_screenshot = \
			self.raw_screenshot.crop((self.start_x, self.start_y, self.end_x, self.end_y))
		
		# read and parse output
		txt = self.engine.image_to_string(cropped_screenshot, lang="jpn")
		lines = txt.split('\n')
		table = []
		for line in lines:
			values = line.split()
			row = []
			for value in values:
				value = value.replace(',', '')
				if is_float(value):
					row.append(float(value))
				elif value == '?':
					row.append(np.nan)

			if len(row) > 0:
				table.append(row)

		self.frontend.update_table(table)
		
		self.destroy_window()

	def destroy_window(self, event=None):
		self.sub_window.destroy()
