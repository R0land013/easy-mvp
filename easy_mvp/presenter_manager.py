from PyQt5.QtWidgets import QApplication, QWidget, QStackedWidget

from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent


class PresenterManager:

    def __init__(self):
        self.__initial_presenter = None
        self.__presenter_stack = []
        self.__window = QStackedWidget()
        self.__app = QApplication([])

    def set_initial_presenter(self, presenter: AbstractPresenter):
        self.__initial_presenter = presenter

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
        pass

    def execute_app(self):
        self.__presenter_stack.append(self.__initial_presenter)
        self.__window.addWidget(self.__initial_presenter.get_view())
        self.__window.setCurrentWidget(self.__initial_presenter.get_view())
        self.__window.show()
        self.__app.exec_()
