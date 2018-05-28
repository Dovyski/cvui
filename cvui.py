# This is a documentation block with several lines
# so I can test how it works.

import cv2
import numpy as np
import sys

def main():
      print("cvui main")

if __name__ == '__main__':
    main()

# Lib version
VERSION = "2.5.0"

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

# Describes the block structure used by the lib to handle `begin*()` and `end*()` calls.
class Block:
	def __init__(self):
		self.where = None           # where the block should be rendered to.
		self.rect = Rect()      # the size and position of the block.
		self.fill = Rect()      # the filled area occuppied by the block as it gets modified by its inner components.
		self.anchor = Point()       # the point where the next component of the block should be rendered.
		self.padding = 0            # padding among components within this block.
		self.type = ROW       		# type of the block, e.g. ROW or COLUMN.
		
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
	justReleased = False    # if the mouse button was released, i.e. click event.
	justPressed = False     # if the mouse button was just pressed, i.e. true for a frame when a button is down.
	pressed = False         # if the mouse button is pressed or not.

	def reset(self):
		self.justPressed = False
		self.justReleased = False
		self.pressed = False

# Describe the information of the mouse cursor
class Mouse:
    buttons = {                        # status of each button. Use cvui::{RIGHT,LEFT,MIDDLE}_BUTTON to access the buttons.
		LEFT_BUTTON: MouseButton(),
		MIDDLE_BUTTON: MouseButton(),
		RIGHT_BUTTON: MouseButton()
	}              
    anyButton = MouseButton()          # represent the behavior of all mouse buttons combined
    position = Point(0, 0)             # x and y coordinates of the mouse at the moment.

# Describes a (window) context.
class Context:
	windowName = '',       # name of the window related to this context.
	mouse = Mouse()        # the mouse cursor related to this context.

# This class contains all stuff that cvui uses internally to render
# and control interaction with components
class Internal:
	_render = None

	def __init__(self):
		self.defaultContext = ''
		self.currentContext = ''
		self.contexts = {} # indexed by the window name.
		self.buffer = []
		self.lastKeyPressed = -1 # TODO: collect it per window
		self.delayWaitKey = -1
		self.screen = Block()
		self.stack = []
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

	def init(self, theWindowName, theDelayWaitKey):
		self.defaultContext = theWindowName
		self.currentContext = theWindowName
		self.delayWaitKey = theDelayWaitKey
		self.lastKeyPressed = -1

	def error(self, theId, theMessage):
		print('[CVUI] Fatal error (code ', theId, '): ', theMessage)
		cv.waitKey(100000)
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
			self.error(5, "Unable to read context. Did you forget to call cvui::init()?")

	def updateLayoutFlow(self, theBlock, theSize):
		aValue = 0

		if theBlock.type == ROW:
			aValue = theSize.width + theBlock.padding;

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

	def text(self, theBlock, theX, theY, theText, theFontScale, theColor, theUpdateLayout):
		aSizeInfo, aBaseline = cv2.getTextSize(theText, cv2.FONT_HERSHEY_SIMPLEX, theFontScale, 1)
		
		aTextSize = Rect(0, 0, aSizeInfo[0], aSizeInfo[1])
		aPos = Point(theX, theY + aTextSize.height)

		self._render.text(theBlock, theText, aPos, theFontScale, theColor)

		if theUpdateLayout:
			# Add an extra pixel to the height to overcome OpenCV font size problems.
			aTextSize.height += 1
			self.updateLayoutFlow(theBlock, aTextSize)

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
		aSize = Rect(aHitArea.width, aHitArea.height)
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

	def rect(self, theBlock, theX, theY, theWidth, theHeight, theBorderColor, theFillingColor):
		aAnchor = Point(theX, theY);
		aRect = Rect(theX, theY, theWidth, theHeight);
		
		aRect.x = aAnchor.x + aRect.width if aRect.width < 0 else aAnchor.x
		aRect.y = aAnchor.y + aRect.height if aRect.height < 0 else aAnchor.y
		aRect.width = abs(aRect.width)
		aRect.height = abs(aRect.height)

		self._render.rect(theBlock, aRect, theBorderColor, theFillingColor)

		# Update the layout flow
		aSize = Rect(aRect.width, aRect.height)
		self.updateLayoutFlow(theBlock, aSize)

	def hexToScalar(self, theColor):
		aAlpha = (theColor >> 24) & 0xff
		aRed = (theColor >> 16) & 0xff
		aGreen = (theColor >> 8) & 0xff
		aBlue = theColor & 0xff

		return (aBlue, aGreen, aRed, aAlpha)

	def isString(self, theObj):
		return isinstance(theObj, basestring if _IS_PY2 else str)

# Class that contains all rendering methods.
class Render:
	_internal = None

	def text(self, theBlock, theText, thePos, theFontScale, theColor):
		aPosition = (int(thePos.x), int(thePos.y))
		cv2.putText(theBlock.where, theText, aPosition, cv2.FONT_HERSHEY_SIMPLEX, theFontScale, self._internal.hexToScalar(theColor), 1, cv2.LINE_AA)

	def checkbox(self, theBlock, theState, theShape):
		# Outline
		cv2.rectangle(theBlock.where, (theShape.x, theShape.y), (theShape.x + theShape.width, theShape.y + theShape.height), (0x63, 0x63, 0x63) if theState == OUT else (0x80, 0x80, 0x80))

		# Border
		theShape.x += 1
		theShape.y+=1
		theShape.width -= 2
		theShape.height -= 2
		cv2.rectangle(theBlock.where, (theShape.x, theShape.y), (theShape.x + theShape.width, theShape.y + theShape.height), (0x17, 0x17, 0x17))

		# Inside
		theShape.x += 1
		theShape.y += 1
		theShape.width -= 2
		theShape.height -= 2
		cv2.rectangle(theBlock.where, (theShape.x, theShape.y), (theShape.x + theShape.width, theShape.y + theShape.height), (0x29, 0x29, 0x29), CVUI_FILLED)
		
	def checkboxLabel(self, theBlock, theRect, theLabel, theTextSize, theColor):
		aPos = Point(theRect.x + theRect.width + 6, theRect.y + theTextSize.height + theRect.height / 2 - theTextSize.height / 2 - 1)
		self.text(theBlock, theLabel, aPos, 0.4, theColor)
		
	def checkboxCheck(self, theBlock, theShape):
		theShape.x += 1
		theShape.y += 1
		theShape.width -= 2
		theShape.height -= 2
		cv2.rectangle(theBlock.where, (theShape.x, theShape.y), (theShape.x + theShape.width, theShape.y + theShape.height), (0xFF, 0xBF, 0x75), CVUI_FILLED)

	def rect(self, theBlock, thePos, theBorderColor, theFillingColor):
		aBorder = self._internal.hexToScalar(theBorderColor)
		aFilling = self._internal.hexToScalar(theFillingColor)

		aHasFilling = aFilling[3] != 0xff

		if aHasFilling:
			cv2.rectangle(theBlock.where, (thePos.x, thePos.y), (thePos.x + thePos.width, thePos.y + thePos.height), aFilling, CVUI_FILLED, CVUI_ANTIALISED)

		# Render the border
		cv2.rectangle(theBlock.where, (thePos.x, thePos.y), (thePos.x + thePos.width, thePos.y + thePos.height), aBorder, 1, CVUI_ANTIALISED);

# Access points to internal namespaces.
# TODO: re-factor this and make it less ugly.
__internal = Internal()
__render = Render()
__internal._render = __render
__render._internal = __internal

def _handleMouse(theEvent, theX, theY, theFlags, theContext):
	aButtons = [LEFT_BUTTON, MIDDLE_BUTTON, RIGHT_BUTTON]
	aEventsDown = [cv2.EVENT_LBUTTONDOWN, cv2.EVENT_MBUTTONDOWN, cv2.EVENT_RBUTTONDOWN]
	aEventsUp = [cv2.EVENT_LBUTTONUP, cv2.EVENT_MBUTTONUP, cv2.EVENT_RBUTTONUP]

	for i in range(LEFT_BUTTON, RIGHT_BUTTON + 1):
		aBtn = aButtons[i]

		if theEvent == aEventsDown[i]:
			theContext.mouse.anyButton.justPressed = True
			theContext.mouse.anyButton.pressed = True
			theContext.mouse.buttons[aBtn].justPressed = True
			theContext.mouse.buttons[aBtn].pressed = True

		elif theEvent == aEventsUp[i]:
			theContext.mouse.anyButton.justReleased = True
			theContext.mouse.anyButton.pressed = False
			theContext.mouse.buttons[aBtn].justReleased = True
			theContext.mouse.buttons[aBtn].pressed = False

	theContext.mouse.position.x = theX
	theContext.mouse.position.y = theY
	print('_handleMouse', theEvent, theX, theY, theFlags)

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

def text(theWhere, theX, theY, theText, theFontScale = 0.4, theColor = 0xCECECE):
	__internal.screen.where = theWhere
	__internal.text(__internal.screen, theX, theY, theText, theFontScale, theColor, True)

def printf(*theArgs):
	if isinstance(theArgs[0], np.ndarray):
		# Not row/column function, signature is printf(theWhere, theX, theY, ...)
		aWhere = theArgs[0]
		aX = theArgs[1]
		aY = theArgs[2]
		__internal.screen.where = aWhere

		if __internal.isString(theArgs[3]):
			# Signature: printf(theWhere, theX, theY, theFmt, *theArgs)
			aFontScale = 0.4
			aColor = 0xCECECE
			aFmt = theArgs[3]
			aArgs= theArgs[4:]
		else:
			# Signature: printf(theWhere, theX, theY, theFontScale, theColor, theFmt, *theArgs)
			aFontScale = theArgs[3]
			aColor = theArgs[4]
			aFmt = theArgs[5]
			aArgs = theArgs[6:]

		aText = aFmt % aArgs
		__internal.text(__internal.screen, aX, aY, aText, aFontScale, aColor, True)
	else:
		# row/column function, signature is printf(theX, theY, ...)
		print('Not implemented yet')

def checkbox(theWhere, theX, theY, theLabel, theState, theColor = 0xCECECE):
	__internal.screen.where = theWhere
	return __internal.checkbox(__internal.screen, theX, theY, theLabel, theState, theColor)

def mouse(theWindowName = ''):
	"""
	 Return the last position of the mouse.

	 \param theWindowName name of the window whose mouse cursor will be used. If nothing is informed (default), the function will return the position of the mouse cursor for the default window (the one informed in `cvui::init()`).
	 \return a point containing the position of the mouse cursor in the speficied window.
	"""
	return __internal.getContext(theWindowName).mouse.position

def mouse2(theQuery):
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
	return mouse3('', theQuery)

def mouse3(theWindowName, theQuery):
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
	aButton = __internal.getContext(theWindowName).mouse.anyButton
	aRet = __internal.isMouseButton(aButton, theQuery)

	return aRet

def mouse4(theButton, theQuery):
	"""
	 Query the mouse for events in a particular button. This function behave exactly like `cvui::mouse(int theQuery)`,
	 with the difference that queries are targeted at a particular mouse button instead.

	 \param theButton an integer describing the mouse button to be queried. Possible values are `cvui::LEFT_BUTTON`, `cvui::MIDDLE_BUTTON` and `cvui::LEFT_BUTTON`.
	 \param theQuery an integer describing the intended mouse query. Available queries are `cvui::DOWN`, `cvui::UP`, `cvui::CLICK`, and `cvui::IS_DOWN`.

	 \sa mouse(const cv::String&)
	 \sa mouse(const cv::String&, int, int)
	 \sa mouse(int)
	"""
	return mouse5('', theButton, theQuery)

def mouse5(theWindowName, theButton, theQuery):
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

	aButton = __internal.getContext(theWindowName).mouse.buttons[theButton]
	aRet = __internal.isMouseButton(aButton, theQuery)

	return aRet

def button(where, x, y, label):
	# Not implemented yet!
	return False

def rect(theWhere, theX, theY, theWidth, theHeight, theBorderColor, theFillingColor = 0xff000000):
	__internal.screen.where = theWhere
	__internal.rect(__internal.screen, theX, theY, theWidth, theHeight, theBorderColor, theFillingColor)

def iarea(theX, theY, theWidth, theHeight):
	return __internal.iarea(theX, theY, theWidth, theHeight)	

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
	aContext.mouse.anyButton.justPressed = False

	for i in range(LEFT_BUTTON, RIGHT_BUTTON + 1):
		aContext.mouse.buttons[i].justReleased = False
		aContext.mouse.buttons[i].justPressed = False
	
	__internal.screen.reset()

	# If we were told to keep track of the keyboard shortcuts, we
	# proceed to handle opencv event queue.
	if __internal.delayWaitKey > 0:
		__internal.lastKeyPressed = cv2.waitKey(__internal.delayWaitKey)

	if __internal.blockStackEmpty() == False:
		__internal.error(2, "Calling update() before finishing all begin*()/end*() calls. Did you forget to call a begin*() or an end*()? Check if every begin*() has an appropriate end*() call before you call update().")

def imshow(theWindowName, theFrame):
	update(theWindowName)
	cv2.imshow(theWindowName, theFrame)