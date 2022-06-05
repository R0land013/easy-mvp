from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget

from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent


class PresenterManager:

    def __init__(self):
        self.__initial_presenter_class = None
        self.__presenter_stack = []
        self.__app = QApplication([])
        self.__window = QStackedWidget()

    def set_initial_presenter(self, presenter: AbstractPresenter):
        self.__initial_presenter_class = presenter

    def push_presenter(self, intent: Intent, calling_presenter: AbstractPresenter):

        top_presenter = self.__presenter_stack[-1]
        top_presenter.on_view_covered()

        new_presenter_class = intent.get_presenter_class()
        new_presenter = new_presenter_class(intent, self)

        self.__presenter_stack.append(new_presenter)
        self.__window.addWidget(new_presenter.get_view())
        self.__window.setCurrentWidget(new_presenter.get_view())

        new_presenter.on_view_shown()

    def pop_presenter(self, calling_presenter: AbstractPresenter):
        top_presenter = self.__presenter_stack.pop(-1)
        top_presenter.on_closing_presenter()

        under_presenter = self.__presenter_stack[-1]
        self.__window.setCurrentWidget(under_presenter.get_view())

    def execute_app(self):
        presenter = self.__initial_presenter_class(Intent(self.__initial_presenter_class), self)
        self.__presenter_stack.append(presenter)
        self.__window.addWidget(presenter.get_view())
        self.__window.setCurrentWidget(presenter.get_view())
        self.__window.show()
        self.__app.exec()
