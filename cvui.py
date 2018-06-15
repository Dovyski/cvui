# This is a documentation block with several lines
# so I can test how it works.

import cv2
import numpy as np
import sys

def main():
	# TODO: make something here?
	return 0

if __name__ == '__main__':
    main()

# Lib version
VERSION = '2.5.0'

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

CVUI_ANTIALISED = cv2.LINE_AA
CVUI_FILLED = -1

# Internal things
_IS_PY2 = sys.version_info.major == 2

# Class to represent 2D points
class Point:
	def __init__(self, theX = 0, theY = 0):
		self.x = theX
		self.y = theY

# Class to represent a rectangle
class Rect:
	def __init__(self, theX = 0, theY = 0, theWidth = 0, theHeight = 0):
		self.x = theX
		self.y = theY
		self.width = theWidth
		self.height = theHeight
	
	def contains(self, thePoint):
		return thePoint.x >= self.x and thePoint.x <= (self.x + self.width) and thePoint.y >= self.y and thePoint.y <= (self.y + self.height)

# Class to represent the size of something, i.e. width and height.
# The class is a simplified version of Rect where x and y are zero.
class Size(Rect):
	def __init__(self, theWidth = 0, theHeight = 0):
		self.x = 0
		self.y = 0
		self.width = theWidth
		self.height = theHeight

# Describes the block structure used by the lib to handle `begin*()` and `end*()` calls.
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

# Describes a component label, including info about a shortcut.
# If a label contains "Re&start", then:
# - hasShortcut will be true
# - shortcut will be 's'
# - textBeforeShortcut will be "Re"
# - textAfterShortcut will be "tart"
class Label:
    __slots__ = [
        'hasShortcut',
        'shortcut',
        'textBeforeShortcut',
        'textAfterShortcut'
    ]

# Describe a mouse button
class MouseButton:
	justReleased = False               # if the mouse button was released, i.e. click event.
	justPressed = False                # if the mouse button was just pressed, i.e. true for a frame when a button is down.
	pressed = False                    # if the mouse button is pressed or not.

	def reset(self):
		self.justPressed = False
		self.justReleased = False
		self.pressed = False

# Describe the information of the mouse cursor
class Mouse:
    buttons = {                        # status of each button. Use cvui.{RIGHT,LEFT,MIDDLE}_BUTTON to access the buttons.
		LEFT_BUTTON: MouseButton(),
		MIDDLE_BUTTON: MouseButton(),
		RIGHT_BUTTON: MouseButton()
	}              
    anyButton = MouseButton()          # represent the behavior of all mouse buttons combined
    position = Point(0, 0)             # x and y coordinates of the mouse at the moment.

# Describes a (window) context.
class Context:
	windowName = '',                   # name of the window related to this context.
	mouse = Mouse()                    # the mouse cursor related to this context.

# This class contains all stuff that cvui uses internally to render
# and control interaction with components
class Internal:
	_render = None

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
		return mouseWBQ('', theButton, theQuery)

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
		aStartPoint = (theShape.x, theShape.y)
		aEndPoint = (theShape.x + theShape.width, theShape.y + theShape.height)

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
		cv2.putText(theBlock.where, theText, (aPositionDecentered.x, aPositionDecentered.y), cv2.FONT_HERSHEY_SIMPLEX, aFontScale, (0xCE, 0xCE, 0xCE), 1, CVUI_ANTIALISED)

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
		cv2.putText(theBlock.where, theTitle, (aPos.x, aPos.y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0xCE, 0xCE, 0xCE), 1, CVUI_ANTIALISED)

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
		aGap = theRect.width / aSize
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

# Access points to internal namespaces.
# TODO: re-factor this and make it less ugly.
__internal = Internal()
__render = Render()
__internal._render = __render
__render._internal = __internal

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

def watch(theWindowName, theDelayWaitKey = -1, theCreateNamedWindow = True):
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

def init(theWindowName, theDelayWaitKey = -1, theCreateNamedWindow = True):
    """
    Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    int
        Description of return value

    """
    __internal.init(theWindowName, theDelayWaitKey)
    watch(theWindowName, theCreateNamedWindow)

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

def counter(theWhere, theX, theY, theValue, theStep = 1, theFormat = "%d"):
	"""
	Display a counter for integer values that the user can increase/descrease
	by clicking the up and down arrows.

	Parameters
    ----------
	\param theWhere the image/frame where the component should be rendered.
	\param theX position X where the component should be placed.
	\param theY position Y where the component should be placed.
	\param theValue the current value of the counter.
	\param theStep the amount that should be increased/decreased when the user interacts with the counter buttons
	\param theFormat how the value of the counter should be presented, as it was printed by `stdio's printf()`. E.g. `"%d"` means the value will be displayed as an integer, `"%0d"` integer with one leading zero, etc.
	
	Returns
    -------
    int
		Integer corresponding to the current value of the counter.
	"""
	__internal.screen.where = theWhere
	return __internal.counter(__internal.screen, theX, theY, theValue, theStep, theFormat)

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
	"""
	Display an image (cv::Mat). 

	\param theWhere the image/frame where the provded image should be rendered.
	\param theX position X where the image should be placed.
	\param theY position Y where the image should be placed.
	\param theImage an image to be rendered in the specified destination.

	\sa button()
	\sa iarea()
	"""
	if isinstance(theArgs[0], np.ndarray) and len(theArgs) > 1:
		# Signature: image(Mat, ...)
		aWhere = theArgs[0]
		aX = theArgs[1]
		aY = theArgs[2]
		aImage = theArgs[3]

		__internal.screen.where = aWhere
		__internal.image(__internal.screen, theX, theY, theImage)
	else:
		# Row/column function, signature is image(...)
		aImage = theArgs[0]
		aBlock = __internal.topBlock()
		
		__internal.image(aBlock, aBlock.anchor.x, aBlock.anchor.y, aImage)

def window(*theArgs):
	"""
	Display a window (a block with a title and a body).

	Parameters
    ----------
	\param theWhere the image/frame where the component should be rendered.
	\param theX position X where the component should be placed.
	\param theY position Y where the component should be placed.
	\param theWidth width of the window.
	\param theHeight height of the window.
	\param theTitle text displayed as the title of the window.

	\sa rect()
	"""
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
	"""
	Display the values of a vector as a sparkline.

	\param theWhere the image/frame where the component should be rendered.
	\param theValues a vector containing the values to be used in the sparkline.
	\param theX position X where the component should be placed.
	\param theY position Y where the component should be placed.
	\param theWidth width of the sparkline.
	\param theHeight height of the sparkline.
	\param theColor color of sparkline in the format `0xRRGGBB`, e.g. `0xff0000` for red.

	\sa trackbar()
	"""
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

def iarea(theX, theY, theWidth, theHeight):
	return __internal.iarea(theX, theY, theWidth, theHeight)	

def beginRow(*theArgs):
	if isinstance(theArgs[0], np.ndarray):
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
	if isinstance(theArgs[0], np.ndarray):
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

def endRow():
	__internal.end(ROW)
	
def endColumn():
	__internal.end(COLUMN)

def space(theValue):
	aBlock = __internal.topBlock()
	aSize = Size(theValue, theValue)

	__internal.updateLayoutFlow(aBlock, aSize)

def update(theWindowName = ""):
	"""
	Updates the library internal things. You need to call this function **AFTER** you are done adding/manipulating
	UI elements in order for them to react to mouse interactions.

	Parameters
    ----------
	theWindowName : str
		Name of the window whose components are being updated. If no window name is provided, cvui uses the default window.

	\sa init()
	\sa watch()
	\sa context()
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

def imshow(theWindowName, theFrame):
	update(theWindowName)
	cv2.imshow(theWindowName, theFrame)