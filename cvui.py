# This is a documentation block with several lines
# so I can test how it works.

import cv2

def main():
      print("cvui main")

if __name__ == '__main__':
    main()

RIGHT_BUTTON = 0
MIDDLE_BUTTON = 1
LEFT_BUTTON = 2

# Class to represent 2D points
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Describes the block structure used by the lib to handle `begin*()` and `end*()` calls.
class Block:
    __slots__ = [
        'where',       # where the block should be rendered to.
        'rect',        # the size and position of the block.
        'fill',        # the filled area occuppied by the block as it gets modified by its inner components.
        'anchor',      # the point where the next component of the block should be rendered.
        'padding',     # padding among components within this block.
        'type'         # type of the block, e.g. ROW or COLUMN.
    ]

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
    __slots__ = [
        'justReleased',  # if the mouse button was released, i.e. click event.
        'justPressed',   # if the mouse button was just pressed, i.e. true for a frame when a button is down.
        'pressed'        # if the mouse button is pressed or not.
    ]

# Describe the information of the mouse cursor
class Mouse:
    buttons = {                        # status of each button. Use cvui::{RIGHT,LEFT,MIDDLE}_BUTTON to access the buttons.
		RIGHT_BUTTON: MouseButton(),
		MIDDLE_BUTTON: MouseButton(),
		LEFT_BUTTON: MouseButton()
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
    defaultContext = ''
    currentContext = ''
    contexts = {} # indexed by the window name.
    buffer = []
    lastKeyPressed = -1 # TODO: collect it per window
    delayWaitKey = -1
    screen = Block()
    stack = []
    stackCount = -1
    trackbarMarginX = 14

    def __init__(self):
        self.defaultContext = ''

    def init(self, theWindowName, theDelayWaitKey):
        self.defaultContext = theWindowName
        self.currentContext = theWindowName
        self.delayWaitKey = theDelayWaitKey
        self.lastKeyPressed = -1

# Class that contains all rendering methods.
class Render:
    def text(self, theBlock, theText, thePos, theFontScale, theColor):
        print('not implemented yet')

# Access point to the internal namespace.
__internal = Internal()
__render = Render()

def _handleMouse(theEvent, theX, theY, theFlags, theContext):
	aButtons = [LEFT_BUTTON, MIDDLE_BUTTON, RIGHT_BUTTON]
	aEventsDown = [cv2.EVENT_LBUTTONDOWN, cv2.EVENT_MBUTTONDOWN, cv2.EVENT_RBUTTONDOWN]
	aEventsUp = [cv2.EVENT_LBUTTONUP, cv2.EVENT_MBUTTONUP, cv2.EVENT_RBUTTONUP]

	for i in range(0, 3):
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
    aContex = Context()

    if theCreateNamedWindow:
        cv2.namedWindow(theWindowName)

    aContex.windowName = theWindowName
    aContex.mouse.position.x = 0
    aContex.mouse.position.y = 0

    #__internal.resetMouseButton(aContex.mouse.anyButton)
    #__internal.resetMouseButton(aContex.mouse.buttons[RIGHT_BUTTON])
    #__internal.resetMouseButton(aContex.mouse.buttons[MIDDLE_BUTTON])
    #__internal.resetMouseButton(aContex.mouse.buttons[LEFT_BUTTON])

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

def text(where, x, y, text, font_scale = 0.4, color = 0xCECECE):
	cv2.putText(where, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 1, cv2.LINE_AA)

def printf(theWhere, theX, theY, theFontScale, theColor, theFmt, *theArgs):
    aText = theFmt % theArgs
    text(theWhere, theX, theY, aText, theFontScale, theColor)

def button(where, x, y, label):
	# Not implemented yet!
	return False

def update(window_name = ""):
	"""
	Updates the library internal things. You need to call this function **AFTER** you are done adding/manipulating
	UI elements in order for them to react to mouse interactions.

	Parameters
    ----------
	window_name : str
		Name of the window whose components are being updated. If no window name is provided, cvui uses the default window.

	\sa init()
	\sa watch()
	\sa context()
	"""