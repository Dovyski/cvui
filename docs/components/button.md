---
layout: default
permalink: /components/button
id: button
---

# Button

The `button()` function will render a button on the screen. The common signature of a button function is:

{% highlight c++ %}
bool button(cv::Mat& theWhere, int theX, int theY, const cv::String& theLabel)
{% endhighlight %}

where `theWhere` is the image/frame where the button will be rendered, `theX` is the position X, `theY` is the position Y, and `theLabel` is the text displayed inside the button. All button functions return `true` if the user clicked the button, or `false` otherwise.

The basic usage below is a button whose width will auto-adjust according to the size of the label:

{% highlight c++ %}
// cv::Mat frame, x, y, label
if (cvui::button(frame, 50, 60, "Button")) {
  // button was clicked
}
{% endhighlight %}

It is also possible to specify the width and height of a button:

{% highlight c++ %}
// cv::Mat frame, x, y, width, height, label
if (cvui::button(frame, 50, 60, 80, 30, "Button")) {
  // button was clicked
}
{% endhighlight %}

You can also display a button whose graphics are images (`cv::Mat`). Such button accepts three images to describe its states, which are _idle_ (no mouse interaction), _over_ (mouse is over the button) and _down_ (mouse clicked the button). The button size will be defined by the width and height of the images:

{% highlight c++ %}
cv::Mat out = cv::imread("./btn_out_state.jpg", cv::IMREAD_COLOR);
cv::Mat down = cv::imread("./btn_down_state.jpg", cv::IMREAD_COLOR);
cv::Mat over = cv::imread("./btn_over_state.jpg", cv::IMREAD_COLOR);

// cv::Mat, x, y, cv::Mat, cv::Mat, cv::Mat
if (cvui::button(frame, 200, 80, out, over, down)) {
	std::cout << "Image button clicked!" << std::endl;
}
{% endhighlight %}

Check the [image-button](https://github.com/Dovyski/cvui/tree/master/example/src/image-button) example for more information about buttons with custom rendering based on images.
