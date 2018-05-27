# This is a documentation block with several lines
# so I can test how it works.

import cv2

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

# Class to represent 2D points
class Point:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

# Class to represent a rectangle
class Rect:
	def __init__(self, x = 0, y = 0, width = 0, height = 0):
		self.x = x
		self.y = y
		self.width = width
		self.height = height


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

	def init(self, theWindowName, theDelayWaitKey):
		self.defaultContext = theWindowName
		self.currentContext = theWindowName
		self.delayWaitKey = theDelayWaitKey
		self.lastKeyPressed = -1

	def error(self, theId, theMessage):
		print('[CVUI] Fatal error (code ', theId, '): ', theMessage)
		cv.waitKey(100000)
		sys.exit(-1)

	def getContext(self, theWindowName):
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

	def hexToScalar(self, theColor):
		aAlpha = (theColor >> 24) & 0xff
		aRed = (theColor >> 16) & 0xff
		aGreen = (theColor >> 8) & 0xff
		aBlue = theColor & 0xff

		return (aBlue, aGreen, aRed, aAlpha)


# Class that contains all rendering methods.
class Render:
	_internal = None

	def text(self, theBlock, theText, thePos, theFontScale, theColor):
		cv2.putText(theBlock.where, theText, (thePos.x, thePos.y), cv2.FONT_HERSHEY_SIMPLEX, theFontScale, self._internal.hexToScalar(theColor), 1, cv2.LINE_AA)

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

def printf(theWhere, theX, theY, theFontScale, theColor, theFmt, *theArgs):
    aText = theFmt % theArgs
    text(theWhere, theX, theY, aText, theFontScale, theColor)

def button(where, x, y, label):
	# Not implemented yet!
	return False

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
