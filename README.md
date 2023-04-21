# easy_mvp

## Description

**easy_mvp** is a package that makes it easy to build desktop applications
using **MVP** pattern, **Python** and **PyQt5**. This is achieved by using
a set of classes and practices similar to those used in the **Android framework**.

The basic idea behind this package is to open a presenter from
another presenter and that the new presenter fills the window for
complete. This is similar to **Android applications**, which
when opening a new **Activity**, they replace the old one with the new one.
If the Back button is pressed, then the new **Activity** is removed
and the old one reappears on the screen. This gives the impression
that there is a **stack of Activity**.

In addition, **easy_mvp** offers the possibility of doing the above **in more than
a window**, since desktop applications are very different to **Android apps**.

## Installation

To install this package you need to have **Python** installed in your system.
Then you can run this command to install this package:

````shell script
pip install easy_mvp
````

## Explaining the mechanism

The following explanations are reflected in ``demo.py`` program.

### The application model created by **easy_mvp** is like this:

![App Manager and windows](https://github.com/R0land013/easy-mvp/blob/master/readme_img/app_manager_and_windows.png?raw=true)

The **ApplicationManager** class is the **entry point** of the program. This
class is the one that knows the windows, creates them and destroys them. Each
window holds a **stack of presenters**. In this way it is implemented
the same behavior that Android applications have. Class
**Intent** is used to **transition** from one presenter to another,
regardless of whether the new presenter is started in a new window.


### The behavior of the windows is represented as follows:

![Window with its internal stack presenter](https://github.com/R0land013/easy-mvp/blob/b2c8ba51e5315679848925967611e1e5931871dd/readme_img/window_with_its_internal_stack.png?raw=true)

As you can see the **window has a stack of presenters**, the
which are attached to their views, therefore **all the
presenters must possess a view**. Again we can see that the class
**Intent** is the one that allows to add a new **pair of presenter-view**
to the window stack. For this mechanism to work, the presenter
classes must **inherit from the AbstractPresenter** class.

**AbstractPresenter** has several methods to open new presenters,
close the current presenter and to handle certain flows within the
application, such as when a presenter is going to be initialized, hidden,
or closed.

### The flow of events in a class that inherits from AbstractPresenter is like this:

![flow_of_calls_on_presenter](https://github.com/R0land013/easy-mvp/blob/b2c8ba51e5315679848925967611e1e5931871dd/readme_img/flow_of_calls_on_presenter.png?raw=true)

The **_on_initialize** method is the first method called in the **AbstractPresenter** class.
Here the instance variables of the presenter must be initialized. Also, you must
create the instance of the view that corresponds to the presenter. Once created,
the view instance must be set with the **_set_view(view)** method, from
this way the view is made accessible to the rest of the classes in **easy_mvp environment**.
The view can be obtained with the **view** property or **get_view** method of **AbstractPresenter**, if it was set
by **_set_view(view)** first.

The **on_view_shown** method is called just after the presenter view
is displayed in the graphical interface. In this method the data should be loaded,
and the tables and forms filled.

If on the presenter whose view is visible, **_open_other_presenter** is called
then another presenter will be created, and this presenter will go to the top of the
**stack of presenters**, and its view will be the only one visible in the graphical interface.
The view of presenter that called **_open_other_presenter** will no longer be visible.
Before this last occurs, the calling presenter will receive control of the program
with the method **on_view_covered**.

If now the top presenter calls _**close_this_presenter**, then the
presenter view just below it will be visible again, and the
presenter will receive control of the main thread via **on_view_discovered**.
In this method the view should be updated due to some change in the model.

When the presenter at the top of the stack calls **_close_this_presenter**
receives the control with the **on_closing_presenter** method. In this method
resources should be released and observers removed. After the call to
**on_closing_presenter** the presenter and the view of the presenter will be
removed, and it will happen what it has been explained previously.
It should be noted that if the presenter who closes is the
only one that exists in the entire application, that is, there is only one
window, and it owns only a presenter then the application will close with
the **status code 0**. To close the program with different code, use the **exit_app**
method of AbstractPresenter.

### Receiving data from presenters

A presenter can receive data from another presenter that it has created,
if the second one is closed using the **_close_this_presenter_with_result(result_data: dict, result: str = Intent.NO_RESULT)**
method. In this way, the presenter that is below in the stack receives control of the
program via **on_view_discovered_with_result(action: str, data: dict, result: str)** instead of
**on_view_discovered**. The action parameter is the action that was passed to the **Intent** when
it was ordered to open the new presenter. The result_data is a **Python dictionary** that the
presenter who was on top can pass through
**_close_this_presenter_with_result(result_data: dict, result: str = Intent.NO_RESULT)**. The result string can be used
to tell the below presenter what happened on top presenter. In this way the below presenter can take different decisions
depending on the result returned by top presenter.

### Managing global data

Data can be created to be accessible throughout the entire application. This is
accomplished with the **set_global_data(key: str, data)** and **get_global_data(key: str)**
methods of **AbstractPresenter**. You can also check if a global data exists with the method
**has_global_data(key: str)**, which returns True if it exists and False otherwise.

## Knowing Intent in depth

As explained **Intent** is what makes it possible to open new presenters. You can specify
that the new presenter must be opened on a new window using
**use_new_window(use_new_window: bool = False)**. You can also specify that
if a new window is to be opened, then make it modal or not with the method
**use_modal(self, modal: bool = False)**.

An intent can be specified with an action with **set_action(action: str)**, like so
the new presenter may behave differently depending on the action received.

**Intent** also allows data to be passed to a new presenter via **set_data(data: dict)**.
To see examples of how **Intent** is used, check out the ``demo.py`` program.

## Acting when user closes window

If the user clicks the close window button then all presenters in the
presenter stack of the window will receive the **on_window_closing(self)**
call. The first presenter to receive the call will be the one which is
on the stack top, the next to receive the call will be the below presenter.
This flow of calls will occur all the way down through the window stack.
When all presenters have executed **on_window_closing(self)** then the
window will be closed. If the window that is being closing has child
windows, then all its children will receive the **on_window_closing(self)**
calls in the same way the parent window received it.

This method is useful to close database connections, close files and
stop threads. All you must close goes here.

## Customize window title

Every presenter can change the window title. This is useful because each presenter will do
a different task, and therefore you would like to change the title of the window depending
on it.

You can reimplement the method **get_default_window_title(self)** to set a custom
window title. You only have to set **return 'My custom window title'** in the method's
body. This method will be called before the presenter receives the
***on_view_show***, ***on_view_discovered*** and ***on_view_discovered_with_result*** calls.
By default, this method returns the *'No Title, reimplement get_default_window_title'* string.

But if you want more power on changing the window title you can use the
**_set_window_title(self, window_title: str)** to immediately change it. After calling
this method the window title can be replaced automatically if the presenter who set it is popped,
or if a new presenter is added on top. This will happen because of the calls to
**get_default_window_title(self)** on below presenter or on the new presenter respectively,
during the **easy-mvp** event flow.

## Setting application name and window Icon

You can set the application name and Window Icon by passing this information to
ApplicationManager constructor:

````python
manager = ApplicationManager(
    app_name='easy_mvp demo',
    window_icon_path='./demo/view/ui/assets/icon.png'
)
````

This way the operating system will know the name of your app and its window icon.
