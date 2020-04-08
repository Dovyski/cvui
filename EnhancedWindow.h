#ifndef _ENHANCED_WINDOW_H_
#define _ENHANCED_WINDOW_H_

/*
This class enhances the window component of cvui by making it movable and minimizable.

Authors:
	ShengYu - https://github.com/shengyu7697
	Amaury Bréhéret - https://github.com/abreheret

Contributions:
	Fernando Bevilacqua <dovyski@gmail.com>

Code licensed under the MIT license.
*/
class EnhancedWindow
{
private:
	int mX;
	int mY;
	int mWidth;
	int mHeight;
	int mHeightNotMinimized;
	cv::String mTitle;
	int mDeltaY;
	int mDeltaX;
	bool mIsMoving;
	bool mMinimized;
	bool mMinimizable;
	double mFontScale;

public:
	EnhancedWindow(int x, int y, int width, int height, const cv::String& title, bool minimizable = true, double theFontScale = cvui::DEFAULT_FONT_SCALE):
		mX(x),
		mY(y),
		mWidth(width),
		mHeight(height),
		mHeightNotMinimized(height),
		mTitle(title),
		mDeltaY(0),
		mDeltaX(0),
		mIsMoving(false),
		mMinimized(false),
		mMinimizable(minimizable),
		mFontScale(theFontScale) {
	}

	void begin(cv::Mat &frame) {
		int scaledTitleHeight = std::lround(20*mFontScale/cvui::DEFAULT_FONT_SCALE);
		bool mouseInsideTitleArea = cvui::mouse().inside(cv::Rect(mX, mY, mWidth, scaledTitleHeight));
		mHeight = mMinimized ? scaledTitleHeight : mHeightNotMinimized;

		if (mIsMoving == false && cvui::mouse(cvui::DOWN) && mouseInsideTitleArea) {
			mDeltaX = cvui::mouse().x - mX;
			mDeltaY = cvui::mouse().y - mY;
			mIsMoving = true;

		} else if (mIsMoving && cvui::mouse(cvui::IS_DOWN)) {
			mX = cvui::mouse().x - mDeltaX;
			mY = cvui::mouse().y - mDeltaY;

		} else {
			mIsMoving = false;
			mX = std::max(0, mX);
			mY = std::max(0, mY);
			mX = std::min(frame.cols - mWidth, mX);
			mY = std::min(frame.rows - scaledTitleHeight, mY);
		}

		cvui::window(frame, mX, mY, mWidth, mHeight, mTitle, mFontScale);
		if (mMinimizable && cvui::button(frame, mX + mWidth - scaledTitleHeight, mY + 1, scaledTitleHeight-1, scaledTitleHeight-1, mMinimized ? "+" : "-", mFontScale)) {
			mMinimized = !mMinimized;
		}
		cvui::beginRow(frame, mX + std::lround(10*mFontScale/cvui::DEFAULT_FONT_SCALE), mY + std::lround(30*mFontScale/cvui::DEFAULT_FONT_SCALE), mWidth - scaledTitleHeight, mHeight - scaledTitleHeight);
		cvui::beginColumn(mWidth - std::lround(10*mFontScale/cvui::DEFAULT_FONT_SCALE), mHeight - scaledTitleHeight);
	}

/**
	Use this function to get the maximum width of a child widget of EnhancedWindow.

	\return the width of the EnhancedWindow without the inner borders that are automatically added
*/
	int widthWithoutBorders() {
		return mWidth - std::lround(20*mFontScale/cvui::DEFAULT_FONT_SCALE);
	}
	
/**
	Use this function to get the maximum height of a child widget of EnhancedWindow.

	\return the height of the EnhancedWindow without title and inner borders that are automatically added
*/
	int heightWithoutBorders() {
		return mHeight - std::lround(40*mFontScale/cvui::DEFAULT_FONT_SCALE);
	}
	
	void end() {
		cvui::endColumn();
		cvui::endRow();
	}

	int posX() const {
		return mX;
	}

	int posY() const {
		return mY;
	}
	
	void setPosX(int posX) {
		mX = posX;
	}

	void setPosY(int posY) {
		mY = posY;
	}

	int width() const {
		return mWidth;
	}

	int height() const {
		return mHeight;
	}

	void setWidth(int w) {
		mWidth = w;
	}

	void setHeight(int h) {
		mHeight = mHeightNotMinimized = h;
	}

	double fontScale() const {
		return mFontScale;
	}
	
	void setFontScale(double fontScale) {
		mFontScale = fontScale;
	}

	bool isMinimized() const {
		return mMinimized;
	}
};

#endif // _ENHANCED_WINDOW_H_
