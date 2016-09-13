/*
 A (very) simple UI lib built on top of OpenCV drawing primitives.

 Version: 1.1.0

 Copyright (c) 2016 Fernando Bevilacqua <dovyski@gmail.com>
 Licensed under the MIT license.
*/

#ifndef _CVUI_H_
#define _CVUI_H_

#include <opencv2/core/core.hpp>
#include <stdarg.h>

namespace cvui
{
/**
 Initializes the library. You must provide the name of the window where
 the components will be added.
 
 \param theWindowName name of the window where the components will be added
 \param theDelayWaitKey delay used by cv::waitKey at each call of cvui::update()
*/
void init(const cv::String& theWindowName, int theDelayWaitKey = 15);

/**
 Return the last key that was pressed
 You need not (and should not) call cv::waitKey between each frame.
 Instead, call cvui::update() that will in turn call cv::waitKey()

 Note : you can set the delay of cv::waitKey during cvui::init()
 */
int lastKeyPressed();


/**
 Display a button. The size of the button will be automatically adjusted to
 properly house the label content.

 \param theWhere the image/frame where the component should be rendered.
 \param theX position X where the component should be placed.
 \param theY position Y where the component should be placed.
 \param theLabel text displayed inside the button.
 \return `true` everytime the user clicks the button.
*/
bool button(cv::Mat& theWhere, int theX, int theY, const cv::String& theLabel);

/**
 Display a button. The button size will be defined by the width and height parameters,
 no matter the content of the label.

 \param theWhere the image/frame where the component should be rendered.
 \param theX position X where the component should be placed.
 \param theY position Y where the component should be placed.
 \param theWidth width of the button.
 \param theHeight height of the button.
 \param theLabel text displayed inside the button.
 \return `true` everytime the user clicks the button.
*/
bool button(cv::Mat& theWhere, int theX, int theY, int theWidth, int theHeight, const cv::String& theLabel);

/**
 Display a checkbox. You can use the state parameter to monitor if the
 checkbox is checked or not.

 \param theWhere the image/frame where the component should be rendered.
 \param theX position X where the component should be placed.
 \param theY position Y where the component should be placed.
 \param theLabel text displayed besides the clickable checkbox square.
 \param theState describes the current state of the checkbox: `true` means the checkbox is checked.
 \param theColor color of the label in the format `0xRRGGBB`, e.g. `0xff0000` for red.
 \return a boolean value that indicates the current state of the checkbox, `true` if it is checked.
*/
bool checkbox(cv::Mat& theWhere, int theX, int theY, const cv::String& theLabel, bool *theState, unsigned int theColor = 0xCECECE);

/**
 Display a piece of text.

 \param theWhere the image/frame where the component should be rendered.
 \param theX position X where the component should be placed.
 \param theY position Y where the component should be placed.
 \param theText the text content.
 \param theFontScale size of the text.
 \param theColor color of the text in the format `0xRRGGBB`, e.g. `0xff0000` for red.

 \sa printf()
*/
void text(cv::Mat& theWhere, int theX, int theY, const cv::String& theText, double theFontScale = 0.4, unsigned int theColor = 0xCECECE);

/**
 Display a piece of text that can be formated using `stdio's printf()` style. For instance
 if you want to display text mixed with numbers, you can use:

 ```
 printf(frame, 10, 15, 0.4, 0xff0000, "Text: %d and %f", 7, 3.1415);
 ```

 \param theWhere the image/frame where the component should be rendered.
 \param theX position X where the component should be placed.
 \param theY position Y where the component should be placed.
 \param theFontScale size of the text.
 \param theColor color of the text in the format `0xRRGGBB`, e.g. `0xff0000` for red.
 \param theFmt formating string as it would be supplied for `stdio's printf()`, e.g. `"Text: %d and %f", 7, 3.1415`.
 
 \sa text()
*/
void printf(cv::Mat& theWhere, int theX, int theY, double theFontScale, unsigned int theColor, const char *theFmt, ...);

/**
 Display a piece of text that can be formated using `stdio's printf()` style. For instance
 if you want to display text mixed with numbers, you can use:

 ```
 printf(frame, 10, 15, 0.4, 0xff0000, "Text: %d and %f", 7, 3.1415);
 ```

 The size and color of the text will be based on cvui's default values.

 \param theWhere the image/frame where the component should be rendered.
 \param theX position X where the component should be placed.
 \param theY position Y where the component should be placed.
 \param theFmt formating string as it would be supplied for `stdio's printf()`, e.g. `"Text: %d and %f", 7, 3.1415`.

 \sa text()
*/
void printf(cv::Mat& theWhere, int theX, int theY, const char *theFmt, ...);

/**
 Display a counter for integer values that the user can increase/descrease
 by clicking the up and down arrows.

 \param theWhere the image/frame where the component should be rendered.
 \param theX position X where the component should be placed.
 \param theY position Y where the component should be placed.
 \param theValue the current value of the counter.
 \param theStep the amount that should be increased/decreased when the user interacts with the counter buttons
 \param theFormat how the value of the counter should be presented, as it was printed by `stdio's printf()`. E.g. `"%d"` means the value will be displayed as an integer, `"%0d"` integer with one leading zero, etc.
 \return an integer that corresponds to the current value of the counter.
*/
int counter(cv::Mat& theWhere, int theX, int theY, int *theValue, int theStep = 1, const char *theFormat = "%d");

/**
 Display a counter for float values that the user can increase/descrease
 by clicking the up and down arrows.

 \param theWhere the image/frame where the component should be rendered.
 \param theX position X where the component should be placed.
 \param theY position Y where the component should be placed.
 \param theValue the current value of the counter.
 \param theStep the amount that should be increased/decreased when the user interacts with the counter buttons
 \param theFormat how the value of the counter should be presented, as it was printed by `stdio's printf()`. E.g. `"%f"` means the value will be displayed as a regular float, `"%.2f"` float with two digits after the point, etc.
 \return a float that corresponds to the current value of the counter.
*/
double counter(cv::Mat& theWhere, int theX, int theY, double *theValue, double theStep = 0.5, const char *theFormat = "%.2f");


struct TrackbarParams
{
	long double MinimumValue, MaximumValue;
	long double SmallStep, LargeStep;
	bool ForceValuesAsMultiplesOfSmallStep;
	bool DrawValuesAtLargeSteps;
	bool DrawSmallSteps;
	std::string Printf_Format;
	std::string Printf_Format_Steps;

	inline TrackbarParams()
			: MinimumValue(0.)
			, MaximumValue(25.)
			, SmallStep(1.)
			, LargeStep(5.)
			, ForceValuesAsMultiplesOfSmallStep(false)
			, DrawValuesAtLargeSteps(true)
			, DrawSmallSteps(true)
			, Printf_Format("%.0lf")
			, Printf_Format_Steps("")
	{
	}
};


template <typename T> // T can be any floating point type (float, double, long double)
TrackbarParams trackbarParams(
	T min, T max,
	int nbDecimals = 1,
	int nbLargeSteps = 1,
	T smallStep = -1.,
	bool forceValuesAsMultiplesOfSmallStep = false);





/**
Display a trackbar
 \param theWhere the image/frame where the component should be rendered.
 \param theX position X where the component should be placed.
 \param theY position Y where the component should be placed.
 \param theValue : pointer to the variable that will hold the value. Will be modified when the user interacts
 \param theParams : trackbar parameters : their names are self-explanatory

   Returns true when the value was modified, false otherwise

   This is the fully customizable version of the trackbar.

   Quick info about the Tracbar params
 	double MinimumValue, MaximumValue : self-explanatory
 	double SmallStep, LargeStep : steps at which smaller and larger ticks are drawn
 	bool ForceValuesAsMultiplesOfSmallStep : we can enforce the value to be a multiple of the small step
	bool DrawValuesAtLargeSteps : draw value at large steps
	bool DrawSmallSteps : draw ticks at small steps
	string Printf_Format : printf format string of the value
	string Printf_Format_Steps : printf format string of the steps (will be replaced by Printf_Format if empty)

 \sa printf()
 \sa beginColumn()
 \sa beginRow()
 \sa endRow()
 \sa endColumn()
*/
template <typename T> // T can be any numeric type (int, double, unsigned int, etc)
bool trackbar(cv::Mat& theWhere, int theX, int theY, T *theValue, const TrackbarParams & theParams);


/**
trackbar_float : Display a trackbar
 \param theWhere the image/frame where the component should be rendered.
 \param theX position X where the component should be placed.
 \param theY position Y where the component should be placed.
 \param theValue : pointer to the variable that will hold the value. Will be modified when the user interacts
 \param theMin : minimum value of the trackbar
 \param theMax : maximum value of the trackbar
 \param theNumberOfDecimals : number of decimal digits to be displayed
 \param theNumberOfLargeSteps : number of large steps (at which a legend will be written, as on a ruler)
 \param theSmallStep : small steps at which ticks will be drawn (-1 to cancel these)
 \param flagForceValuesAsMultiplesOfSmallStep : enforce values to be a multiple of theSmallStep

   Returns true when the value was modified, false otherwise

   Note : remember to cast the minimum and maximum values to your type
  See examples below :

   float myValue;
   cvui::trackbar_float(&myValue, 0.f, 100.f);
   unsigned char myValue;
   cvui::trackbar_float(&myValue, (unsigned char)0, (unsigned char)255);

 \sa printf()
 \sa beginColumn()
 \sa beginRow()
 \sa endRow()
 \sa endColumn()
*/
template <typename T> // T can be any float type (float, double, long double)
bool trackbar(  cv::Mat& theWhere, int theX, int theY,
				T *theValue,
				T theMin, T theMax,
				int theNumberOfDecimals = 1,
				int theNumberOfLargeSteps = 1,
				T theSmallStep = -1.,
				bool flagForceValuesAsMultiplesOfSmallStep = false);

/**
 Display a window (a block with a title and a body).

 \param theWhere the image/frame where the component should be rendered.
 \param theX position X where the component should be placed.
 \param theY position Y where the component should be placed.
 \param theWidth width of the window.
 \param theHeight height of the window.
 \param theTitle text displayed as the title of the window.

 \sa rect()
*/
void window(cv::Mat& theWhere, int theX, int theY, int theWidth, int theHeight, const cv::String& theTitle);

/**
 Display a filled rectangle.

 \param theWhere the image/frame where the component should be rendered.
 \param theX position X where the component should be placed.
 \param theY position Y where the component should be placed.
 \param theWidth width of the rectangle.
 \param theHeight height of the rectangle.
 \param theBorderColor color of rectangle's border in the format `0xRRGGBB`, e.g. `0xff0000` for red.
 \param theFillingColor color of rectangle's filling in the format `0xAARRGGBB`, e.g. `0x00ff0000` for red, `0xff000000` for transparent filling.
*/
void rect(cv::Mat& theWhere, int theX, int theY, int theWidth, int theHeight, unsigned int theBorderColor, unsigned int theFillingColor = 0xff000000);

/**
 Display the values of a vector as a sparkline.

 \param theWhere the image/frame where the component should be rendered.
 \param theValues a vector containing the values to be used in the sparkline.
 \param theX position X where the component should be placed.
 \param theY position Y where the component should be placed.
 \param theWidth width of the sparkline.
 \param theHeight height of the sparkline.
 \param theColor color of sparkline in the format `0xRRGGBB`, e.g. `0xff0000` for red.
*/
void sparkline(cv::Mat& theWhere, std::vector<double>& theValues, int theX, int theY, int theWidth, int theHeight, unsigned int theColor = 0x00FF00);

/**
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
 beginRow(frame, x, y, width, height);
  text("test");
  button("btn");
 endRow();
 ```

 Rows and columns can be nested, so you can create columns/rows within
 columns/rows as much as you want. It's important to notice that any
 component within `beginRow()` and `endRow()` *do not* specify the position
 where the component is rendered, which is also true for `beginRow()`.
 As a consequence, **be sure you are calling `beginRow(width, height)`
 when the call is nested instead of `beginRow(x, y, width, height)`**,
 otherwise cvui will throw an error.

 E.g.

 ```
 beginRow(frame, x, y, width, height);
  text("test");       
  button("btn"); 

  beginColumn();      // no frame nor x,y parameters here!
   text("column1");
   text("column2");
  endColumn();
 endRow();
 ```

 Don't forget to call `endRow()` to finish the row, otherwise cvui will throw an error.

 \param theWhere the image/frame where the components within this block should be rendered.
 \param theX position X where the row should be placed.
 \param theY position Y where the row should be placed.
 \param theWidth width of the row. If a negative value is specified, the width of the row will be automatically calculated based on the content of the block.
 \param theHeight height of the row. If a negative value is specified, the height of the row will be automatically calculated based on the content of the block.
 \param thePadding space, in pixels, among the components of the block.

 \sa beginColumn()
 \sa endRow()
 \sa endColumn()
*/
void beginRow(cv::Mat &theWhere, int theX, int theY, int theWidth = -1, int theHeight = -1, int thePadding = 0);

/**
 Ends a row. You must call this function only if you have previously called
 its counter part, the `beginRow()` function. 

\sa beginRow()
\sa beginColumn()
\sa endColumn()
*/
void endRow();

/**
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
 beginColumn(frame, x, y, width, height);
  text("test");
  button("btn");
 endColumn();
 ```

 Rows and columns can be nested, so you can create columns/rows within
 columns/rows as much as you want. It's important to notice that any
 component within `beginColumn()` and `endColumn()` *do not* specify the position
 where the component is rendered, which is also true for `beginColumn()`.
 As a consequence, **be sure you are calling `beginColumn(width, height)`
 when the call is nested instead of `beginColumn(x, y, width, height)`**,
 otherwise cvui will throw an error.

E.g.

```
beginColumn(frame, x, y, width, height);
 text("test");
 button("btn");

 beginRow();      // no frame nor x,y parameters here!
  text("column1");
  text("column2");
 endRow();
endColumn();
```

Don't forget to call `endColumn()` to finish the column, otherwise cvui will throw an error.

\param theWhere the image/frame where the components within this block should be rendered.
\param theX position X where the row should be placed.
\param theY position Y where the row should be placed.
\param theWidth width of the column. If a negative value is specified, the width of the column will be automatically calculated based on the content of the block.
\param theHeight height of the column. If a negative value is specified, the height of the column will be automatically calculated based on the content of the block.
\param thePadding space, in pixels, among the components of the block.

\sa beginRow()
\sa endColumn()
\sa endRow()
*/
void beginColumn(cv::Mat &theWhere, int theX, int theY, int theWidth = -1, int theHeight = -1, int thePadding = 0);

/**
 Ends a column. You must call this function only if you have previously called
 its counter part, the `beginColumn()` function.

 \sa beginColumn()
 \sa beginRow()
 \sa endRow()
*/
void endColumn();

/**
Starts a row. This function behaves in the same way as `beginRow(frame, x, y, width, height)`,
however it is suposed to be used within `begin*()/end*()` blocks since they require components
not to inform frame nor x,y coordinates.

\sa beginColumn()
\sa endRow()
\sa endColumn()
*/
void beginRow(int theWidth = -1, int theHeight = -1, int thePadding = 0);

/**
Starts a column. This function behaves in the same way as `beginColumn(frame, x, y, width, height)`,
however it is suposed to be used within `begin*()/end*()` blocks since they require components
not to inform frame nor x,y coordinates.

\sa beginColumn()
\sa endRow()
\sa endColumn()
*/
void beginColumn(int theWidth = -1, int theHeight = -1, int thePadding = 0);

/**
 Adds an arbitrary amount of space between components within a `begin*()` and `end*()` block.
 The function is aware of context, so if it is used within a `beginColumn()` and
 `endColumn()` block, the space will be vertical. If it is used within a `beginRow()`
 and `endRow()` block, space will be horizontal.

 IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

 \param theValue the amount of space to be added.

 \sa beginColumn()
 \sa beginRow()
 \sa endRow()
 \sa endColumn()
*/
void space(int theValue = 5);

/**
 Display a piece of text within a `begin*()` and `end*()` block.
 IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

 \param theText the text content.
 \param theFontScale size of the text.
 \param theColor color of the text in the format `0xRRGGBB`, e.g. `0xff0000` for red.

 \sa printf()
 \sa beginColumn()
 \sa beginRow()
 \sa endRow()
 \sa endColumn()
*/
void text(const cv::String& theText, double theFontScale = 0.4, unsigned int theColor = 0xCECECE);

// 
/**
 Display a button within a `begin*()` and `end*()` block.
 The button size will be defined by the width and height parameters,
 no matter the content of the label.

 IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

 \param theWidth width of the button.
 \param theHeight height of the button.
 \param theLabel text displayed inside the button. You can set shortcuts by pre-pending them with "&"
 \return `true` everytime the user clicks the button.

 \sa beginColumn()
 \sa beginRow()
 \sa endRow()
 \sa endColumn()
*/
bool button(int theWidth, int theHeight, const cv::String& theLabel);

/**
 Display a button within a `begin*()` and `end*()` block. The size of the button will be
 automatically adjusted to properly house the label content.

 IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

 \param theLabel text displayed inside the button. You can set shortcuts by pre-pending them with "&"
 \return `true` everytime the user clicks the button.

 \sa beginColumn()
 \sa beginRow()
 \sa endRow()
 \sa endColumn()
*/
bool button(const cv::String& theLabel);

/**
 Display a checkbox within a `begin*()` and `end*()` block. You can use the state parameter
 to monitor if the checkbox is checked or not.

 IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

 \param theLabel text displayed besides the clickable checkbox square.
 \param theState describes the current state of the checkbox: `true` means the checkbox is checked.
 \param theColor color of the label in the format `0xRRGGBB`, e.g. `0xff0000` for red.
 \return a boolean value that indicates the current state of the checkbox, `true` if it is checked.

 \sa beginColumn()
 \sa beginRow()
 \sa endRow()
 \sa endColumn()
*/
bool checkbox(const cv::String& theLabel, bool *theState, unsigned int theColor = 0xCECECE);

/**
 Display a piece of text within a `begin*()` and `end*()` block.
 
 IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

 The text can be formated using `stdio's printf()` style. For instance if you want to display text mixed
 with numbers, you can use:

 ```
 printf(0.4, 0xff0000, "Text: %d and %f", 7, 3.1415);
 ```

\param theFontScale size of the text.
\param theColor color of the text in the format `0xRRGGBB`, e.g. `0xff0000` for red.
\param theFmt formating string as it would be supplied for `stdio's printf()`, e.g. `"Text: %d and %f", 7, 3.1415`.

\sa text()
\sa beginColumn()
\sa beginRow()
\sa endRow()
\sa endColumn()
*/
void printf(double theFontScale, unsigned int theColor, const char *theFmt, ...);

/**
 Display a piece of text that can be formated using `stdio's printf()` style.
 
 IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

 For instance if you want to display text mixed with numbers, you can use:

 ```
 printf(frame, 10, 15, 0.4, 0xff0000, "Text: %d and %f", 7, 3.1415);
 ```

 The size and color of the text will be based on cvui's default values.

 \param theFmt formating string as it would be supplied for `stdio's printf()`, e.g. `"Text: %d and %f", 7, 3.1415`.

 \sa text()
 \sa beginColumn()
 \sa beginRow()
 \sa endRow()
 \sa endColumn()
*/
void printf(const char *theFmt, ...);

/**
 Display a counter for integer values that the user can increase/descrease
 by clicking the up and down arrows.

 IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

 \param theValue the current value of the counter.
 \param theStep the amount that should be increased/decreased when the user interacts with the counter buttons.
 \param theFormat how the value of the counter should be presented, as it was printed by `stdio's printf()`. E.g. `"%d"` means the value will be displayed as an integer, `"%0d"` integer with one leading zero, etc.
 \return an integer that corresponds to the current value of the counter.

\sa printf()
\sa beginColumn()
\sa beginRow()
\sa endRow()
\sa endColumn()
*/
int counter(int *theValue, int theStep = 1, const char *theFormat = "%d");

/**
 Display a counter for float values that the user can increase/descrease
 by clicking the up and down arrows.

 IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

 \param theValue the current value of the counter.
 \param theStep the amount that should be increased/decreased when the user interacts with the counter buttons.
 \param theFormat how the value of the counter should be presented, as it was printed by `stdio's printf()`. E.g. `"%d"` means the value will be displayed as an integer, `"%0d"` integer with one leading zero, etc.
 \return an float that corresponds to the current value of the counter.

 \sa printf()
 \sa beginColumn()
 \sa beginRow()
 \sa endRow()
 \sa endColumn()
*/
double counter(double *theValue, double theStep = 0.5, const char *theFormat = "%.2f");


/**
Display a trackbar

 \param theValue : pointer to the variable that will hold the value
 \param theParams : trackbar parameters : their names are self-explanatory
 Returns true when the value was modified, false otherwise

    Quick info about the Tracbar params
 	double MinimumValue, MaximumValue : self-explanatory
 	double SmallStep, LargeStep : steps at which smaller and larger ticks are drawn
 	bool ForceValuesAsMultiplesOfSmallStep : we can enforce the value to be a multiple of the small step
	bool DrawValuesAtLargeSteps : draw value at large steps
	bool DrawSmallSteps : draw ticks at small steps
	string Printf_Format : printf format string of the value
	string Printf_Format_Steps : printf format string of the steps (will be replaced by Printf_Format if empty)

  IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

 \sa printf()
 \sa beginColumn()
 \sa beginRow()
 \sa endRow()
 \sa endColumn()
*/
template<typename T>
bool trackbar(T *theValue, const TrackbarParams & theParams);


/**
trackbar_float : Display a trackbar
 \param theValue : pointer to the variable that will hold the value. Will be modified when the user interacts
 \param theMin : minimum value of the trackbar
 \param theMax : maximum value of the trackbar
 \param theNumberOfDecimals : number of decimal digits to be displayed
 \param theNumberOfLargeSteps : number of large steps (at which a legend will be written, as on a ruler)
 \param theSmallStep : small steps at which ticks will be drawn (-1 to cancel these)
 \param flagForceValuesAsMultiplesOfSmallStep : enforce values to be a multiple of theSmallStep

  Note : remember to cast the minimum and maximum values to your type
  See examples below :

   float myValue;
   cvui::trackbar_float(&myValue, 0.f, 100.f);
   unsigned char myValue;
   cvui::trackbar_float(&myValue, (unsigned char)0, (unsigned char)255);

   Returns true when the value was modified, false otherwise
*/
template <typename T> // T can be any float type (float, double, long double)
bool trackbar(
		T *theValue,
		T theMin, T theMax,
		int theNumberOfDecimals = 1,
		int theNumberOfLargeSteps = 1,
		T theSmallStep = -1.,
		bool flagForceValuesAsMultiplesOfSmallStep = true);



/**
 Display a window (a block with a title and a body) within a `begin*()` and `end*()` block.

 IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

 \param theWidth width of the window.
 \param theHeight height of the window.
 \param theTitle text displayed as the title of the window.

 \sa rect()
 \sa beginColumn()
 \sa beginRow()
 \sa endRow()
 \sa endColumn()
*/
void window(int theWidth, int theHeight, const cv::String& theTitle);

/**
 Display a rectangle within a `begin*()` and `end*()` block.
 
 IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

 \param theWidth width of the rectangle.
 \param theHeight height of the rectangle.
 \param theBorderColor color of rectangle's border in the format `0xRRGGBB`, e.g. `0xff0000` for red.
 \param theFillingColor color of rectangle's filling in the format `0xAARRGGBB`, e.g. `0x00ff0000` for red, `0xff000000` for transparent filling.

 \sa window()
 \sa beginColumn()
 \sa beginRow()
 \sa endRow()
 \sa endColumn()
*/
void rect(int theWidth, int theHeight, unsigned int theBorderColor, unsigned int theFillingColor = 0xff000000);

/**
 Display the values of a vector as a sparkline within a `begin*()` and `end*()` block.

 IMPORTANT: this function can only be used within a `begin*()/end*()` block, otherwise it does nothing.

 \param theValues vector with the values that will be rendered as a sparkline.
 \param theWidth width of the sparkline.
 \param theHeight height of the sparkline.
 \param theColor color of sparkline in the format `0xRRGGBB`, e.g. `0xff0000` for red.

 \sa beginColumn()
 \sa beginRow()
 \sa endRow()
 \sa endColumn()
*/
void sparkline(std::vector<double>& theValues, int theWidth, int theHeight, unsigned int theColor = 0x00FF00);



/**
 Updates the library internal things. You need to call this function **AFTER** you are done adding/manipulating
 UI elements in order for them to react to mouse interactions.
*/
void update();

// Internally used to handle mouse events
void handleMouse(int theEvent, int theX, int theY, int theFlags, void* theData);

#ifdef __GNUC__
// just to remove the warning under gcc that is introduced by the VERSION variable below
// (needed for those who compile with -Werror (make warning as errors)
#pragma GCC diagnostic ignored "-Wunused-variable"
#endif
// Lib version
static const char *VERSION = "1.1.0";

const int ROW = 0;
const int COLUMN = 1;

// Describes the block structure used by the lib to handle `begin*()` and `end*()` calls.
typedef struct {
	cv::Mat where;			// where the block should be rendered to.
	cv::Rect rect;			// the size and position of the block.
	cv::Rect fill;			// the filled area occuppied by the block as it gets modified by its inner components.
	cv::Point anchor;		// the point where the next component of the block should be rendered.
	int padding;			// padding among components within this block.
	int type;				// type of the block, e.g. ROW or COLUMN.
} cvui_block_t;

// Internal namespace that contains all rendering functions.
namespace render {
	const int IDLE = 0;
	const int OVER = 1;
	const int PRESSED = 2;

	void text(cvui_block_t& theBlock, const cv::String& theText, cv::Point& thePos, double theFontScale, unsigned int theColor);
	void button(cvui_block_t& theBlock, int theState, cv::Rect& theShape, const cv::String& theLabel);
	void buttonLabel(cvui_block_t& theBlock, int theState, cv::Rect theRect, const cv::String& theLabel, cv::Size& theTextSize);
	void counter(cvui_block_t& theBlock, cv::Rect& theShape, const cv::String& theValue);
	void trackbar(cvui_block_t& theBlock, cv::Rect& theShape, double theValue, const TrackbarParams &theParams, bool theMouseIsOver);
	void checkbox(cvui_block_t& theBlock, int theState, cv::Rect& theShape);
	void checkboxLabel(cvui_block_t& theBlock, cv::Rect& theRect, const cv::String& theLabel, cv::Size& theTextSize, unsigned int theColor);
	void checkboxCheck(cvui_block_t& theBlock, cv::Rect& theShape);
	void window(cvui_block_t& theBlock, cv::Rect& theTitleBar, cv::Rect& theContent, const cv::String& theTitle);
	void rect(cvui_block_t& theBlock, cv::Rect& thePos, unsigned int theBorderColor, unsigned int theFillingColor);
	void sparkline(cvui_block_t& theBlock, std::vector<double>& theValues, cv::Rect &theRect, double theMin, double theMax, unsigned int theColor);
}

} // namespace cvui

#endif // _CVUI_H_