from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtCore import Qt
from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent


class Window:

    def __init__(self, application_manager):
        self.__presenter_stack = []

        self.__stacked_widget = QStackedWidget()
        self.__app_manager = application_manager

    def add_presenter(self, intent: Intent, calling_presenter: AbstractPresenter = None):
        if self.presenter_count() == 0:
            self.__set_modal(intent.is_using_modal())

        self.__notify_presenter_on_view_covered(calling_presenter)

        self.__add_presenter_and_its_view(intent)
        self.__notify_presenter_on_view_shown()

    def presenter_count(self) -> int:
        return len(self.__presenter_stack)

    def __set_modal(self, modal: bool):
        if modal:
            self.__stacked_widget.setWindowModality(Qt.WindowModality.ApplicationModal)
        else:
            self.__stacked_widget.setWindowModality(Qt.WindowModality.NonModal)

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

    def get_top_presenter(self) -> AbstractPresenter:
        return self.__presenter_stack[-1]

    def pop_presenter(self, calling_presenter: AbstractPresenter) -> AbstractPresenter:
        top_presenter = self.__pop_presenter_and_its_view()
        top_presenter.on_closing_presenter()

        self.__notify_presenter_on_view_shown()
        self.__close_window_if_no_presenter_remains()

        return top_presenter

    def __pop_presenter_and_its_view(self) -> AbstractPresenter:
        top_presenter = self.__presenter_stack.pop(-1)
        self.__stacked_widget.removeWidget(top_presenter.get_view())
        return top_presenter

    def __notify_presenter_on_view_shown(self):
        if len(self.__presenter_stack) >= 1:
            below_presenter = self.get_top_presenter()
            below_presenter.on_view_shown()

    def __close_window_if_no_presenter_remains(self):
        if len(self.__presenter_stack) == 0:
            self.close()

    def close(self):
        self.__app_manager.remove_window(self)
        self.__stacked_widget.close()

    def show(self):
        self.__stacked_widget.show()
