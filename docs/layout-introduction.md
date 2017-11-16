---
layout: default
title: layout-introduction
---

# Rows and columns

One of the most annoying tasks when building UI is to calculate where each component should be placed on the screen. cvui has a set of methods that abstract the position of components, so you don't have to think about (x,y) coordinates. Instead you just create rows/columns and cvui will place components in them for you.

You can create rows (and columns) using the pair `beginRow()` and `endRow()` (and `beginColumn()` and `endColumn()`). Use `begin*()` to start a group (row or column), add components, then finish the group by calling `end*()`.

For example, you can create a row at `(10, 20)` on the screen as:

{% highlight c++ %}
cv::Mat frame = cv::Mat(300, 800, CV_8UC3);

// Signature is: beginRow(cv::Mat, int x, int y)
cvui::beginRow(frame, 10, 20);
  cvui::text("This is another row");
  cvui::checkbox("checkbox", &checked);
  cvui::window(80, 80, "window");
  cvui::button(100, 30, "Fixed");
  cvui::text("with text.");  
cvui::endRow();
{% endhighlight %}

The code above will produce the following on the screen:

![Example of cvui::beginRow() and cvui::endRow()](/img/row-no-padding.png)

When creating a row (or a column), you are required to inform the frame where the group will be rendered and the `(x, y)` coordinates of the group. In the example above, the row will be rendered to `frame` at coordinates `(10, 20)`. Notice that all component calls between `beginRow()` and `endRow()` do not specify `(x, y)` coordinates, only width and height when needed, e.g. `cvui::window(80, 80, "window")` and `cvui::button(100, 30, "Fixed")`.

Both `cvui::beginRow()` and `cvui::beginColumn()` require you to specify a frame and `(x,y)` coordinates, but you can inform more rows/columns attributes. The signature of `cvui::begin*()` is:

{% highlight c++ %}
void begin*(cv::Mat &theWhere, int theX, int theY, int theWidth = -1, int theHeight = -1, int thePadding = 0)
{% endhighlight %}

The width and height of a row/column are `-1` by default, which means cvui will calculate it based on the components. If you specify a width or height for a row/column, it influences how adjacent components, e.g. another row or a button, will be rended nearby your row/column.

The parameter `thePadding` allow you to specify the spacement of components in a row/column. Below is the same row example, however using `50` as padding:

{% highlight c++ %}
// beginRow(cv::Mat, x, y, width, height, padding)
cvui::beginRow(frame, 10, 20, -1, -1, 50);
  cvui::text("This is another row");
  cvui::checkbox("checkbox", &checked);
  cvui::window(80, 80, "window");
  cvui::button(100, 30, "Fixed");
  cvui::text("with text.");  
cvui::endRow();
{% endhighlight %}

which will produce the following on the screen:

![Example of cvui::beginRow() and cvui::endRow() with padding](/img/row-padding.png)

Check the [row-column](https://github.com/Dovyski/cvui/tree/master/example/src/row-column) example for more information about rows and columns.
