from PyQt5.QtWidgets import QApplication
from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.exception import NoGlobalDataWithKeyException
from easy_mvp.intent import Intent
from easy_mvp.window import WindowHandler
import sys

class ApplicationManager:

    def __init__(self, app_name: str = 'No Name', window_icon_path: str = None):
        self.__window_stack = []
        self.__app = QApplication(sys.argv)
        self.__global_data = {}
        self.__window_icon_path = window_icon_path

        self.__app.setApplicationName(app_name)

    def add_new_window(self, intent: Intent, parent_window: WindowHandler, calling_presenter: AbstractPresenter):
        window = WindowHandler(self, parent_window)
        window.add_presenter(intent, calling_presenter)
        self.__window_stack.append(window)
        window.show()

    def remove_window(self, window: WindowHandler):
        self.__window_stack.remove(window)

    def execute_app(self, initial_intent: Intent):
        window = WindowHandler(self, window_icon_path=self.__window_icon_path)
        window.add_presenter(initial_intent)

        self.__window_stack.append(window)
        window.show()
        self.__app.exec()

    def exit(self, code: int = 0):
        self.__app.exit(code)

    def set_global_data(self, key: str, data):
        self.__global_data[key] = data

    def get_global_data(self, key: str):
        if key not in self.__global_data:
            raise NoGlobalDataWithKeyException(key)
        return self.__global_data[key]

    def has_global_data(self, key: str) -> bool:
        return key in self.__global_data
