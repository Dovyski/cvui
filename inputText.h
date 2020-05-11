#include "cvui.h"

using namespace cvui;

/**
Allows for input via keyboard when inputField is true, no mater where or what you type, it will be placed at the X and Y cords.

WARNING: It doesnt always regester your press, infact in my experences it only got about 50% of it.

WARNING: It can't tell the differece between one textBox and another, they will use the same string.

\param theWhere frame where its rendered.
\param theX the X cordinate.
\param theY the Y cordinate.
\param millisecondDelay the delay wait for a key press (seems to influence how effective it is), also calculates to FPS (Frames Per Second).
\param theFontScale the size of input text.
\param textColor the color of the text.

\sa text()
*/
std::string inputField(cv::Mat &theWhere, int theX, int theY, int millisecondDelay = 10, double theFontScale = DEFAULT_FONT_SCALE, unsigned int textColor = 0xCECECE) {

	char keyChar;
	std::string keyString;
	static std::string totalString;

	keyChar = cv::waitKey(millisecondDelay);

	if (std::size(totalString) <= 0 && keyChar == 8 || keyChar == 127)
		totalString = totalString;

	else if ((keyChar < 8 || keyChar > 9) && keyChar != 27 && keyChar < 32 && keyChar > 127)
		totalString = totalString;

	else if (keyChar == 8 || keyChar == 127)
		totalString.erase(std::prev(totalString.end()));

	else if (keyChar != -1) {

		keyString = (1, keyChar);
		totalString += keyString;

	}

	cvui::text(theWhere, theX, theY, totalString, theFontScale);

	return totalString;
}

/**
Allows for input via keyboard after you click the area its located, oce clicked anything you type will be placed in the box (Hopefully).

WARNING: It doesnt always regester your press, infact in my experences it only got about 50% of it.

WARNING: It can't tell the differece between one textBox and another, they will use the same string.

\param theWhere frame where its rendered.
\param theX the X cordinate.
\param theY the Y cordinate.
\param textY helps align text into the text box
\param theWidth width of the text box.
\param theHeight height of the text box.
\param millisecondDelay the delay wait for a key press (seems to influence how effective typing is), also calculates to FPS (Frames Per Second).
\param theBorderColor color of text box's border in the format `0xRRGGBB`, e.g. `0xff0000` for red.
\param theFillingColor color of rectangle's filling in the format `0xAARRGGBB`, e.g. `0x00ff0000` for red, `0xff000000` for transparent filling.
\param theFontScale the size of input text.
\param textColor the color of the text.

\sa inputField()
\sa iarea()
\sa rect()
\sa text()
*/
std::string inputBox(cv::Mat& theWhere, int theX, int theY, int textY, int theWidth, int theHeight, int millisecondDelay = 10, unsigned int theBorderColor = 0xc9c9c9, unsigned int theFillingColor = 0x676054, double theFontScale = DEFAULT_FONT_SCALE, unsigned int textColor = 0xCECECE) {
	static std::string totalStr;
	static bool allowInput = false;

	rect(theWhere, theX, theY, theWidth, theHeight, theBorderColor, theFillingColor);

	int status = iarea(theX, theY, theWidth, theHeight);

	if (status == OUT && mouse(DOWN))
		allowInput = false;

	else if (status == CLICK)
		allowInput = true;

	if (allowInput == true) {

		totalStr = (inputField(theWhere, (theX + 5), textY, millisecondDelay, theFontScale, textColor));

	}

	cvui::text(theWhere, (theX + 5), textY, totalStr, theFontScale);


	return totalStr;
}
