from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtCore import Qt
from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.exception import BelowPresenterDoingCommandsException, NoBelowPresenterToBeNotifiedWithResultException
from easy_mvp.intent import Intent


class StackWindow(QStackedWidget):

    def __init__(self, window_handler):
        super().__init__()
        self.__window_handler = window_handler

    def closeEvent(self, event: QCloseEvent):
        self.__window_handler.close_all_child_windows()


class WindowHandler:

    def __init__(self, application_manager, parent_window=None):
        self.__presenter_stack = []
        self.__parent_window = None
        self.__link_to_parent_window(parent_window)
        self.__stacked_widget = StackWindow(self)
        self.__app_manager = application_manager
        self.__child_windows = []

    def __link_to_parent_window(self, parent_window):
        if parent_window is not None:
            parent_window.add_child_window(self)
        self.__parent_window = parent_window

    def get_base_widget(self) -> QStackedWidget:
        return self.__stacked_widget

    def add_presenter(self, intent: Intent, calling_presenter: AbstractPresenter = None):

        if self.presenter_count() == 0:
            self.__set_modal(intent.is_using_modal())

        self.__check_is_top_presenter(calling_presenter)
        self.__notify_presenter_on_view_covered(calling_presenter)

        self.__add_presenter_and_its_view(intent)
        self.__notify_top_presenter_on_view_shown()

    def presenter_count(self) -> int:
        return len(self.__presenter_stack)

    def __set_modal(self, modal: bool):
        if modal:
            self.__stacked_widget.setWindowModality(Qt.WindowModality.ApplicationModal)
        else:
            self.__stacked_widget.setWindowModality(Qt.WindowModality.NonModal)

    def __check_is_top_presenter(self, presenter: AbstractPresenter):
        if self.presenter_count() >= 1:
            top_presenter = self.get_top_presenter()
            if top_presenter is not presenter:
                raise BelowPresenterDoingCommandsException()

    @staticmethod
    def __notify_presenter_on_view_covered(self, calling_presenter: AbstractPresenter = None):
        if calling_presenter is not None:
            calling_presenter.on_view_covered()

    def __add_presenter_and_its_view(self, intent: Intent):
        presenter_class = intent.get_presenter_class()
        new_presenter = presenter_class(intent, self, self.__app_manager)
        self.__presenter_stack.append(new_presenter)
        self.__stacked_widget.addWidget(new_presenter.get_view())
        self.__stacked_widget.setCurrentWidget(new_presenter.get_view())

    def __notify_top_presenter_on_view_shown(self):
        self.get_top_presenter().on_view_shown()

    def get_top_presenter(self) -> AbstractPresenter:
        return self.__presenter_stack[-1]

    def pop_presenter(self, calling_presenter: AbstractPresenter) -> AbstractPresenter:
        self.__check_is_top_presenter(calling_presenter)

        top_presenter = self.__pop_presenter_and_its_view()
        top_presenter.on_closing_presenter()

        was_window_closed = self.__close_window_if_no_presenter_remains()
        if was_window_closed and self.has_parent_window():
            presenter_of_parent_window = self.__parent_window.get_top_presenter()
            presenter_of_parent_window.on_view_discovered()
        elif self.presenter_count() >= 1:
            below_presenter = self.get_top_presenter()
            below_presenter.on_view_discovered()
        else:
            self.__app_manager.exit()

        return top_presenter

    def __pop_presenter_and_its_view(self) -> AbstractPresenter:
        top_presenter = self.__presenter_stack.pop(-1)
        self.__stacked_widget.removeWidget(top_presenter.get_view())
        return top_presenter

    def __notify_presenter_on_view_discovered(self):
        if len(self.__presenter_stack) >= 1:
            below_presenter = self.get_top_presenter()
            below_presenter.on_view_discovered()

    def __close_window_if_no_presenter_remains(self) -> bool:
        if len(self.__presenter_stack) == 0:
            self.close_window()
            return True
        return False

    def close_window(self):
        self.__stacked_widget.close()
        self.__app_manager.remove_window(self)
        if self.__parent_window is not None:
            self.__parent_window.remove_child_window(self)

    def pop_presenter_with_result(self, intent: Intent, calling_presenter: AbstractPresenter, result_data: dict):
        self.__check_is_top_presenter(calling_presenter)
        self.__check_there_is_below_presenter_to_be_notified_with_result()

        top_presenter = self.__pop_presenter_and_its_view()
        top_presenter.on_closing_presenter()

        was_window_closed = self.__close_window_if_no_presenter_remains()
        if was_window_closed:
            self.__notify_presenter_on_discovered_with_result_on_parent_window(intent, result_data)
        else:
            self.__notify_below_presenter_on_discovered_with_result(intent, result_data)

    def __check_there_is_below_presenter_to_be_notified_with_result(self):
        if self.presenter_count() == 1 and not self.has_parent_window():
            raise NoBelowPresenterToBeNotifiedWithResultException()

    def has_parent_window(self) -> bool:
        return self.__parent_window is not None

    def __notify_presenter_on_discovered_with_result_on_parent_window(self, intent: Intent, result_data: dict):
        parent_window_presenter = self.__parent_window.get_top_presenter()
        parent_window_presenter.on_view_discovered_with_result(intent.get_action(), result_data)

    def __notify_below_presenter_on_discovered_with_result(self, intent: Intent, result_data: dict):
        below_presenter = self.get_top_presenter()
        below_presenter.on_view_discovered_with_result(intent.get_action(), result_data)

    def show(self):
        self.__stacked_widget.show()

    def exit_app(self, code: int = 0):
        self.__app_manager.exit(code)

    def close_all_child_windows(self):
        while len(self.__child_windows) > 0:
            child_window = self.__child_windows[0]
            child_window.close_window()

    def add_child_window(self, child_window):
        self.__child_windows.append(child_window)

    def remove_child_window(self, child_window):
        self.__child_windows.remove(child_window)
