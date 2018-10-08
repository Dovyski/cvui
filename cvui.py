"""
A (very) simple UI lib built on top of OpenCV drawing primitives.
Version: 2.7

Use of cvui revolves around calling cvui.init() to initialize the lib,
rendering cvui components to a np.ndarray (that you handle yourself) and
finally showing that np.ndarray on the screen using cvui.imshow(), which
is cvui's version of cv2.imshow(). Alternatively you can use cv2.imshow()
to show things, but in such case you must call cvui.update() yourself
before calling cv.imshow().

E.g.:

	import numpy as np
	import cv2
	import cvui

	WINDOW_NAME = 'CVUI Hello World!'

	frame = np.zeros((200, 500, 3), np.uint8)
	cvui.init(WINDOW_NAME)

	while (True):
		# Fill the frame with a nice color
		frame[:] = (49, 52, 49)

		cvui.text(frame, x, y, 'Hello world!')
		cvui.imshow(WINDOW_NAME, frame)

		if cv2.waitKey(20) == 27:
			break

Read the full documentation at https://dovyski.github.io/cvui/

Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
Licensed under the MIT license.
"""

import cv2
import numpy as np
import sys

def main():
	# TODO: make something here?
	return 0

if __name__ == '__main__':
    main()

# Lib version
VERSION = '2.7'

# Constants regarding component interactions
ROW = 0
COLUMN = 1
DOWN = 2
CLICK = 3
OVER = 4
OUT = 5
UP = 6
IS_DOWN = 7

# Constants regarding mouse buttons
LEFT_BUTTON = 0
MIDDLE_BUTTON = 1
RIGHT_BUTTON = 2

# Constants regarding components
TRACKBAR_HIDE_SEGMENT_LABELS = 1
TRACKBAR_HIDE_STEP_SCALE = 2
TRACKBAR_DISCRETE = 4
TRACKBAR_HIDE_MIN_MAX_LABELS = 8
TRACKBAR_HIDE_VALUE_LABEL = 16
TRACKBAR_HIDE_LABELS = 32

# Internal things
_IS_PY2 = sys.version_info.major == 2
CVUI_ANTIALISED = cv2.LINE_AA
CVUI_FILLED = -1

# Represent a 2D point.
class Point:
	def __init__(self, theX = 0, theY = 0):
		self.x = theX
		self.y = theY

	def inside(self, theRect):
		return theRect.contains(self)

# Represent a rectangle.
class Rect:
	def __init__(self, theX = 0, theY = 0, theWidth = 0, theHeight = 0):
		self.x = theX
		self.y = theY
		self.width = theWidth
		self.height = theHeight

	def contains(self, thePoint):
		return thePoint.x >= self.x and thePoint.x <= (self.x + self.width) and thePoint.y >= self.y and thePoint.y <= (self.y + self.height)

	def area(self):
		return self.width * self.height

# Represent the size of something, i.e. width and height.
# It is essentially a simplified version of Rect where x and y are zero.
class Size(Rect):
	def __init__(self, theWidth = 0, theHeight = 0):
		self.x = 0
		self.y = 0
		self.width = theWidth
		self.height = theHeight

# Describe a block structure used by cvui to handle `begin*()` and `end*()` calls.
class Block:
	def __init__(self):
		self.where = None              # where the block should be rendered to.
		self.rect = Rect()             # the size and position of the block.
		self.fill = Rect()             # the filled area occuppied by the block as it gets modified by its inner components.
		self.anchor = Point()          # the point where the next component of the block should be rendered.
		self.padding = 0               # padding among components within this block.
		self.type = ROW       		   # type of the block, e.g. ROW or COLUMN.

		self.reset()

	def reset(self):
		self.rect.x = 0
		self.rect.y = 0
		self.rect.width = 0
		self.rect.height = 0

		self.fill = self.rect
		self.fill.width = 0
		self.fill.height = 0

		self.anchor.x = 0
		self.anchor.y = 0

		self.padding = 0

# Describe a component label, including info about a shortcut.
# If a label contains "Re&start", then:
# - hasShortcut will be true
# - shortcut will be 's'
# - textBeforeShortcut will be "Re"
# - textAfterShortcut will be "tart"
class Label:
	def __init__(self):
		self.hasShortcut = False
		self.shortcut = ''
		self.textBeforeShortcut = ''
		self.textAfterShortcut = ''

# Describe a mouse button
class MouseButton:
	def __init__(self):
		self.justReleased = False           # if the mouse button was released, i.e. click event.
		self.justPressed = False            # if the mouse button was just pressed, i.e. true for a frame when a button is down.
		self.pressed = False                # if the mouse button is pressed or not.

	def reset(self):
		self.justPressed = False
		self.justReleased = False
		self.pressed = False

# Describe the information of the mouse cursor
class Mouse:
	def __init__(self):
		self.buttons = {                   # status of each button. Use cvui.{RIGHT,LEFT,MIDDLE}_BUTTON to access the buttons.
			LEFT_BUTTON: MouseButton(),
			MIDDLE_BUTTON: MouseButton(),
			RIGHT_BUTTON: MouseButton()
		}
		self.anyButton = MouseButton()     # represent the behavior of all mouse buttons combined
		self.position = Point(0, 0)        # x and y coordinates of the mouse at the moment.

# Describe a (window) context.
class Context:
	def __init__(self):
		self.windowName = ''               # name of the window related to this context.
		self.mouse = Mouse()               # the mouse cursor related to this context.

# Describe the inner parts of the trackbar component.
class TrackbarParams:
	def __init__(self, theMin = 0., theMax = 25., theStep = 1., theSegments = 0, theLabelFormat = '%.0Lf', theOptions = 0):
		self.min = theMin
		self.max = theMax
		self.step = theStep
		self.segments = theSegments
		self.options = theOptions
		self.labelFormat = theLabelFormat

# This class contains all stuff that cvui uses internally to render
# and control interaction with components.
class Internal:
	def __init__(self):
		self.defaultContext = ''
		self.currentContext = ''
		self.contexts = {}             # indexed by the window name.
		self.buffer = []
		self.lastKeyPressed = -1       # TODO: collect it per window
		self.delayWaitKey = -1
		self.screen = Block()
		self.stack = [Block() for i in range(100)] # TODO: make it dynamic
		self.stackCount = -1
		self.trackbarMarginX = 14

		self._render = Render()
		self._render._internal = self

	def isMouseButton(self, theButton, theQuery):
		aRet = False

		if theQuery == CLICK or theQuery == UP:
			aRet = theButton.justReleased
		elif theQuery == DOWN:
			aRet = theButton.justPressed
		elif theQuery == IS_DOWN:
			aRet = theButton.pressed

		return aRet

	def mouseW(self, theWindowName = ''):
		"""
		Return the last position of the mouse.

		\param theWindowName name of the window whose mouse cursor will be used. If nothing is informed (default), the function will return the position of the mouse cursor for the default window (the one informed in `cvui::init()`).
		\return a point containing the position of the mouse cursor in the speficied window.
		"""
		return self.getContext(theWindowName).mouse.position

	def mouseQ(self, theQuery):
		"""
		Query the mouse for events, e.g. "is any button down now?". Available queries are:

		* `cvui::DOWN`: any mouse button was pressed. `cvui::mouse()` returns `true` for a single frame only.
		* `cvui::UP`: any mouse button was released.  `cvui::mouse()` returns `true` for a single frame only.
		* `cvui::CLICK`: any mouse button was clicked (went down then up, no matter the amount of frames in between). `cvui::mouse()` returns `true` for a single frame only.
		* `cvui::IS_DOWN`: any mouse button is currently pressed. `cvui::mouse()` returns `true` for as long as the button is down/pressed.

		It is easier to think of this function as the answer to a questions. For instance, asking if any mouse button went down:

		```
		if (cvui::mouse(cvui::DOWN)) {
		  // Any mouse button just went down.
		}
		```

		The window whose mouse will be queried depends on the context. If `cvui::mouse(query)` is being called after
		`cvui::context()`, the window informed in the context will be queried. If no context is available, the default
		window (informed in `cvui::init()`) will be used.

		Parameters
		----------
		theQuery: int
			Integer describing the intended mouse query. Available queries are `cvui::DOWN`, `cvui::UP`, `cvui::CLICK`, and `cvui::IS_DOWN`.

		\sa mouse(const cv::String&)
		\sa mouse(const cv::String&, int)
		\sa mouse(const cv::String&, int, int)
		\sa mouse(int, int)
		"""
		return self.mouseWQ('', theQuery)

	def mouseWQ(self, theWindowName, theQuery):
		"""
		 Query the mouse for events in a particular window. This function behave exactly like `cvui::mouse(int theQuery)`
		 with the difference that queries are targeted at a particular window.

		 \param theWindowName name of the window that will be queried.
		 \param theQuery an integer describing the intended mouse query. Available queries are `cvui::DOWN`, `cvui::UP`, `cvui::CLICK`, and `cvui::IS_DOWN`.

		 \sa mouse(const cv::String&)
		 \sa mouse(const cv::String&, int, int)
		 \sa mouse(int, int)
		 \sa mouse(int)
		"""
		aButton = self.getContext(theWindowName).mouse.anyButton
		aRet = self.isMouseButton(aButton, theQuery)

		return aRet

	def mouseBQ(self, theButton, theQuery):
		"""
		 Query the mouse for events in a particular button. This function behave exactly like `cvui::mouse(int theQuery)`,
		 with the difference that queries are targeted at a particular mouse button instead.

		 \param theButton an integer describing the mouse button to be queried. Possible values are `cvui::LEFT_BUTTON`, `cvui::MIDDLE_BUTTON` and `cvui::LEFT_BUTTON`.
		 \param theQuery an integer describing the intended mouse query. Available queries are `cvui::DOWN`, `cvui::UP`, `cvui::CLICK`, and `cvui::IS_DOWN`.

		 \sa mouse(const cv::String&)
		 \sa mouse(const cv::String&, int, int)
		 \sa mouse(int)
		"""
		return self.mouseWBQ('', theButton, theQuery)

	def mouseWBQ(self, theWindowName, theButton, theQuery):
		"""
		 Query the mouse for events in a particular button in a particular window. This function behave exactly
		 like `cvui::mouse(int theButton, int theQuery)`, with the difference that queries are targeted at
		 a particular mouse button in a particular window instead.

		 \param theWindowName name of the window that will be queried.
		 \param theButton an integer describing the mouse button to be queried. Possible values are `cvui::LEFT_BUTTON`, `cvui::MIDDLE_BUTTON` and `cvui::LEFT_BUTTON`.
		 \param theQuery an integer describing the intended mouse query. Available queries are `cvui::DOWN`, `cvui::UP`, `cvui::CLICK`, and `cvui::IS_DOWN`.
		"""
		if theButton != RIGHT_BUTTON and theButton != MIDDLE_BUTTON and theButton != LEFT_BUTTON:
			__internal.error(6, 'Invalid mouse button. Are you using one of the available: cvui.{RIGHT,MIDDLE,LEFT}_BUTTON ?')

		aButton = self.getContext(theWindowName).mouse.buttons[theButton]
		aRet = self.isMouseButton(aButton, theQuery)

		return aRet

	def init(self, theWindowName, theDelayWaitKey):
		self.defaultContext = theWindowName
		self.currentContext = theWindowName
		self.delayWaitKey = theDelayWaitKey
		self.lastKeyPressed = -1

	def bitsetHas(self, theBitset, theValue):
		return (theBitset & theValue) != 0

	def error(self, theId, theMessage):
		print('[CVUI] Fatal error (code ', theId, '): ', theMessage)
		cv2.waitKey(100000)
		sys.exit(-1)

	def getContext(self, theWindowName = ''):
		if len(theWindowName) != 0:
			# Get context in particular
			return self.contexts[theWindowName]

		elif len(self.currentContext) != 0:
			# No window provided, return currently active context.
			return self.contexts[self.currentContext]

		elif len(self.defaultContext) != 0:
			# We have no active context, so let's use the default one.
			return self.contexts[self.defaultContext]

		else:
			# Apparently we have no window at all! <o>
			# This should not happen. Probably cvui::init() was never called.
			self.error(5, 'Unable to read context. Did you forget to call cvui.init()?')

	def updateLayoutFlow(self, theBlock, theSize):
		if theBlock.type == ROW:
			aValue = theSize.width + theBlock.padding

			theBlock.anchor.x += aValue
			theBlock.fill.width += aValue
			theBlock.fill.height = max(theSize.height, theBlock.fill.height)

		elif theBlock.type == COLUMN:
			aValue = theSize.height + theBlock.padding

			theBlock.anchor.y += aValue
			theBlock.fill.height += aValue
			theBlock.fill.width = max(theSize.width, theBlock.fill.width)

	def blockStackEmpty(self):
		return self.stackCount == -1

	def topBlock(self):
		if self.stackCount < 0:
			self.error(3, 'You are using a function that should be enclosed by begin*() and end*(), but you probably forgot to call begin*().')

		return self.stack[self.stackCount]

	def pushBlock(self):
		self.stackCount += 1
		return self.stack[self.stackCount]

	def popBlock(self):
		# Check if there is anything to be popped out from the stack.
		if self.stackCount < 0:
			self.error(1, 'Mismatch in the number of begin*()/end*() calls. You are calling one more than the other.')

		aIndex = self.stackCount
		self.stackCount -= 1

		return self.stack[aIndex]

	def createLabel(self, theLabel):
		i = 0
		aBefore = ''
		aAfter = ''

		aLabel = Label()
		aLabel.hasShortcut = False
		aLabel.shortcut = 0
		aLabel.textBeforeShortcut = ''
		aLabel.textAfterShortcut = ''

		while i < len(theLabel):
			c = theLabel[i]
			if c == '&' and i < len(theLabel) - 1:
				aLabel.hasShortcut = True
				aLabel.shortcut = theLabel[i + 1]
				i += 1
			elif aLabel.hasShortcut == False:
				aBefore += c
			else:
				aAfter += c
			i += 1

		aLabel.textBeforeShortcut = aBefore
		aLabel.textAfterShortcut = aAfter

		return aLabel

	def text(self, theBlock, theX, theY, theText, theFontScale, theColor, theUpdateLayout):
		aSizeInfo, aBaseline = cv2.getTextSize(theText, cv2.FONT_HERSHEY_SIMPLEX, theFontScale, 1)

		aTextSize = Size(aSizeInfo[0], aSizeInfo[1])
		aPos = Point(theX, theY + aTextSize.height)

		self._render.text(theBlock, theText, aPos, theFontScale, theColor)

		if theUpdateLayout:
			# Add an extra pixel to the height to overcome OpenCV font size problems.
			aTextSize.height += 1
			self.updateLayoutFlow(theBlock, aTextSize)

	def counter(self, theBlock, theX, theY, theValue, theStep, theFormat):
		aContentArea = Rect(theX + 22, theY, 48, 22)

		if self.buttonWH(theBlock, theX, theY, 22, 22, '-', False):
			theValue[0] -= theStep

		aText = theFormat % theValue[0]
		self._render.counter(theBlock, aContentArea, aText)

		if self.buttonWH(theBlock, aContentArea.x + aContentArea.width, theY, 22, 22, "+", False):
			theValue[0] += theStep

		# Update the layout flow
		aSize = Size(22 * 2 + aContentArea.width, aContentArea.height)
		self.updateLayoutFlow(theBlock, aSize)

		return theValue[0]

	def checkbox(self, theBlock, theX, theY, theLabel, theState, theColor):
		aMouse = self.getContext().mouse
		aRect = Rect(theX, theY, 15, 15)
		aSizeInfo, aBaseline = cv2.getTextSize(theLabel, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
		aTextSize = Rect(0, 0, aSizeInfo[0], aSizeInfo[1])
		aHitArea = Rect(theX, theY, aRect.width + aTextSize.width + 6, aRect.height)
		aMouseIsOver = aHitArea.contains(aMouse.position)

		if aMouseIsOver:
			self._render.checkbox(theBlock, OVER, aRect)

			if aMouse.anyButton.justReleased:
				theState[0] = not theState[0]
		else:
			self._render.checkbox(theBlock, OUT, aRect)

		self._render.checkboxLabel(theBlock, aRect, theLabel, aTextSize, theColor)

		if theState[0]:
			self._render.checkboxCheck(theBlock, aRect)

		# Update the layout flow
		aSize = Size(aHitArea.width, aHitArea.height)
		self.updateLayoutFlow(theBlock, aSize)

		return theState[0]

	def clamp01(self, theValue):
		theValue = 1. if theValue > 1. else theValue
		theValue = 0. if theValue < 0. else theValue
		return theValue

	def trackbarForceValuesAsMultiplesOfSmallStep(self, theParams, theValue):
		if self.bitsetHas(theParams.options, TRACKBAR_DISCRETE) and theParams.step != 0.:
			k = float(theValue[0] - theParams.min) / theParams.step
			k = round(k)
			theValue[0] = theParams.min + theParams.step * k

	def trackbarXPixelToValue(self, theParams, theBounding, thePixelX):
		aRatio = float(thePixelX - (theBounding.x + self.trackbarMarginX)) / (theBounding.width - 2 * self.trackbarMarginX)
		aRatio = self.clamp01(aRatio)
		aValue = theParams.min + aRatio * (theParams.max - theParams.min)
		return aValue

	def trackbarValueToXPixel(self, theParams, theBounding, theValue):
		aRatio = float(theValue - theParams.min) / (theParams.max - theParams.min)
		aRatio = self.clamp01(aRatio)
		aPixelsX = theBounding.x + self.trackbarMarginX + aRatio * (theBounding.width - 2 * self.trackbarMarginX)
		return int(aPixelsX)

	def iarea(self, theX, theY, theWidth, theHeight):
		aMouse = self.getContext().mouse

		# By default, return that the mouse is out of the interaction area.
		aRet = OUT

		# Check if the mouse is over the interaction area.
		aMouseIsOver = Rect(theX, theY, theWidth, theHeight).contains(aMouse.position)

		if aMouseIsOver:
			if aMouse.anyButton.pressed:
				aRet = DOWN
			else:
				aRet = OVER

		# Tell if the button was clicked or not
		if aMouseIsOver and aMouse.anyButton.justReleased:
			aRet = CLICK

		return aRet

	def buttonWH(self, theBlock, theX, theY, theWidth, theHeight, theLabel, theUpdateLayout):
		# Calculate the space that the label will fill
		aSizeInfo, aBaseline = cv2.getTextSize(theLabel, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
		aTextSize = Rect(0, 0, aSizeInfo[0], aSizeInfo[1])

		# Make the button big enough to house the label
		aRect = Rect(theX, theY, theWidth, theHeight)

		# Render the button according to mouse interaction, e.g. OVER, DOWN, OUT.
		aStatus = self.iarea(theX, theY, aRect.width, aRect.height)
		self._render.button(theBlock, aStatus, aRect, theLabel)
		self._render.buttonLabel(theBlock, aStatus, aRect, theLabel, aTextSize)

		# Update the layout flow according to button size
		# if we were told to update.
		if theUpdateLayout:
			aSize = Size(theWidth, theHeight)
			self.updateLayoutFlow(theBlock, aSize)

		aWasShortcutPressed = False

		# Handle keyboard shortcuts
		if self.lastKeyPressed != -1:
			aLabel = self.createLabel(theLabel)

			if aLabel.hasShortcut and aLabel.shortcut.lower() == chr(self.lastKeyPressed).lower():
				aWasShortcutPressed = True

		# Return true if the button was clicked
		return aStatus == CLICK or aWasShortcutPressed

	def button(self, theBlock, theX, theY, theLabel):
		# Calculate the space that the label will fill
		aSizeInfo, aBaseline = cv2.getTextSize(theLabel, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
		aTextSize = Rect(0, 0, aSizeInfo[0], aSizeInfo[1])

		# Create a button based on the size of the text
		return self.buttonWH(theBlock, theX, theY, aTextSize.width + 30, aTextSize.height + 18, theLabel, True)

	def buttonI(self, theBlock, theX, theY, theIdle, theOver, theDown, theUpdateLayout):
		aIdleRows = theIdle.shape[0]
		aIdleCols = theIdle.shape[1]

		aRect = Rect(theX, theY, aIdleCols, aIdleRows)
		aStatus = self.iarea(theX, theY, aRect.width, aRect.height)

		if   aStatus == OUT:  self._render.image(theBlock, aRect, theIdle)
		elif aStatus == OVER: self._render.image(theBlock, aRect, theOver)
		elif aStatus == DOWN: self._render.image(theBlock, aRect, theDown)

		# Update the layout flow according to button size
		# if we were told to update.
		if theUpdateLayout:
			aSize = Size(aRect.width, aRect.height)
			self.updateLayoutFlow(theBlock, aSize)

		# Return true if the button was clicked
		return aStatus == CLICK

	def image(self, theBlock, theX, theY, theImage):
		aImageRows = theImage.shape[0]
		aImageCols = theImage.shape[1]

		aRect = Rect(theX, theY, aImageCols, aImageRows)

		# TODO: check for render outside the frame area
		self._render.image(theBlock, aRect, theImage)

		# Update the layout flow according to image size
		aSize = Size(aImageCols, aImageRows)
		self.updateLayoutFlow(theBlock, aSize)

	def trackbar(self, theBlock, theX, theY, theWidth, theValue, theParams):
		aMouse = self.getContext().mouse
		aContentArea = Rect(theX, theY, theWidth, 45)
		aMouseIsOver = aContentArea.contains(aMouse.position)
		aValue = theValue[0]

		self._render.trackbar(theBlock, OVER if aMouseIsOver else OUT, aContentArea, theValue[0], theParams)

		if aMouse.anyButton.pressed and aMouseIsOver:
			theValue[0] = self.trackbarXPixelToValue(theParams, aContentArea, aMouse.position.x)

			if self.bitsetHas(theParams.options, TRACKBAR_DISCRETE):
				self.trackbarForceValuesAsMultiplesOfSmallStep(theParams, theValue)

		# Update the layout flow
		# TODO: use aSize = aContentArea.size()?
		self.updateLayoutFlow(theBlock, aContentArea)

		return theValue[0] != aValue

	def window(self, theBlock, theX, theY, theWidth, theHeight, theTitle):
		aTitleBar = Rect(theX, theY, theWidth, 20)
		aContent = Rect(theX, theY + aTitleBar.height, theWidth, theHeight - aTitleBar.height)

		self._render.window(theBlock, aTitleBar, aContent, theTitle)

		# Update the layout flow
		aSize = Size(theWidth, theHeight)
		self.updateLayoutFlow(theBlock, aSize)

	def rect(self, theBlock, theX, theY, theWidth, theHeight, theBorderColor, theFillingColor):
		aAnchor = Point(theX, theY);
		aRect = Rect(theX, theY, theWidth, theHeight);

		aRect.x = aAnchor.x + aRect.width if aRect.width < 0 else aAnchor.x
		aRect.y = aAnchor.y + aRect.height if aRect.height < 0 else aAnchor.y
		aRect.width = abs(aRect.width)
		aRect.height = abs(aRect.height)

		self._render.rect(theBlock, aRect, theBorderColor, theFillingColor)

		# Update the layout flow
		aSize = Size(aRect.width, aRect.height)
		self.updateLayoutFlow(theBlock, aSize)

	def sparkline(self, theBlock, theValues, theX, theY, theWidth, theHeight, theColor):
		aRect = Rect(theX, theY, theWidth, theHeight)
		aHowManyValues = len(theValues)

		if (aHowManyValues >= 2):
			aMin,aMax = self.findMinMax(theValues)
			self._render.sparkline(theBlock, theValues, aRect, aMin, aMax, theColor)
		else:
			self.text(theBlock, theX, theY, 'No data.' if aHowManyValues == 0 else 'Insufficient data points.', 0.4, 0xCECECE, False)

		# Update the layout flow
		aSize = Size(theWidth, theHeight)
		self.updateLayoutFlow(theBlock, aSize)

	def hexToScalar(self, theColor):
		aAlpha = (theColor >> 24) & 0xff
		aRed   = (theColor >> 16) & 0xff
		aGreen = (theColor >> 8)  & 0xff
		aBlue  = theColor & 0xff

		return (aBlue, aGreen, aRed, aAlpha)

	def isString(self, theObj):
		return isinstance(theObj, basestring if _IS_PY2 else str)

	def begin(self, theType, theWhere, theX, theY, theWidth, theHeight, thePadding):
		aBlock = self.pushBlock()

		aBlock.where = theWhere

		aBlock.rect.x = theX
		aBlock.rect.y = theY
		aBlock.rect.width = theWidth
		aBlock.rect.height = theHeight

		aBlock.fill = aBlock.rect
		aBlock.fill.width = 0
		aBlock.fill.height = 0

		aBlock.anchor.x = theX
		aBlock.anchor.y = theY

		aBlock.padding = thePadding
		aBlock.type = theType

	def end(self, theType):
		aBlock = self.popBlock()

		if aBlock.type != theType:
			self.error(4, 'Calling wrong type of end*(). E.g. endColumn() instead of endRow(). Check if your begin*() calls are matched with their appropriate end*() calls.')

		# If we still have blocks in the stack, we must update
		# the current top with the dimensions that were filled by
		# the newly popped block.

		if self.blockStackEmpty() == False:
			aTop = self.topBlock()
			aSize = Size()

			# If the block has rect.width < 0 or rect.heigth < 0, it means the
			# user don't want to calculate the block's width/height. It's up to
			# us do to the math. In that case, we use the block's fill rect to find
			# out the occupied space. If the block's width/height is greater than
			# zero, then the user is very specific about the desired size. In that
			# case, we use the provided width/height, no matter what the fill rect
			# actually is.
			aSize.width = aBlock.fill.width if aBlock.rect.width < 0 else aBlock.rect.width
			aSize.height = aBlock.fill.height if aBlock.rect.height < 0 else aBlock.rect.height

			self.updateLayoutFlow(aTop, aSize)

	# Find the min and max values of a vector
	def findMinMax(self, theValues):
		aMin = theValues[0]
		aMax = theValues[0]

		for aValue in theValues:
			if aValue < aMin:
				aMin = aValue

			if aValue > aMax:
				aMax = aValue

		return (aMin, aMax)

# Class that contains all rendering methods.
class Render:
	_internal = None

	def rectangle(self, theWhere, theShape, theColor, theThickness = 1, theLineType = CVUI_ANTIALISED):
		aStartPoint = (int(theShape.x), int(theShape.y))
		aEndPoint = (int(theShape.x + theShape.width), int(theShape.y + theShape.height))

		cv2.rectangle(theWhere, aStartPoint, aEndPoint, theColor, theThickness, theLineType)

	def text(self, theBlock, theText, thePos, theFontScale, theColor):
		aPosition = (int(thePos.x), int(thePos.y))
		cv2.putText(theBlock.where, theText, aPosition, cv2.FONT_HERSHEY_SIMPLEX, theFontScale, self._internal.hexToScalar(theColor), 1, cv2.LINE_AA)

	def counter(self, theBlock, theShape, theValue):
		self.rectangle(theBlock.where, theShape, (0x29, 0x29, 0x29), CVUI_FILLED) # fill
		self.rectangle(theBlock.where, theShape, (0x45, 0x45, 0x45))              # border

		aSizeInfo, aBaseline = cv2.getTextSize(theValue, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
		aTextSize = Rect(0, 0, aSizeInfo[0], aSizeInfo[1])

		aPos = Point(theShape.x + theShape.width / 2 - aTextSize.width / 2, theShape.y + aTextSize.height / 2 + theShape.height / 2)
		cv2.putText(theBlock.where, theValue, (int(aPos.x), int(aPos.y)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0xCE, 0xCE, 0xCE), 1, CVUI_ANTIALISED)

	def button(self, theBlock, theState, theShape, theLabel):
		# Outline
		self.rectangle(theBlock.where, theShape, (0x29, 0x29, 0x29))

		# Border
		theShape.x += 1
		theShape.y +=1
		theShape.width -= 2
		theShape.height -= 2
		self.rectangle(theBlock.where, theShape, (0x4A, 0x4A, 0x4A))

		# Inside
		theShape.x += 1
		theShape.y +=1
		theShape.width -= 2
		theShape.height -= 2
		self.rectangle(theBlock.where, theShape, (0x42, 0x42, 0x42) if theState == OUT else ((0x52, 0x52, 0x52) if theState == OVER else (0x32, 0x32, 0x32)), CVUI_FILLED)

	def image(self, theBlock, theRect, theImage):
		theBlock.where[theRect.y: theRect.y + theRect.height, theRect.x: theRect.x + theRect.width] = theImage

	def putText(self, theBlock, theState, theColor, theText, thePosition):
		aFontScale = 0.39 if theState == DOWN else 0.4
		aTextSize = Rect()

		if theText != '':
			aPosition = (int(thePosition.x), int(thePosition.y))
			cv2.putText(theBlock.where, theText, aPosition, cv2.FONT_HERSHEY_SIMPLEX, aFontScale, theColor, 1, CVUI_ANTIALISED)

			aSizeInfo, aBaseline = cv2.getTextSize(theText, cv2.FONT_HERSHEY_SIMPLEX, aFontScale, 1)
			aTextSize = Rect(0, 0, aSizeInfo[0], aSizeInfo[1])

		return aTextSize.width

	def putTextCentered(self, theBlock, thePosition, theText):
		aFontScale = 0.3

		aSizeInfo, aBaseline = cv2.getTextSize(theText, cv2.FONT_HERSHEY_SIMPLEX, aFontScale, 1)
		aTextSize = Rect(0, 0, aSizeInfo[0], aSizeInfo[1])
		aPositionDecentered = Point(thePosition.x - aTextSize.width / 2, thePosition.y)
		cv2.putText(theBlock.where, theText, (int(aPositionDecentered.x), int(aPositionDecentered.y)), cv2.FONT_HERSHEY_SIMPLEX, aFontScale, (0xCE, 0xCE, 0xCE), 1, CVUI_ANTIALISED)

		return aTextSize.width

	def buttonLabel(self, theBlock, theState, theRect, theLabel, theTextSize):
		aPos = Point(theRect.x + theRect.width / 2 - theTextSize.width / 2, theRect.y + theRect.height / 2 + theTextSize.height / 2)
		aColor = (0xCE, 0xCE, 0xCE)

		aLabel = self._internal.createLabel(theLabel)

		if aLabel.hasShortcut == False:
			self.putText(theBlock, theState, aColor, theLabel, aPos);

		else:
			aWidth = self.putText(theBlock, theState, aColor, aLabel.textBeforeShortcut, aPos)
			aStart = aPos.x + aWidth
			aPos.x += aWidth

			aShortcut = ''
			aShortcut += aLabel.shortcut

			aWidth = self.putText(theBlock, theState, aColor, aShortcut, aPos)
			aEnd = aStart + aWidth
			aPos.x += aWidth

			self.putText(theBlock, theState, aColor, aLabel.textAfterShortcut, aPos)
			cv2.line(theBlock.where, (int(aStart), int(aPos.y + 3)), (int(aEnd), int(aPos.y + 3)), aColor, 1, CVUI_ANTIALISED)

	def trackbarHandle(self, theBlock, theState, theShape, theValue, theParams, theWorkingArea):
		aBarTopLeft = Point(theWorkingArea.x, theWorkingArea.y + theWorkingArea.height / 2)
		aBarHeight = 7

		# Draw the rectangle representing the handle
		aPixelX = self._internal.trackbarValueToXPixel(theParams, theShape, theValue)
		aIndicatorWidth = 3
		aIndicatorHeight = 4
		aPoint1 = Point(aPixelX - aIndicatorWidth, aBarTopLeft.y - aIndicatorHeight)
		aPoint2 = Point(aPixelX + aIndicatorWidth, aBarTopLeft.y + aBarHeight + aIndicatorHeight)
		aRect = Rect(aPoint1.x, aPoint1.y, aPoint2.x - aPoint1.x, aPoint2.y - aPoint1.y)

		aFillColor = 0x525252 if theState == OVER else 0x424242

		self.rect(theBlock, aRect, 0x212121, 0x212121)
		aRect.x += 1
		aRect.y += 1
		aRect.width -= 2
		aRect.height -= 2
		self.rect(theBlock, aRect, 0x515151, aFillColor)

		aShowLabel = self._internal.bitsetHas(theParams.options, TRACKBAR_HIDE_VALUE_LABEL) == False

		# Draw the handle label
		if aShowLabel:
			aTextPos = Point(aPixelX, aPoint2.y + 11)
			aText = theParams.labelFormat % theValue
			self.putTextCentered(theBlock, aTextPos, aText)

	def trackbarPath(self, theBlock, theState, theShape, theValue, theParams, theWorkingArea):
		aBarHeight = 7
		aBarTopLeft = Point(theWorkingArea.x, theWorkingArea.y + theWorkingArea.height / 2)
		aRect = Rect(aBarTopLeft.x, aBarTopLeft.y, theWorkingArea.width, aBarHeight)

		aBorderColor = 0x4e4e4e if theState == OVER else 0x3e3e3e

		self.rect(theBlock, aRect, aBorderColor, 0x292929)
		cv2.line(theBlock.where, (int(aRect.x + 1), int(aRect.y + aBarHeight - 2)), (int(aRect.x + aRect.width - 2), int(aRect.y + aBarHeight - 2)), (0x0e, 0x0e, 0x0e))

	def trackbarSteps(self, theBlock, theState, theShape, theValue, theParams, theWorkingArea):
		aBarTopLeft = Point(theWorkingArea.x, theWorkingArea.y + theWorkingArea.height / 2)
		aColor = (0x51, 0x51, 0x51)

		aDiscrete = self._internal.bitsetHas(theParams.options, TRACKBAR_DISCRETE)
		aFixedStep = theParams.step if aDiscrete else (theParams.max - theParams.min) / 20

		# TODO: check min, max and step to prevent infinite loop.
		aValue = theParams.min
		while aValue <= theParams.max:
			aPixelX = int(self._internal.trackbarValueToXPixel(theParams, theShape, aValue))
			aPoint1 = (aPixelX, int(aBarTopLeft.y))
			aPoint2 = (aPixelX, int(aBarTopLeft.y - 3))
			cv2.line(theBlock.where, aPoint1, aPoint2, aColor)
			aValue += aFixedStep

	def trackbarSegmentLabel(self, theBlock, theShape, theParams, theValue, theWorkingArea, theShowLabel):
		aColor = (0x51, 0x51, 0x51)
		aBarTopLeft = Point(theWorkingArea.x, theWorkingArea.y + theWorkingArea.height / 2)

		aPixelX = int(self._internal.trackbarValueToXPixel(theParams, theShape, theValue))

		aPoint1 = (aPixelX, int(aBarTopLeft.y))
		aPoint2 = (aPixelX, int(aBarTopLeft.y - 8))
		cv2.line(theBlock.where, aPoint1, aPoint2, aColor)

		if theShowLabel:
			aText = theParams.labelFormat % theValue
			aTextPos = Point(aPixelX, aBarTopLeft.y - 11)
			self.putTextCentered(theBlock, aTextPos, aText)

	def trackbarSegments(self, theBlock, theState, theShape, theValue, theParams, theWorkingArea):
		aSegments = 1 if theParams.segments < 1 else theParams.segments
		aSegmentLength = float(theParams.max - theParams.min) / aSegments

		aHasMinMaxLabels = self._internal.bitsetHas(theParams.options, TRACKBAR_HIDE_MIN_MAX_LABELS) == False

		# Render the min value label
		self.trackbarSegmentLabel(theBlock, theShape, theParams, theParams.min, theWorkingArea, aHasMinMaxLabels)

		# Draw large steps and labels
		aHasSegmentLabels = self._internal.bitsetHas(theParams.options, TRACKBAR_HIDE_SEGMENT_LABELS) == False
		# TODO: check min, max and step to prevent infinite loop.
		aValue = theParams.min
		while aValue <= theParams.max:
			self.trackbarSegmentLabel(theBlock, theShape, theParams, aValue, theWorkingArea, aHasSegmentLabels)
			aValue += aSegmentLength

		# Render the max value label
		self.trackbarSegmentLabel(theBlock, theShape, theParams, theParams.max, theWorkingArea, aHasMinMaxLabels)

	def trackbar(self, theBlock, theState, theShape, theValue, theParams):
		aWorkingArea = Rect(theShape.x + self._internal.trackbarMarginX, theShape.y, theShape.width - 2 * self._internal.trackbarMarginX, theShape.height)

		self.trackbarPath(theBlock, theState, theShape, theValue, theParams, aWorkingArea)

		aHideAllLabels = self._internal.bitsetHas(theParams.options, TRACKBAR_HIDE_LABELS)
		aShowSteps = self._internal.bitsetHas(theParams.options, TRACKBAR_HIDE_STEP_SCALE) == False

		if aShowSteps and aHideAllLabels == False:
			self.trackbarSteps(theBlock, theState, theShape, theValue, theParams, aWorkingArea)

		if aHideAllLabels == False:
			self.trackbarSegments(theBlock, theState, theShape, theValue, theParams, aWorkingArea)

		self.trackbarHandle(theBlock, theState, theShape, theValue, theParams, aWorkingArea)

	def checkbox(self, theBlock, theState, theShape):
		# Outline
		self.rectangle(theBlock.where, theShape, (0x63, 0x63, 0x63) if theState == OUT else (0x80, 0x80, 0x80))

		# Border
		theShape.x += 1
		theShape.y+=1
		theShape.width -= 2
		theShape.height -= 2
		self.rectangle(theBlock.where, theShape, (0x17, 0x17, 0x17))

		# Inside
		theShape.x += 1
		theShape.y += 1
		theShape.width -= 2
		theShape.height -= 2
		self.rectangle(theBlock.where, theShape, (0x29, 0x29, 0x29), CVUI_FILLED)

	def checkboxLabel(self, theBlock, theRect, theLabel, theTextSize, theColor):
		aPos = Point(theRect.x + theRect.width + 6, theRect.y + theTextSize.height + theRect.height / 2 - theTextSize.height / 2 - 1)
		self.text(theBlock, theLabel, aPos, 0.4, theColor)

	def checkboxCheck(self, theBlock, theShape):
		theShape.x += 1
		theShape.y += 1
		theShape.width -= 2
		theShape.height -= 2
		self.rectangle(theBlock.where, theShape, (0xFF, 0xBF, 0x75), CVUI_FILLED)

	def window(self, theBlock, theTitleBar, theContent, theTitle):
		aTransparecy = False
		aAlpha = 0.3
		aOverlay = theBlock.where.copy()

		# Render borders in the title bar
		self.rectangle(theBlock.where, theTitleBar, (0x4A, 0x4A, 0x4A));

		# Render the inside of the title bar
		theTitleBar.x += 1
		theTitleBar.y += 1
		theTitleBar.width -= 2
		theTitleBar.height -= 2
		self.rectangle(theBlock.where, theTitleBar, (0x21, 0x21, 0x21), CVUI_FILLED);

		# Render title text.
		aPos = Point(theTitleBar.x + 5, theTitleBar.y + 12)
		cv2.putText(theBlock.where, theTitle, (int(aPos.x), int(aPos.y)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0xCE, 0xCE, 0xCE), 1, CVUI_ANTIALISED)

		# Render borders of the body
		self.rectangle(theBlock.where, theContent, (0x4A, 0x4A, 0x4A))

		# Render the body filling.
		theContent.x += 1
		theContent.y += 1
		theContent.width -= 2
		theContent.height -= 2
		self.rectangle(aOverlay, theContent, (0x31, 0x31, 0x31), CVUI_FILLED)

		if aTransparecy:
			np.copyto(aOverlay, theBlock.where) # theBlock.where.copyTo(aOverlay);
			self.rectangle(aOverlay, theContent, (0x31, 0x31, 0x31), CVUI_FILLED)
			cv2.addWeighted(aOverlay, aAlpha, theBlock.where, 1.0 - aAlpha, 0.0, theBlock.where)
		else:
			self.rectangle(theBlock.where, theContent, (0x31, 0x31, 0x31), CVUI_FILLED)

	def rect(self, theBlock, thePos, theBorderColor, theFillingColor):
		aBorderColor = self._internal.hexToScalar(theBorderColor)
		aFillingColor = self._internal.hexToScalar(theFillingColor)

		aHasFilling = aFillingColor[3] != 0xff

		if aHasFilling:
			self.rectangle(theBlock.where, thePos, aFillingColor, CVUI_FILLED, CVUI_ANTIALISED)

		# Render the border
		self.rectangle(theBlock.where, thePos, aBorderColor)

	def sparkline(self, theBlock, theValues, theRect, theMin, theMax, theColor):
		aSize = len(theValues)
		i = 0
		aScale = theMax - theMin
		aGap = float(theRect.width) / aSize
		aPosX = theRect.x

		while i <= aSize - 2:
			x = aPosX;
			y = (theValues[i] - theMin) / aScale * -(theRect.height - 5) + theRect.y + theRect.height - 5
			aPoint1 = Point(x, y)

			x = aPosX + aGap
			y = (theValues[i + 1] - theMin) / aScale * -(theRect.height - 5) + theRect.y + theRect.height - 5
			aPoint2 = Point(x, y)

			cv2.line(theBlock.where, (int(aPoint1.x), int(aPoint1.y)), (int(aPoint2.x), int(aPoint2.y)), self._internal.hexToScalar(theColor))
			aPosX += aGap

			i += 1

# Access points to internal global namespaces.
__internal = Internal()

def _handleMouse(theEvent, theX, theY, theFlags, theContext):
	aButtons    = [LEFT_BUTTON, MIDDLE_BUTTON, RIGHT_BUTTON]
	aEventsDown = [cv2.EVENT_LBUTTONDOWN, cv2.EVENT_MBUTTONDOWN, cv2.EVENT_RBUTTONDOWN]
	aEventsUp   = [cv2.EVENT_LBUTTONUP, cv2.EVENT_MBUTTONUP, cv2.EVENT_RBUTTONUP]

	for i in range(LEFT_BUTTON, RIGHT_BUTTON + 1):
		aBtn = aButtons[i]

		if theEvent == aEventsDown[i]:
			theContext.mouse.anyButton.justPressed      = True
			theContext.mouse.anyButton.pressed          = True
			theContext.mouse.buttons[aBtn].justPressed  = True
			theContext.mouse.buttons[aBtn].pressed      = True

		elif theEvent == aEventsUp[i]:
			theContext.mouse.anyButton.justReleased     = True
			theContext.mouse.anyButton.pressed          = False
			theContext.mouse.buttons[aBtn].justReleased = True
			theContext.mouse.buttons[aBtn].pressed      = False

	theContext.mouse.position.x = theX
	theContext.mouse.position.y = theY

def init(theWindowName, theDelayWaitKey = -1, theCreateNamedWindow = True):
	"""
	Initializes cvui. You must provide the name of the window where
	components will be added. It is also possible to tell cvui to handle
	OpenCV's event queue automatically (by informing a value greater than zero
	in the `theDelayWaitKey` parameter of the function). In that case, cvui will
	automatically call `cv2.waitKey()` within `cvui.update()`, so you don't
	have to worry about it. The value passed to `theDelayWaitKey` will be
	used as the delay for `cv2.waitKey()`.

	Parameters
	----------
	theWindowName: str
		name of the window where the components will be added.
	theDelayWaitKey: int
		delay value passed to `cv2.waitKey()`. If a negative value is informed (default is `-1`), cvui will not automatically call `cv2.waitKey()` within `cvui.update()`, which will disable keyboard shortcuts for all components. If you want to enable keyboard shortcut for components (e.g. using & in a button label), you must specify a positive value for this param.
	theCreateNamedWindow: bool
		if an OpenCV window named `theWindowName` should be created during the initialization. Windows are created using `cv2.namedWindow()`. If this parameter is `False`, ensure you call `cv2.namedWindow(WINDOW_NAME)` *before* initializing cvui, otherwise it will not be able to track UI interactions.

	See Also
	----------
	watch()
	context()
	"""
	print('This is wrapper function to help code autocompletion.')

def init(theWindowNames, theHowManyWindows, theDelayWaitKey = -1, theCreateNamedWindows = True):
	"""
	Initialize cvui using a list of names of windows where components will be added.
	It is also possible to tell cvui to handle OpenCV's event queue automatically
	(by informing a value greater than zero in the `theDelayWaitKey` parameter of the function).
	In that case, cvui will automatically call `cv2.waitKey()` within `cvui.update()`,
	so you don't have to worry about it. The value passed to `theDelayWaitKey` will be
	used as the delay for `cv2.waitKey()`.

	Parameters
	----------
	theWindowNames: str
		array containing the name of the windows where components will be added. Those windows will be automatically if `theCreateNamedWindows` is `True`.
	theHowManyWindows: int
		how many window names exist in the `theWindowNames` array.
	theDelayWaitKey: int
		delay value passed to `cv2.waitKey()`. If a negative value is informed (default is `-1`), cvui will not automatically call `cv2.waitKey()` within `cvui.update()`, which will disable keyboard shortcuts for all components. If you want to enable keyboard shortcut for components (e.g. using & in a button label), you must specify a positive value for this param.
	theCreateNamedWindows: bool
		if OpenCV windows named according to `theWindowNames` should be created during the initialization. Windows are created using `cv2.namedWindow()`. If this parameter is `False`, ensure you call `cv2.namedWindow(WINDOW_NAME)` for all windows *before* initializing cvui, otherwise it will not be able to track UI interactions.

	See Also
	----------
	watch()
	context()
	"""
	print('This is wrapper function to help code autocompletion.')

def watch(theWindowName, theCreateNamedWindow = True):
	"""
	Track UI interactions of a particular window. This function must be invoked
	for any window that will receive cvui components. cvui automatically calls `cvui.watch()`
	for any window informed in `cvui.init()`, so generally you don't have to watch them
	yourself. If you initialized cvui and told it *not* to create windows automatically,
	you need to call `cvui.watch()` on those windows yourself. `cvui.watch()` can
	automatically create a window before watching it, if it does not exist.

	Parameters
	----------
	theWindowName: str
		name of the window whose UI interactions will be tracked.
	theCreateNamedWindow: bool
		if an OpenCV window named `theWindowName` should be created before it is watched. Windows are created using `cv2.namedWindow()`. If this parameter is `False`, ensure you have called `cv2.namedWindow(WINDOW_NAME)` to create the window, otherwise cvui will not be able to track its UI interactions.

	See Also
	----------
	init()
	context()
	"""
	if theCreateNamedWindow:
		cv2.namedWindow(theWindowName)

	aContex = Context()
	aContex.windowName = theWindowName
	aContex.mouse.position.x = 0
	aContex.mouse.position.y = 0

	aContex.mouse.anyButton.reset()
	aContex.mouse.buttons[RIGHT_BUTTON].reset()
	aContex.mouse.buttons[MIDDLE_BUTTON].reset()
	aContex.mouse.buttons[LEFT_BUTTON].reset()

	__internal.contexts[theWindowName] = aContex
	cv2.setMouseCallback(theWindowName, _handleMouse, __internal.contexts[theWindowName])

def context(theWindowName):
	"""
	Inform cvui that all subsequent component calls belong to a window in particular.
	When using cvui with multiple OpenCV windows, you must call cvui component calls
	between `cvui.contex(NAME)` and `cvui.update(NAME)`, where `NAME` is the name of
	the window. That way, cvui knows which window you are using (`NAME` in this case),
	so it can track mouse events, for instance.

	E.g.

	```
	# Code for window 'window1'.
	cvui.context('window1')
	cvui.text(frame, ...)
	cvui.button(frame, ...)
	cvui.update('window1')


	# somewhere else, code for 'window2'
	cvui.context('window2')
	cvui.printf(frame, ...)
	cvui.printf(frame, ...)
	cvui.update('window2')

	# Show everything in a window
	cv2.imshow(frame)
	```

	Pay attention to the pair `cvui.context(NAME)` and `cvui.update(NAME)`, which
	encloses the component calls for that window. You need such pair for each window
	of your application.

	After calling `cvui.update()`, you can show the result in a window using `cv2.imshow()`.
	If you want to save some typing, you can use `cvui.imshow()`, which calls `cvui.update()`
	for you and then shows the frame in a window.

	E.g.:

	```
	# Code for window 'window1'.
	cvui.context('window1')
	cvui.text(frame, ...)
	cvui.button(frame, ...)
	cvui.imshow('window1')

	# somewhere else, code for 'window2'
	cvui.context('window2')
	cvui.printf(frame, ...)
	cvui.printf(frame, ...)
	cvui.imshow('window2')
	```

	In that case, you don't have to bother calling `cvui.update()` yourself, since
	`cvui.imshow()` will do it for you.

	Parameters
	----------
	theWindowName: str
		name of the window that will receive components from all subsequent cvui calls.

	See Also
	----------
	init()
	watch()
	"""
	__internal.currentContext = theWindowName

def imshow(theWindowName, theFrame):
	"""
	Display an image in the specified window and update the internal structures of cvui.
	This function can be used as a replacement for `cv2.imshow()`. If you want to use
	`cv2.imshow() instead of `cvui.imshow()`, you must ensure you call `cvui.update()`
	*after* all component calls and *before* `cv2.imshow()`, so cvui can update its
	internal structures.

	In general, it is easier to call `cvui.imshow()` alone instead of calling
	`cvui.update()' immediately followed by `cv2.imshow()`.

	Parameters
	----------
	theWindowName: str
		name of the window that will be shown.
	theFrame: np.ndarray
		image, i.e. `np.ndarray`, to be shown in the window.

	See Also
	----------
	update()
	context()
	watch()
	"""
	update(theWindowName)
	cv2.imshow(theWindowName, theFrame)

def lastKeyPressed():
	"""
	Return the last key that was pressed. This function will only
	work if a value greater than zero was passed to `cvui.init()`
	as the delay waitkey parameter.

	See Also
	----------
	init()
	"""
	return __internal.lastKeyPressed

def mouse(theWindowName = ''):
	"""
	Return the last position of the mouse.

	Parameters
	----------
	theWindowName: str
		name of the window whose mouse cursor will be used. If nothing is informed (default), the function will return the position of the mouse cursor for the default window (the one informed in `cvui.init()`).

	Returns
	----------
	a point containing the position of the mouse cursor in the speficied window.
	"""
	print('This is wrapper function to help code autocompletion.')

def mouse(theQuery):
	"""
	Query the mouse for events, e.g. 'is any button down now?'. Available queries are:

	* `cvui.DOWN`: any mouse button was pressed. `cvui.mouse()` returns `True` for a single frame only.
	* `cvui.UP`: any mouse button was released.  `cvui.mouse()` returns `True` for a single frame only.
	* `cvui.CLICK`: any mouse button was clicked (went down then up, no matter the amount of frames in between). `cvui.mouse()` returns `True` for a single frame only.
	* `cvui.IS_DOWN`: any mouse button is currently pressed. `cvui.mouse()` returns `True` for as long as the button is down/pressed.

	It is easier to think of this function as the answer to a questions. For instance, asking if any mouse button went down:

	```
	if cvui.mouse(cvui.DOWN):
	# Any mouse button just went down.

	```

	The window whose mouse will be queried depends on the context. If `cvui.mouse(query)` is being called after
	`cvui.context()`, the window informed in the context will be queried. If no context is available, the default
	window (informed in `cvui.init()`) will be used.

	Parameters
	----------
	theQuery: int
		an integer describing the intended mouse query. Available queries are `cvui.DOWN`, `cvui.UP`, `cvui.CLICK`, and `cvui.IS_DOWN`.

	See Also
	----------
	mouse(str)
	mouse(str, int)
	mouse(str, int, int)
	mouse(int, int)
	"""
	print('This is wrapper function to help code autocompletion.')

def mouse(theWindowName, theQuery):
	"""
	Query the mouse for events in a particular window. This function behave exactly like `cvui.mouse(int theQuery)`
	with the difference that queries are targeted at a particular window.

	Parameters
	----------
	theWindowName: str
		name of the window that will be queried.
	theQuery: int
		an integer describing the intended mouse query. Available queries are `cvui.DOWN`, `cvui.UP`, `cvui.CLICK`, and `cvui.IS_DOWN`.

	See Also
	----------
	mouse(str)
	mouse(str, int, int)
	mouse(int, int)
	mouse(int)
	"""
	print('This is wrapper function to help code autocompletion.')

def mouse(theButton, theQuery):
	"""
	Query the mouse for events in a particular button. This function behave exactly like `cvui.mouse(int theQuery)`,
	with the difference that queries are targeted at a particular mouse button instead.

	Parameters
	----------
	theButton: int
		an integer describing the mouse button to be queried. Possible values are `cvui.LEFT_BUTTON`, `cvui.MIDDLE_BUTTON` and `cvui.LEFT_BUTTON`.
	theQuery: int
		an integer describing the intended mouse query. Available queries are `cvui.DOWN`, `cvui.UP`, `cvui.CLICK`, and `cvui.IS_DOWN`.

	See Also
	----------
	mouse(str)
	mouse(str, int, int)
	mouse(int)
	"""
	print('This is wrapper function to help code autocompletion.')

def mouse(theWindowName, theButton, theQuery):
	"""
	Query the mouse for events in a particular button in a particular window. This function behave exactly
	like `cvui.mouse(int theButton, int theQuery)`, with the difference that queries are targeted at
	a particular mouse button in a particular window instead.

	Parameters
	----------
	theWindowName: str
		name of the window that will be queried.
	theButton: int
		an integer describing the mouse button to be queried. Possible values are `cvui.LEFT_BUTTON`, `cvui.MIDDLE_BUTTON` and `cvui.LEFT_BUTTON`.
	theQuery: int
		an integer describing the intended mouse query. Available queries are `cvui.DOWN`, `cvui.UP`, `cvui.CLICK`, and `cvui.IS_DOWN`.
	"""
	print('This is wrapper function to help code autocompletion.')

def button(theWhere, theX, theY, theLabel):
	"""
	Display a button. The size of the button will be automatically adjusted to
	properly house the label content.

	Parameters
	----------
	theWhere: np.ndarray
		image/frame where the component should be rendered.
	theX: int
		position X where the component should be placed.
	theY: int
		position Y where the component should be placed.
	theLabel: str
		text displayed inside the button.

	Returns
	----------
	`true` everytime the user clicks the button.
	"""
	print('This is wrapper function to help code autocompletion.')

def button(theWhere, theX, theY, theWidth, theHeight, theLabel):
	"""
	Display a button. The button size will be defined by the width and height parameters,
	no matter the content of the label.

	Parameters
	----------
	theWhere: np.ndarray
		image/frame where the component should be rendered.
	theX: int
		position X where the component should be placed.
	theY: int
		position Y where the component should be placed.
	theWidth: int
		width of the button.
	theHeight: int
		height of the button.
	theLabel: str
		text displayed inside the button.

	Returns
	----------
	`true` everytime the user clicks the button.
	"""
	print('This is wrapper function to help code autocompletion.')

def button(theWhere, theX, theY, theIdle, theOver, theDown):
	"""
	Display a button whose graphics are images (np.ndarray). The button accepts three images to describe its states,
	which are idle (no mouse interaction), over (mouse is over the button) and down (mouse clicked the button).
	The button size will be defined by the width and height of the images.

	Parameters
	----------
	theWhere: np.ndarray
		image/frame where the component should be rendered.
	theX: int
		position X where the component should be placed.
	theY: int
		position Y where the component should be placed.
	theIdle: np.ndarray
		an image that will be rendered when the button is not interacting with the mouse cursor.
	theOver: np.ndarray
		an image that will be rendered when the mouse cursor is over the button.
	theDown: np.ndarray
		an image that will be rendered when the mouse cursor clicked the button (or is clicking).

	Returns
	----------
	`true` everytime the user clicks the button.

	See Also
	----------
	button()
	image()
	iarea()
	"""
	print('This is wrapper function to help code autocompletion.')

def image(theWhere, theX, theY, theImage):
	"""
	Display an image (np.ndarray).

	Parameters
	----------
	theWhere: np.ndarray
		image/frame where the provded image should be rendered.
	theX: int
		position X where the image should be placed.
	theY: int
		position Y where the image should be placed.
	theImage: np.ndarray
		image to be rendered in the specified destination.

	See Also
	----------
	button()
	iarea()
	"""
	print('This is wrapper function to help code autocompletion.')

def checkbox(theWhere, theX, theY, theLabel, theState, theColor = 0xCECECE):
	"""
	Display a checkbox. You can use the state parameter to monitor if the
	checkbox is checked or not.

	Parameters
	----------
	theWhere: np.ndarray
		image/frame where the component should be rendered.
	theX: int
		position X where the component should be placed.
	theY: int
		position Y where the component should be placed.
	theLabel: str
		text displayed besides the clickable checkbox square.
	theState: [bool]
		array or list of booleans whose first position, i.e. theState[0], will be used to store the current state of the checkbox: `True` means the checkbox is checked.
	theColor: uint
		color of the label in the format `0xRRGGBB`, e.g. `0xff0000` for red.

	Returns
	----------
	a boolean value that indicates the current state of the checkbox, `true` if it is checked.
	"""
	print('This is wrapper function to help code autocompletion.')

def text(theWhere, theX, theY, theText, theFontScale = 0.4, theColor = 0xCECECE):
	"""
	Display a piece of text.

	Parameters
	----------
	theWhere: np.ndarray
		image/frame where the component should be rendered.
	theX: int
		position X where the component should be placed.
	theY: int
		position Y where the component should be placed.
	theText: str
		the text content.
	theFontScale: float
		size of the text.
	theColor: uint
		color of the text in the format `0xRRGGBB`, e.g. `0xff0000` for red.

	See Also
	----------
	printf()
	"""
	print('This is wrapper function to help code autocompletion.')

def printf(theWhere, theX, theY, theFontScale, theColor, theFmt):
	"""
	Display a piece of text that can be formated using `C stdio's printf()` style. For instance
	if you want to display text mixed with numbers, you can use:

	```
	printf(frame, 10, 15, 0.4, 0xff0000, 'Text: %d and %f', 7, 3.1415)
	```

	Parameters
	----------
	theWhere: np.ndarray
		image/frame where the component should be rendered.
	theX: int
		position X where the component should be placed.
	theY: int
		position Y where the component should be placed.
	theFontScale: float
		size of the text.
	theColor: uint
		color of the text in the format `0xRRGGBB`, e.g. `0xff0000` for red.
	theFmt: str
		formating string as it would be supplied for `stdio's printf()`, e.g. `'Text: %d and %f', 7, 3.1415`.

	See Also
	----------
	text()
	"""
	print('This is wrapper function to help code autocompletion.')

def printf(theWhere, theX, theY, theFmt):
	"""
	Display a piece of text that can be formated using `C stdio's printf()` style. For instance
	if you want to display text mixed with numbers, you can use:

	```
	printf(frame, 10, 15, 0.4, 0xff0000, 'Text: %d and %f', 7, 3.1415)
	```

	The size and color of the text will be based on cvui's default values.

	Parameters
	----------
	theWhere: np.ndarray
		image/frame where the component should be rendered.
	theX: int
		position X where the component should be placed.
	theY: int
		position Y where the component should be placed.
	theFmt: str
		formating string as it would be supplied for `stdio's printf()`, e.g. `'Text: %d and %f', 7, 3.1415`.

	See Also
	----------
	text()
	"""
	print('This is wrapper function to help code autocompletion.')

def counter(theWhere, theX, theY, theValue, theStep = 1, theFormat = '%d'):
	"""
	Display a counter for integer values that the user can increase/descrease
	by clicking the up and down arrows.

	Parameters
	----------
	theWhere: np.ndarray
		image/frame where the component should be rendered.
	theX: int
		position X where the component should be placed.
	theY: int
		position Y where the component should be placed.
	theValue: [number]
		array or list of numbers whose first position, i.e. theValue[0], will be used to store the current value of the counter.
	theStep: number
		amount that should be increased/decreased when the user interacts with the counter buttons
	theFormat: str
		how the value of the counter should be presented, as it was printed by `stdio's printf()`. E.g. `'%d'` means the value will be displayed as an integer, `'%0d'` integer with one leading zero, etc.

	Returns
	----------
	number that corresponds to the current value of the counter.
	"""
	print('This is wrapper function to help code autocompletion.')

def trackbar(theWhere, theX, theY, theWidth, theValue, theMin, theMax, theSegments = 1, theLabelFormat = '%.1Lf', theOptions = 0, theDiscreteStep = 1):
	"""
	Display a trackbar for numeric values that the user can increase/decrease
	by clicking and/or dragging the marker right or left. This component can use
	different types of data as its value, so it is imperative provide the right
	label format, e.g. '%d' for ints, otherwise you might end up with weird errors.

	Example:

	```
	# using float
	trackbar(where, x, y, width, &floatValue, 0.0, 50.0)

	# using float
	trackbar(where, x, y, width, &floatValue, 0.0f, 50.0f)

	# using char
	trackbar(where, x, y, width, &charValue, (char)1, (char)10)
	```

	Parameters
	----------
	theWhere: np.ndarray
		image/frame where the component should be rendered.
	theX: int
		position X where the component should be placed.
	theY: int
		position Y where the component should be placed.
	theWidth: int
		width of the trackbar.
	theValue: [number]
		array or list of numbers whose first position, i.e. theValue[0], will be used to store the current value of the trackbar. It will be modified when the user interacts with the trackbar. Any numeric type can be used, e.g. int, float, long double, etc.
	theMin: number
		minimum value allowed for the trackbar.
	theMax: number
		maximum value allowed for the trackbar.
	theSegments: int
		number of segments the trackbar will have (default is 1). Segments can be seen as groups of numbers in the scale of the trackbar. For example, 1 segment means a single groups of values (no extra labels along the scale), 2 segments mean the trackbar values will be divided in two groups and a label will be placed at the middle of the scale.
	theLabelFormat: str
		formating string that will be used to render the labels. If you are using a trackbar with integers values, for instance, you can use `%d` to render labels.
	theOptions: uint
		options to customize the behavior/appearance of the trackbar, expressed as a bitset. Available options are defined as `cvui.TRACKBAR_` constants and they can be combined using the bitwise `|` operand. Available options are: `TRACKBAR_HIDE_SEGMENT_LABELS` (do not render segment labels, but do render min/max labels), `TRACKBAR_HIDE_STEP_SCALE` (do not render the small lines indicating values in the scale), `TRACKBAR_DISCRETE` (changes of the trackbar value are multiples of theDiscreteStep param), `TRACKBAR_HIDE_MIN_MAX_LABELS` (do not render min/max labels), `TRACKBAR_HIDE_VALUE_LABEL` (do not render the current value of the trackbar below the moving marker), `TRACKBAR_HIDE_LABELS` (do not render labels at all).
	theDiscreteStep: number
		amount that the trackbar marker will increase/decrease when the marker is dragged right/left (if option TRACKBAR_DISCRETE is ON)

	Returns
	----------
	`true` when the value of the trackbar changed.

	See Also
	----------
	counter()
	"""
	print('This is wrapper function to help code autocompletion.')

def window(theWhere, theX, theY, theWidth, theHeight, theTitle):
	"""
	Display a window (a block with a title and a body).

	Parameters
	----------
	theWhere: np.ndarray
		image/frame where the component should be rendered.
	theX: int
		position X where the component should be placed.
	theY: int
		position Y where the component should be placed.
	theWidth: int
		width of the window.
	theHeight: int
		height of the window.
	theTitle: str
		text displayed as the title of the window.

	See Also
	----------
	rect()
	"""
	print('This is wrapper function to help code autocompletion.')

def rect(theWhere, theX, theY, theWidth, theHeight, theBorderColor, theFillingColor = 0xff000000):
	"""
	Display a filled rectangle.

	Parameters
	----------
	theWhere: np.ndarray
		image/frame where the component should be rendered.
	theX: int
		position X where the component should be placed.
	theY: int
		position Y where the component should be placed.
	theWidth: int
		width of the rectangle.
	theHeight: int
		height of the rectangle.
	theBorderColor: uint
		color of rectangle's border in the format `0xRRGGBB`, e.g. `0xff0000` for red.
	theFillingColor: uint
		color of rectangle's filling in the format `0xAARRGGBB`, e.g. `0x00ff0000` for red, `0xff000000` for transparent filling.

	See Also
	----------
	image()
	"""
	print('This is wrapper function to help code autocompletion.')

def sparkline(theWhere, theValues, theX, theY, theWidth, theHeight, theColor = 0x00FF00):
	"""
	Display the values of a vector as a sparkline.

	Parameters
	----------
	theWhere: np.ndarray
		image/frame where the component should be rendered.
	theValues: number[]
		array or list containing the numeric values to be used in the sparkline.
	theX: int
		position X where the component should be placed.
	theY: int
		position Y where the component should be placed.
	theWidth: int
		width of the sparkline.
	theHeight: int
		height of the sparkline.
	theColor: uint
		color of sparkline in the format `0xRRGGBB`, e.g. `0xff0000` for red.

	See Also
	----------
	trackbar()
	"""
	print('This is wrapper function to help code autocompletion.')

def iarea(theX, theY, theWidth, theHeight):
	"""
	Create an interaction area that reports activity with the mouse cursor.
	The tracked interactions are returned by the function and they are:

	`OUT` when the cursor is not over the iarea.
	`OVER` when the cursor is over the iarea.
	`DOWN` when the cursor is pressed over the iarea, but not released yet.
	`CLICK` when the cursor clicked (pressed and released) within the iarea.

	This function creates no visual output on the screen. It is intended to
	be used as an auxiliary tool to create interactions.

	Parameters
	----------
	theX: int
		position X where the interactive area should be placed.
	theY: int
		position Y where the interactive area should be placed.
	theWidth: int
		width of the interactive area.
	theHeight: int
		height of the interactive area.

	Returns
	----------
	integer value representing the current state of interaction with the mouse cursor. It can be `OUT` (cursor is not over the area), `OVER` (cursor is over the area), `DOWN` (cursor is pressed over the area, but not released yet) and `CLICK` (cursor clicked, i.e. pressed and released, within the area).

	See Also
	----------
	button()
	image()
	"""
	return __internal.iarea(theX, theY, theWidth, theHeight)

def beginRow(theWhere, theX, theY, theWidth = -1, theHeight = -1, thePadding = 0):
	"""
	Start a new row.

	One of the most annoying tasks when building UI is to calculate
	where each component should be placed on the screen. cvui has
	a set of methods that abstract the process of positioning
	components, so you don't have to think about assigning a
	X and Y coordinate. Instead you just add components and cvui
	will place them as you go.

	You use `beginRow()` to start a group of elements. After `beginRow()`
	has been called, all subsequent component calls don't have to specify
	the frame where the component should be rendered nor its position.
	The position of the component will be automatically calculated by cvui
	based on the components within the group. All components are placed
	side by side, from left to right.

	E.g.

	```
	beginRow(frame, x, y, width, height)
	text('test')
	button('btn')
	endRow()
	```

	Rows and columns can be nested, so you can create columns/rows within
	columns/rows as much as you want. It's important to notice that any
	component within `beginRow()` and `endRow()` *do not* specify the position
	where the component is rendered, which is also True for `beginRow()`.
	As a consequence, **be sure you are calling `beginRow(width, height)`
	when the call is nested instead of `beginRow(x, y, width, height)`**,
	otherwise cvui will throw an error.

	E.g.

	```
	beginRow(frame, x, y, width, height)
	text('test')
	button('btn')

	beginColumn()      # no frame nor x,y parameters here!
	text('column1')
	text('column2')
	endColumn()
	endRow()
	```

	Don't forget to call `endRow()` to finish the row, otherwise cvui will throw an error.

	Parameters
	----------
	theWhere: np.ndarray
		image/frame where the components within this block should be rendered.
	theX: int
		position X where the row should be placed.
	theY: int
		position Y where the row should be placed.
	theWidth: int
		width of the row. If a negative value is specified, the width of the row will be automatically calculated based on the content of the block.
	theHeight: int
		height of the row. If a negative value is specified, the height of the row will be automatically calculated based on the content of the block.
	thePadding: int
		space, in pixels, among the components of the block.

	See Also
	----------
	beginColumn()
	endRow()
	endColumn()
	"""
	print('This is wrapper function to help code autocompletion.')

def endRow():
	"""
	End a row. You must call this function only if you have previously called
	its counter part, the `beginRow()` function.

	See Also
	----------
	beginRow()
	beginColumn()
	endColumn()
	"""
	__internal.end(ROW)

def beginColumn(theWhere, theX, theY, theWidth = -1, theHeight = -1, thePadding = 0):
	"""
	Start a new column.

	One of the most annoying tasks when building UI is to calculate
	where each component should be placed on the screen. cvui has
	a set of methods that abstract the process of positioning
	components, so you don't have to think about assigning a
	X and Y coordinate. Instead you just add components and cvui
	will place them as you go.

	You use `beginColumn()` to start a group of elements. After `beginColumn()`
	has been called, all subsequent component calls don't have to specify
	the frame where the component should be rendered nor its position.
	The position of the component will be automatically calculated by cvui
	based on the components within the group. All components are placed
	below each other, from the top of the screen towards the bottom.

	E.g.

	```
	beginColumn(frame, x, y, width, height)
	text('test')
	button('btn')
	endColumn()
	```

	Rows and columns can be nested, so you can create columns/rows within
	columns/rows as much as you want. It's important to notice that any
	component within `beginColumn()` and `endColumn()` *do not* specify the position
	where the component is rendered, which is also True for `beginColumn()`.
	As a consequence, **be sure you are calling `beginColumn(width, height)`
	when the call is nested instead of `beginColumn(x, y, width, height)`**,
	otherwise cvui will throw an error.

	E.g.

	```
	beginColumn(frame, x, y, width, height)
	text('test')
	button('btn')

	beginRow()      # no frame nor x,y parameters here!
	text('column1')
	text('column2')
	endRow()
	endColumn()
	```

	Don't forget to call `endColumn()` to finish the column, otherwise cvui will throw an error.

	Parameters
	----------
	theWhere: np.ndarray
		image/frame where the components within this block should be rendered.
	theX: int
		position X where the row should be placed.
	theY: int
		position Y where the row should be placed.
	theWidth: int
		width of the column. If a negative value is specified, the width of the column will be automatically calculated based on the content of the block.
	theHeight: int
		height of the column. If a negative value is specified, the height of the column will be automatically calculated based on the content of the block.
	thePadding: int
		space, in pixels, among the components of the block.

	See Also
	----------
	beginRow()
	endColumn()
	endRow()
	"""
	print('This is wrapper function to help code autocompletion.')

def endColumn():
	"""
	End a column. You must call this function only if you have previously called
	its counter part, i.e. `beginColumn()`.

	See Also
	----------
	beginColumn()
	beginRow()
	endRow()
	"""
	__internal.end(COLUMN)

def beginRow(theWidth = -1, theHeight = -1, thePadding = 0):
	"""
	Start a row. This function behaves in the same way as `beginRow(frame, x, y, width, height)`,
	however it is suposed to be used within `begin*()/end*()` blocks since they require components
	not to inform frame nor x,y coordinates.

	IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

	Parameters
	----------
	theWidth: int
		width of the row. If a negative value is specified, the width of the row will be automatically calculated based on the content of the block.
	theHeight: int
		height of the row. If a negative value is specified, the height of the row will be automatically calculated based on the content of the block.
	thePadding: int
		space, in pixels, among the components of the block.

	See Also
	----------
	beginColumn()
	endRow()
	endColumn()
	"""
	print('This is wrapper function to help code autocompletion.')

def beginColumn(theWidth = -1, theHeight = -1, thePadding = 0):
	"""
	Start a column. This function behaves in the same way as `beginColumn(frame, x, y, width, height)`,
	however it is suposed to be used within `begin*()/end*()` blocks since they require components
	not to inform frame nor x,y coordinates.

	IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

	Parameters
	----------
	theWidth: int
		width of the column. If a negative value is specified, the width of the column will be automatically calculated based on the content of the block.
	theHeight: int
		height of the column. If a negative value is specified, the height of the column will be automatically calculated based on the content of the block.
	thePadding: int
		space, in pixels, among the components of the block.

	See Also
	----------
	beginColumn()
	endRow()
	endColumn()
	"""
	print('This is wrapper function to help code autocompletion.')

def space(theValue = 5):
	"""
	Add an arbitrary amount of space between components within a `begin*()` and `end*()` block.
	The function is aware of context, so if it is used within a `beginColumn()` and
	`endColumn()` block, the space will be vertical. If it is used within a `beginRow()`
	and `endRow()` block, space will be horizontal.

	IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

	Parameters
	----------
	theValue: int
		the amount of space to be added.

	See Also
	----------
	beginColumn()
	beginRow()
	endRow()
	endColumn()
	"""
	aBlock = __internal.topBlock()
	aSize = Size(theValue, theValue)

	__internal.updateLayoutFlow(aBlock, aSize)

def text(theText, theFontScale = 0.4, theColor = 0xCECECE):
	"""
	Display a piece of text within a `begin*()` and `end*()` block.

	IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

	Parameters
	----------
	theText: str
		text content.
	theFontScale: float
		size of the text.
	theColor: uint
		color of the text in the format `0xRRGGBB`, e.g. `0xff0000` for red.

	See Also
	----------
	printf()
	beginColumn()
	beginRow()
	endRow()
	endColumn()
	"""
	print('This is wrapper function to help code autocompletion.')

def button(theWidth, theHeight, theLabel):
	"""
	Display a button within a `begin*()` and `end*()` block.
	The button size will be defined by the width and height parameters,
	no matter the content of the label.

	IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

	Parameters
	----------
	theWidth: int
		width of the button.
	theHeight: int
		height of the button.
	theLabel: str
		text displayed inside the button. You can set shortcuts by pre-pending them with '&'

	Returns
	----------
	`true` everytime the user clicks the button.

	See Also
	----------
	beginColumn()
	beginRow()
	endRow()
	endColumn()
	"""
	print('This is wrapper function to help code autocompletion.')

def button(theLabel):
	"""
	Display a button within a `begin*()` and `end*()` block. The size of the button will be
	automatically adjusted to properly house the label content.

	IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

	Parameters
	----------
	theLabel: str
		text displayed inside the button. You can set shortcuts by pre-pending them with '&'

	Returns
	----------
	`true` everytime the user clicks the button.

	See Also
	----------
	beginColumn()
	beginRow()
	endRow()
	endColumn()
	"""
	print('This is wrapper function to help code autocompletion.')

def button(theIdle, theOver, theDown):
	"""
	Display a button whose graphics are images (np.ndarray).

	IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

	The button accepts three images to describe its states,
	which are idle (no mouse interaction), over (mouse is over the button) and down (mouse clicked the button).
	The button size will be defined by the width and height of the images.

	Parameters
	----------
	theIdle: np.ndarray
		image that will be rendered when the button is not interacting with the mouse cursor.
	theOver: np.ndarray
		image that will be rendered when the mouse cursor is over the button.
	theDown: np.ndarray
		image that will be rendered when the mouse cursor clicked the button (or is clicking).

	Returns
	----------
	`true` everytime the user clicks the button.

	See Also
	----------
	button()
	image()
	iarea()
	beginColumn()
	beginRow()
	endRow()
	endColumn()
	"""
	print('This is wrapper function to help code autocompletion.')

def image(theImage):
	"""
	Display an image (np.ndarray) within a `begin*()` and `end*()` block

	IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

	Parameters
	----------
	theImage: np.ndarray
		image to be rendered in the specified destination.

	See Also
	----------
	button()
	iarea()
	beginColumn()
	beginRow()
	endRow()
	endColumn()
	"""
	print('This is wrapper function to help code autocompletion.')

def checkbox(theLabel, theState, theColor = 0xCECECE):
	"""
	Display a checkbox within a `begin*()` and `end*()` block. You can use the state parameter
	to monitor if the checkbox is checked or not.

	IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

	Parameters
	----------
	theLabel: str
		text displayed besides the clickable checkbox square.
	theState: [bool]
		array or list of booleans whose first position, i.e. theState[0], will be used to store the current state of the checkbox: `True` means the checkbox is checked.
	theColor: uint
		color of the label in the format `0xRRGGBB`, e.g. `0xff0000` for red.

	Returns
	----------
	a boolean value that indicates the current state of the checkbox, `true` if it is checked.

	See Also
	----------
	beginColumn()
	beginRow()
	endRow()
	endColumn()
	"""
	print('This is wrapper function to help code autocompletion.')

def printf(theFontScale, theColor, theFmt):
	"""
	Display a piece of text within a `begin*()` and `end*()` block.

	IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

	The text can be formated using `C stdio's printf()` style. For instance if you want to display text mixed
	with numbers, you can use:

	```
	printf(0.4, 0xff0000, 'Text: %d and %f', 7, 3.1415)
	```

	Parameters
	----------
	theFontScale: float
		size of the text.
	theColor: uint
		color of the text in the format `0xRRGGBB`, e.g. `0xff0000` for red.
	theFmt: str
		formating string as it would be supplied for `C stdio's printf()`, e.g. `'Text: %d and %f', 7, 3.1415`.

	See Also
	----------
	text()
	beginColumn()
	beginRow()
	endRow()
	endColumn()
	"""
	print('This is wrapper function to help code autocompletion.')

def printf(theFmt):
	"""
	Display a piece of text that can be formated using `C stdio's printf()` style.

	IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

	For instance if you want to display text mixed with numbers, you can use:

	```
	printf(frame, 10, 15, 0.4, 0xff0000, 'Text: %d and %f', 7, 3.1415)
	```

	The size and color of the text will be based on cvui's default values.

	Parameters
	----------
	theFmt: str
		formating string as it would be supplied for `stdio's printf()`, e.g. `'Text: %d and %f', 7, 3.1415`.

	See Also
	----------
	text()
	beginColumn()
	beginRow()
	endRow()
	endColumn()
	"""
	print('This is wrapper function to help code autocompletion.')

def counter(theValue, theStep = 1, theFormat = '%d'):
	"""
	Display a counter for integer values that the user can increase/descrease
	by clicking the up and down arrows.

	IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

	Parameters
	----------
	theValue: [number]
		array or list of numbers whose first position, i.e. theValue[0], will be used to store the current value of the counter.
	theStep: number
		amount that should be increased/decreased when the user interacts with the counter buttons.
	theFormat: str
		how the value of the counter should be presented, as it was printed by `C stdio's printf()`. E.g. `'%d'` means the value will be displayed as an integer, `'%0d'` integer with one leading zero, etc.

	Returns
	----------
	number that corresponds to the current value of the counter.

	See Also
	----------
	printf()
	beginColumn()
	beginRow()
	endRow()
	endColumn()
	"""
	print('This is wrapper function to help code autocompletion.')

def trackbar(theWidth, theValue, theMin, theMax, theSegments = 1, theLabelFormat = '%.1Lf', theOptions = 0, theDiscreteStep = 1):
	"""
	Display a trackbar for numeric values that the user can increase/decrease
	by clicking and/or dragging the marker right or left.

	IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

	This component uses templates so it is imperative that you make it very explicit
	the type of `theValue`, `theMin`, `theMax` and `theStep`, otherwise you might end up with
	weird compilation errors.

	Example:

	```
	# using float
	trackbar(width, &floatValue, 0.0, 50.0)

	# using float
	trackbar(width, &floatValue, 0.0f, 50.0f)

	# using char
	trackbar(width, &charValue, (char)1, (char)10)
	```

	Parameters
	----------
	theWidth: int
		the width of the trackbar.
	theValue: [number]
		array or list of numbers whose first position, i.e. theValue[0], will be used to store the current value of the trackbar. It will be modified when the user interacts with the trackbar. Any numeric type can be used, e.g. int, float, long double, etc.
	theMin: number
		minimum value allowed for the trackbar.
	theMax: number
		maximum value allowed for the trackbar.
	theSegments: int
		number of segments the trackbar will have (default is 1). Segments can be seen as groups of numbers in the scale of the trackbar. For example, 1 segment means a single groups of values (no extra labels along the scale), 2 segments mean the trackbar values will be divided in two groups and a label will be placed at the middle of the scale.
	theLabelFormat: str
		formating string that will be used to render the labels, e.g. `%.2Lf`. No matter the type of the `theValue` param, internally trackbar stores it as a `long float`, so the formating string will *always* receive a `long float` value to format. If you are using a trackbar with integers values, for instance, you can supress decimals using a formating string as `%.0Lf` to format your labels.
	theOptions: uint
		options to customize the behavior/appearance of the trackbar, expressed as a bitset. Available options are defined as `TRACKBAR_` constants and they can be combined using the bitwise `|` operand. Available options are: `TRACKBAR_HIDE_SEGMENT_LABELS` (do not render segment labels, but do render min/max labels), `TRACKBAR_HIDE_STEP_SCALE` (do not render the small lines indicating values in the scale), `TRACKBAR_DISCRETE` (changes of the trackbar value are multiples of informed step param), `TRACKBAR_HIDE_MIN_MAX_LABELS` (do not render min/max labels), `TRACKBAR_HIDE_VALUE_LABEL` (do not render the current value of the trackbar below the moving marker), `TRACKBAR_HIDE_LABELS` (do not render labels at all).
	theDiscreteStep: number
		amount that the trackbar marker will increase/decrease when the marker is dragged right/left (if option TRACKBAR_DISCRETE is ON)

	Returns
	----------
	`true` when the value of the trackbar changed.

	See Also
	----------
	counter()
	beginColumn()
	beginRow()
	endRow()
	endColumn()
	"""
	print('This is wrapper function to help code autocompletion.')

def window(theWidth, theHeight, theTitle):
	"""
	Display a window (a block with a title and a body) within a `begin*()` and `end*()` block.

	IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

	Parameters
	----------
	theWidth: int
		width of the window.
	theHeight: int
		height of the window.
	theTitle: str
		text displayed as the title of the window.

	See Also
	----------
	rect()
	beginColumn()
	beginRow()
	endRow()
	endColumn()
	"""
	print('This is wrapper function to help code autocompletion.')

def rect(theWidth, theHeight, theBorderColor, theFillingColor = 0xff000000):
	"""
	Display a rectangle within a `begin*()` and `end*()` block.

	IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

	Parameters
	----------
	theWidth: int
		width of the rectangle.
	theHeight: int
		height of the rectangle.
	theBorderColor: uint
		color of rectangle's border in the format `0xRRGGBB`, e.g. `0xff0000` for red.
	theFillingColor: uint
		color of rectangle's filling in the format `0xAARRGGBB`, e.g. `0x00ff0000` for red, `0xff000000` for transparent filling.

	See Also
	----------
	window()
	beginColumn()
	beginRow()
	endRow()
	endColumn()
	"""
	print('This is wrapper function to help code autocompletion.')

def sparkline(theValues, theWidth, theHeight, theColor = 0x00FF00):
	"""
	Display the values of a vector as a sparkline within a `begin*()` and `end*()` block.

	IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

	Parameters
	----------
	theValues: number[]
		array or list of numeric values that will be rendered as a sparkline.
	theWidth: int
		width of the sparkline.
	theHeight: int
		height of the sparkline.
	theColor: uint
		color of sparkline in the format `0xRRGGBB`, e.g. `0xff0000` for red.

	See Also
	----------
	beginColumn()
	beginRow()
	endRow()
	endColumn()
	"""
	print('This is wrapper function to help code autocompletion.')

def update(theWindowName = ''):
	"""
	Update the library internal things. You need to call this function **AFTER** you are done adding/manipulating
	UI elements in order for them to react to mouse interactions.

	Parameters
	----------
	theWindowName: str
		name of the window whose components are being updated. If no window name is provided, cvui uses the default window.

	See Also
	----------
	init()
	watch()
	context()
	"""
	aContext = __internal.getContext(theWindowName)

	aContext.mouse.anyButton.justReleased = False
	aContext.mouse.anyButton.justPressed  = False

	for i in range(LEFT_BUTTON, RIGHT_BUTTON + 1):
		aContext.mouse.buttons[i].justReleased = False
		aContext.mouse.buttons[i].justPressed  = False

	__internal.screen.reset()

	# If we were told to keep track of the keyboard shortcuts, we
	# proceed to handle opencv event queue.
	if __internal.delayWaitKey > 0:
		__internal.lastKeyPressed = cv2.waitKey(__internal.delayWaitKey)

	if __internal.blockStackEmpty() == False:
		__internal.error(2, 'Calling update() before finishing all begin*()/end*() calls. Did you forget to call a begin*() or an end*()? Check if every begin*() has an appropriate end*() call before you call update().')

def init(*theArgs):
	if __internal.isString(theArgs[0]):
		# Signature: init(theWindowName, theDelayWaitKey = -1, theCreateNamedWindow = True)
		aWindowName = theArgs[0]
		aDelayWaitKey = theArgs[1] if len(theArgs) >= 2 else -1
		aCreateNamedWindow = theArgs[2] if len(theArgs) >= 3 else True

		__internal.init(aWindowName, aDelayWaitKey)
		watch(aWindowName, aCreateNamedWindow)
	else:
		# Signature: init(theWindowNames[], theHowManyWindows, theDelayWaitKey = -1, theCreateNamedWindows = True)
		aWindowNames = theArgs[0]
		aHowManyWindows = theArgs[1]
		aDelayWaitKey = theArgs[2] if len(theArgs) >= 3 else -1
		aCreateNamedWindows = theArgs[3] if len(theArgs) >= 4 else True

		__internal.init(aWindowNames[0], aDelayWaitKey)

		for i in range(0, aHowManyWindows):
			watch(aWindowNames[i], aCreateNamedWindows)

def text(*theArgs):
	if isinstance(theArgs[0], np.ndarray):
		# Signature: text(theWhere, theX, theY, theText, theFontScale = 0.4, theColor = 0xCECECE)
		aWhere = theArgs[0]
		aX = theArgs[1]
		aY = theArgs[2]
		aText = theArgs[3]
		aFontScale = theArgs[4] if len(theArgs) >= 5 else 0.4
		aColor = theArgs[5] if len(theArgs) >= 6 else 0xCECECE

		__internal.screen.where = aWhere
		aBlock = __internal.screen
	else:
		# Signature: text(theText, theFontScale = 0.4, theColor = 0xCECECE)
		aBlock = __internal.topBlock()
		aX = aBlock.anchor.x
		aY = aBlock.anchor.y
		aText = theArgs[0]
		aFontScale = theArgs[1] if len(theArgs) >= 2 else 0.4
		aColor = theArgs[2] if len(theArgs) >= 3 else 0xCECECE

	__internal.text(aBlock, aX, aY, aText, aFontScale, aColor, True)

def printf(*theArgs):
	if isinstance(theArgs[0], np.ndarray):
		# Signature: printf(theWhere, theX, theY, ...)
		aWhere = theArgs[0]
		aX = theArgs[1]
		aY = theArgs[2]

		__internal.screen.where = aWhere
		aBlock = __internal.screen

		aArgs = theArgs[3:]
	else:
		# Row/column function
		aBlock = __internal.topBlock()
		aX = aBlock.anchor.x
		aY = aBlock.anchor.y
		aArgs = theArgs

	if __internal.isString(aArgs[0]):
		# Signature: printf(theWhere, theX, theY, theFmt, ...)
		aFontScale = 0.4
		aColor = 0xCECECE
		aFmt = aArgs[0]
		aFmtArgs = aArgs[1:]
	else:
		# Signature: printf(theWhere, theX, theY, theFontScale, theColor, theFmt, ...)
		aFontScale = aArgs[0]
		aColor = aArgs[1]
		aFmt = aArgs[2]
		aFmtArgs = aArgs[3:]

	aText = aFmt % aFmtArgs
	__internal.text(aBlock, aX, aY, aText, aFontScale, aColor, True)

def counter(*theArgs):
	if isinstance(theArgs[0], np.ndarray):
		# Signature: counter(theWhere, theX, theY, theValue, theStep = 1, theFormat = "")
		aWhere = theArgs[0]
		aX = theArgs[1]
		aY = theArgs[2]
		aValue = theArgs[3]
		aStep = theArgs[4] if len(theArgs) >= 5 else 1
		aFormat = theArgs[5] if len(theArgs) >= 6 else ''

		__internal.screen.where = aWhere
		aBlock = __internal.screen
	else:
		# Signature: counter(theValue, theStep = 1, theFormat = "%d")
		aBlock = __internal.topBlock()
		aX = aBlock.anchor.x
		aY = aBlock.anchor.y
		aValue = theArgs[0]
		aStep = theArgs[1] if len(theArgs) >= 2 else 1
		aFormat = theArgs[2] if len(theArgs) >= 3 else ''

	if not aFormat:
		aIsInt = isinstance(aValue[0], int) == True and isinstance(aStep, int)
		aFormat = '%d' if aIsInt else '%.1f'

	return __internal.counter(aBlock, aX, aY, aValue, aStep, aFormat)

def checkbox(*theArgs):
	if isinstance(theArgs[0], np.ndarray):
		# Signature: checkbox(theWhere, theX, theY, theLabel, theState, theColor = 0xCECECE)
		aWhere = theArgs[0]
		aX = theArgs[1]
		aY = theArgs[2]
		aLabel = theArgs[3]
		aState = theArgs[4]
		aColor = theArgs[5] if len(theArgs) >= 6 else 0xCECECE

		__internal.screen.where = aWhere
		aBlock = __internal.screen
	else:
		# Signature: checkbox(theLabel, theState, theColor = 0xCECECE)
		aBlock = __internal.topBlock()
		aX = aBlock.anchor.x
		aY = aBlock.anchor.y
		aLabel = theArgs[0]
		aState = theArgs[1]
		aColor = theArgs[2] if len(theArgs) >= 3 else 0xCECECE

	return __internal.checkbox(aBlock, aX, aY, aLabel, aState, aColor)

def mouse(*theArgs):
	if len(theArgs) == 3:
		# Signature: mouse(theWindowName, theButton, theQuery)
		aWindowName = theArgs[0]
		aButton = theArgs[1]
		aQuery = theArgs[2]
		return __internal.mouseWBQ(aWindowName, aButton, aQuery)
	elif len(theArgs) == 2:
		# Signatures: mouse(theWindowName, theQuery) or mouse(theButton, theQuery)
		if __internal.isString(theArgs[0]):
			# Signature: mouse(theWindowName, theQuery)
			aWindowName = theArgs[0]
			aQuery = theArgs[1]
			return __internal.mouseWQ(aWindowName, aQuery)
		else:
			# Signature: mouse(theButton, theQuery)
			aButton = theArgs[0]
			aQuery = theArgs[1]
			return __internal.mouseBQ(aButton, aQuery)
	elif len(theArgs) == 1 and isinstance(theArgs[0], int):
		# Signature: mouse(theQuery)
		aQuery = theArgs[0]
		return __internal.mouseQ(aQuery)
	else:
		# Signature: mouse(theWindowName = '')
		aWindowName = theArgs[0] if len(theArgs) == 1 else ''
		return __internal.mouseW(aWindowName)

def button(*theArgs):
	if isinstance(theArgs[0], np.ndarray) and isinstance(theArgs[1], np.ndarray) == False:
		# Signature: button(Mat, theX, theY, ...)
		aWhere = theArgs[0]
		aX = theArgs[1]
		aY = theArgs[2]

		__internal.screen.where = aWhere
		aBlock = __internal.screen

		aArgs = theArgs[3:]
	else:
		# Row/column function
		aBlock = __internal.topBlock()
		aX = aBlock.anchor.x
		aY = aBlock.anchor.y
		aArgs = theArgs

	if len(aArgs) == 1:
		# Signature: button(theLabel)
		aLabel = aArgs[0]
		return __internal.button(aBlock, aX, aY, aLabel)

	elif len(aArgs) == 3:
		if isinstance(aArgs[0], int):
			# Signature: button(theWidth, theHeight, theLabel)
			aWidth = aArgs[0]
			aHeight = aArgs[1]
			aLabel = aArgs[2]
			return __internal.buttonWH(aBlock, aX, aY, aWidth, aHeight, aLabel, True)
		else:
			# Signature: button(theIdle, theOver, theDown)
			aIdle = aArgs[0]
			aOver = aArgs[1]
			aDown= aArgs[2]
			return __internal.buttonI(aBlock, aX, aY, aIdle, aOver, aDown, True)
	else:
		# TODO: check this case here
		print('Problem?')

def image(*theArgs):
	if isinstance(theArgs[0], np.ndarray) and len(theArgs) > 1:
		# Signature: image(Mat, ...)
		aWhere = theArgs[0]
		aX = theArgs[1]
		aY = theArgs[2]
		aImage = theArgs[3]

		__internal.screen.where = aWhere
		__internal.image(__internal.screen, aX, aY, aImage)
	else:
		# Row/column function, signature is image(...)
		aImage = theArgs[0]
		aBlock = __internal.topBlock()

		__internal.image(aBlock, aBlock.anchor.x, aBlock.anchor.y, aImage)

def trackbar(*theArgs):
	# TODO: re-factor this two similar blocks by slicing theArgs into aArgs
	if isinstance(theArgs[0], np.ndarray):
		# Signature: trackbar(theWhere, theX, theY, theWidth, theValue, theMin, theMax, theSegments = 1, theLabelFormat = "%.1Lf", theOptions = 0, theDiscreteStep = 1)
		aWhere = theArgs[0]
		aX = theArgs[1]
		aY = theArgs[2]
		aWidth = theArgs[3]
		aValue = theArgs[4]
		aMin = theArgs[5]
		aMax = theArgs[6]
		aSegments = theArgs[7] if len(theArgs) >= 8 else 1
		aLabelFormat = theArgs[8] if len(theArgs) >= 9 else '%.1Lf'
		aOptions = theArgs[9] if len(theArgs) >= 10 else 0
		aDiscreteStep = theArgs[10] if len(theArgs) >= 11 else 1

		__internal.screen.where = aWhere
		aBlock = __internal.screen
	else:
		# Signature: trackbar(theWidth, theValue, theMin, theMax, theSegments = 1, theLabelFormat = "%.1Lf", theOptions = 0, theDiscreteStep = 1)
		aBlock = __internal.topBlock()
		aX = aBlock.anchor.x
		aY = aBlock.anchor.y
		aWidth = theArgs[0]
		aValue = theArgs[1]
		aMin = theArgs[2]
		aMax = theArgs[3]
		aSegments = theArgs[4] if len(theArgs) >= 5 else 1
		aLabelFormat = theArgs[5] if len(theArgs) >= 6 else '%.1Lf'
		aOptions = theArgs[6] if len(theArgs) >= 7 else 0
		aDiscreteStep = theArgs[7] if len(theArgs) >= 8 else 1

	# TODO: adjust aLabelFormat based on type of aValue
	aParams = TrackbarParams(aMin, aMax, aDiscreteStep, aSegments, aLabelFormat, aOptions)
	aResult = __internal.trackbar(aBlock, aX, aY, aWidth, aValue, aParams)

	return aResult

def window(*theArgs):
	if isinstance(theArgs[0], np.ndarray):
		# Signature: window(theWhere, theX, theY, theWidth, theHeight, theTitle)
		aWhere = theArgs[0]
		aX = theArgs[1]
		aY = theArgs[2]
		aWidth = theArgs[3]
		aHeight = theArgs[4]
		aTitle = theArgs[5]

		__internal.screen.where = aWhere
		__internal.window(__internal.screen, aX, aY, aWidth, aHeight, aTitle)
	else:
		# Row/column function, signature: window(theWidth, theHeight, theTitle)
		aWidth = theArgs[0]
		aHeight = theArgs[1]
		aTitle = theArgs[2]

		aBlock = __internal.topBlock()
		__internal.window(aBlock, aBlock.anchor.x, aBlock.anchor.y, aWidth, aHeight, aTitle)

def rect(*theArgs):
	if isinstance(theArgs[0], np.ndarray):
		# Signature: rect(theWhere, theX, theY, theWidth, theHeight, theBorderColor, theFillingColor = 0xff000000)
		aWhere = theArgs[0]
		aX = theArgs[1]
		aY = theArgs[2]
		aWidth = theArgs[3]
		aHeight = theArgs[4]
		aBorderColor = theArgs[5]
		aFillingColor = theArgs[6] if len(theArgs) >= 7 else 0xff000000

		__internal.screen.where = aWhere
		aBlock = __internal.screen
	else:
		# Signature: rect(theWidth, theHeight, theBorderColor, theFillingColor = 0xff000000)
		aBlock = __internal.topBlock()
		aX = aBlock.anchor.x
		aY = aBlock.anchor.y
		aWidth = theArgs[0]
		aHeight = theArgs[1]
		aBorderColor = theArgs[2]
		aFillingColor = theArgs[3] if len(theArgs) >= 4 else 0xff000000

	__internal.rect(aBlock, aX, aY, aWidth, aHeight, aBorderColor, aFillingColor)

def sparkline(*theArgs):
	if isinstance(theArgs[0], np.ndarray):
		# Signature: sparkline(theWhere, theValues, theX, theY, theWidth, theHeight, theColor = 0x00FF00)
		aWhere = theArgs[0]
		aValues = theArgs[1]
		aX = theArgs[2]
		aY = theArgs[3]
		aWidth = theArgs[4]
		aHeight = theArgs[5]
		aColor = theArgs[6] if len(theArgs) >= 7 else 0x00FF00

		__internal.screen.where = aWhere
		aBlock = __internal.screen
	else:
		# Signature: sparkline(theValues, theWidth, theHeight, theColor = 0x00FF00)
		aBlock = __internal.topBlock()
		aValues = theArgs[0]
		aX = aBlock.anchor.x
		aY = aBlock.anchor.y
		aWidth = theArgs[1]
		aHeight = theArgs[2]
		aColor = theArgs[3] if len(theArgs) >= 4 else 0x00FF00

	__internal.sparkline(aBlock, aValues, aX, aY, aWidth, aHeight, aColor)

def beginRow(*theArgs):
	if len(theArgs) and isinstance(theArgs[0], np.ndarray):
		# Signature: beginRow(theWhere, theX, theY, theWidth = -1, theHeight = -1, thePadding = 0):
		aWhere = theArgs[0]
		aX = theArgs[1]
		aY = theArgs[2]
		aWidth = theArgs[3] if len(theArgs) >= 4 else -1
		aHeight = theArgs[4] if len(theArgs) >= 5 else -1
		aPadding = theArgs[5] if len(theArgs) >= 6 else 0

		__internal.begin(ROW, aWhere, aX, aY, aWidth, aHeight, aPadding)
	else:
		# Signature: beginRow(theWidth = -1, theHeight = -1, thePadding = 0)
		aWidth = theArgs[0] if len(theArgs) >= 1 else -1
		aHeight = theArgs[1] if len(theArgs) >= 2 else -1
		aPadding = theArgs[2] if len(theArgs) >= 3 else 0

		aBlock = __internal.topBlock()
		__internal.begin(ROW, aBlock.where, aBlock.anchor.x, aBlock.anchor.y, aWidth, aHeight, aPadding)

def beginColumn(*theArgs):
	if len(theArgs) > 0 and isinstance(theArgs[0], np.ndarray):
		# Signature: beginColumn(theWhere, theX, theY, theWidth = -1, theHeight = -1, thePadding = 0):
		aWhere = theArgs[0]
		aX = theArgs[1]
		aY = theArgs[2]
		aWidth = theArgs[3] if len(theArgs) >= 4 else -1
		aHeight = theArgs[4] if len(theArgs) >= 5 else -1
		aPadding = theArgs[5] if len(theArgs) >= 6 else 0

		__internal.begin(COLUMN, aWhere, aX, aY, aWidth, aHeight, aPadding)
	else:
		# Signature: beginColumn(theWidth = -1, theHeight = -1, thePadding = 0):
		aWidth = theArgs[0] if len(theArgs) >= 1 else -1
		aHeight = theArgs[1] if len(theArgs) >= 2 else -1
		aPadding = theArgs[2] if len(theArgs) >= 3 else 0

		aBlock = __internal.topBlock()
		__internal.begin(COLUMN, aBlock.where, aBlock.anchor.x, aBlock.anchor.y, aWidth, aHeight, aPadding)
