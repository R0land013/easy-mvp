from PyQt5.QtWidgets import QApplication
from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent
from easy_mvp.window import Window


class ApplicationManager:

    def __init__(self):
        self.__initial_intent = None
        self.__window_stack = []
        self.__app = QApplication([])

    def set_initial_intent(self, intent: Intent):
        self.__initial_intent = intent

    def add_new_window(self, intent: Intent, calling_presenter: AbstractPresenter = None):
        window = Window(self)
        window.add_presenter(intent)
        self.__window_stack.append(window)
        window.show()

    def pop_presenter(self, calling_presenter: AbstractPresenter):
        pass

    def execute_app(self):
        window = Window(self)
        window.add_presenter(self.__initial_intent)

        self.__window_stack.append(window)
        window.show()
        self.__app.exec()

