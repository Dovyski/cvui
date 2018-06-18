#
# This is a dummy class to illustrate the use of cvui in a project
# that contains multiple files.
#
# Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
#

import cvui

class Class2:
	def renderMessage(self, frame):
		cvui.text(frame, 10, 10, 'Message')
