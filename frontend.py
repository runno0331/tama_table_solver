import tkinter as tk
from table_reader import TableReader
from solver import Solver
from utils import is_float
import numpy as np


class Frontend:
	TABLE_SIZE = (6, 6)
	def __init__(self):
		self.create_root()
		self.table_reader = TableReader(self)
		self.solver = Solver(self)
		self.create_components()
		self.table = []
		
	def create_root(self):
		self.root = tk.Tk()
		self.root.title('solver')
		self.root.geometry('550x260')
		self.root.resizable(width=False, height=False)

	def create_components(self):
		frame = tk.Frame(self.root, bg="green")

		# table inputs
		table_frame = tk.Frame(frame, padx=10, pady=10, bg="red")
		self.textboxes = [
			[tk.Entry(table_frame, width=8) for _ in range(self.TABLE_SIZE[1])] 
			for _ in range(self.TABLE_SIZE[0])
		]
		for i in range(self.TABLE_SIZE[0]):
			for j in range(self.TABLE_SIZE[1]):
				self.textboxes[i][j].grid(row=i, column=j)

		# button inputs
		self.use_bias = tk.BooleanVar()
		button_frame = tk.Frame(self.root, padx=5, pady=5, bg="black")
		load_table_button = tk.Button(button_frame, width=6, text='読み込み', command=self.table_reader.read_table)
		calculate_button = tk.Button(button_frame, width=6, text='計算', command=lambda:[self.read_table(), self.solver.solve()])
		bias_checkbox = tk.Checkbutton(button_frame, width=6, variable=self.use_bias, text="バイアス")
		delete_button = tk.Button(button_frame, width=6, text='削除', command=self.delete_textbox_value)
		
		load_table_button.pack(anchor=tk.W, pady=5)
		calculate_button.pack(anchor=tk.W, pady=5)
		bias_checkbox.pack(anchor=tk.W, pady=5)
		delete_button.pack(anchor=tk.W, pady=5)

		# result outputs
		result_frame = tk.Frame(frame, padx=5, pady=5, bg="blue")
		title_label = tk.Label(result_frame, text="計算結果")
		self.result_text = tk.StringVar()
		result_output_label = tk.Label(result_frame, textvariable=self.result_text, justify='left')

		title_label.pack(anchor=tk.NW)
		result_output_label.pack(anchor=tk.NW)

		frame.pack(anchor=tk.NW, side=tk.LEFT)
		table_frame.pack(anchor=tk.NW, side=tk.TOP)
		result_frame.pack(anchor=tk.W, side=tk.TOP, fill=tk.X)
		button_frame.pack(anchor=tk.NW, side=tk.LEFT)
	
	def run(self):
		self.root.mainloop()

	def delete_textbox_value(self):
		for i in range(self.TABLE_SIZE[0]):
			for j in range(self.TABLE_SIZE[1]):
				self.textboxes[i][j].delete(0, tk.END)

	def update_table(self, table):
		self.delete_textbox_value()

		for i in range(len(table)):
			if i >= self.TABLE_SIZE[0]:
				break
				
			for j in range(len(table[i])):
				if j >= self.TABLE_SIZE[1]:
					break
				
				if table[i][j] is np.nan:
					self.textboxes[i][j].insert(tk.END, '?')
				else:
					self.textboxes[i][j].insert(tk.END, table[i][j])
	
	def read_table(self):
		self.table = []
		for i in range(self.TABLE_SIZE[0]):
			row = []
			for j in range(self.TABLE_SIZE[1]):
				value = self.textboxes[i][j].get()
				if is_float(value):
					row.append(float(value))
				elif value == '?':
					row.append(np.nan)
				else:
					continue
			
			if len(row) > 0:
				self.table.append(row)

	def set_result_str(self, result_str):
		self.result_text.set(result_str)
