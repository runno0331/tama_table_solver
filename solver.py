import numpy as np


class Solver:
	def __init__(self, frontend):
		self.frontend = frontend

	def solve(self):
		table = self.frontend.table
		table = np.array(table)
		use_bias = self.frontend.use_bias.get()
		if not self.check_table_format(table):
			self.frontend.set_result_str(self.message)
		else:
			# place to predict
			nan_row, nan_col = self.nan_position

			# split data
			train_data = np.delete(table, nan_col, axis=1)
			X, y = np.delete(train_data, nan_row, axis=0), train_data[nan_row]
			if use_bias:
				X = np.concatenate([X, np.ones((1, X.shape[1]))], axis=0)
			test_data = table[:, nan_col]
			test_x = np.delete(test_data, nan_row, axis=0)
			if use_bias:
				test_x = np.concatenate([test_x, [1]])

			w = np.linalg.inv(X @ X.T) @ X @ y

			self.output_result(test_x, w)

	def output_result(self, x, w):
		result = x @ w
		result_str = '{:.2f}'.format(result) + '\n = '
		total_row_len = 0
		for i, (w_elem, x_elem) in enumerate(zip(w, x)):
			temp = '{:.2f}'.format(w_elem) + '*' + str(x_elem)
			total_row_len += len(temp)
			result_str += temp
			
			if total_row_len > 40:
				total_row_len = 0
				result_str += '\n'
			if i != len(w) - 1:
				result_str += ' + '

		self.frontend.set_result_str(result_str)
		
	def check_table_format(self, table):
		# no input
		if len(table) == 0:
			self.message = '入力が少ないです'
			return False
		
		row_length = [len(table[i]) for i in range(len(table))]
		row_length = set(row_length)

		# not in table format
		if len(row_length) != 1:
			self.message = '入力が少ないです'
			return False
		
		is_nan = np.isnan(table)
		nan_row = np.where(is_nan.any(axis=1))[0]
		nan_col = np.where(is_nan.any(axis=0))[0]

		# too many unknowns
		if len(nan_row) != 1 or len(nan_col) != 1:
			self.message = '未知数の数が不正です'
			return False

		self.nan_position = (nan_row[0], nan_col[0])
		return True