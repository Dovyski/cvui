#
# This is a dummy class to illustrate the use of cvui in a project
# that contains multiple files.
#
# Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
#

import cvui

class Class1:
	def __init__(self):
		self.checked = [False]

	def renderInfo(self, frame):
		cvui.window(frame, 10, 50, 100, 120, 'Info')
		cvui.checkbox(frame, 15, 80, 'Checked', self.checked)
