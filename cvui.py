# This is a documentation block with several lines
# so I can test how it works.

import cv2

def main():
      print("cvui main")

if __name__ == '__main__':
    main()

def random_number_generator(arg1, arg2):
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
    return 42

def init(window_name, delay_wait_key = -1, create_named_window = True):
	cv2.namedWindow(window_name)

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