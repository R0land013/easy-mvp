

class Intent:

    NO_ACTION = 'no_action'

    NO_RESULT = 'no_result'

    def __init__(self, presenter_class: type):
        self.__presenter_data = {}
        self.__presenter_action = self.NO_ACTION
        self.__presenter_class = presenter_class
        self.__use_new_window = False
        self.__use_modal = False

    def get_presenter_class(self) -> type:
        return self.__presenter_class

    def get_data(self) -> dict:
        return self.__presenter_data

    def set_data(self, data: dict):
        self.__presenter_data = data

    def get_action(self) -> str:
        return self.__presenter_action

    def set_action(self, action: str):
        self.__presenter_action = action

    def use_new_window(self, use_new_window: bool = False):
        self.__use_new_window = use_new_window

    def is_using_new_window(self) -> bool:
        return self.__use_new_window

    def use_modal(self, modal: bool = False):
        self.__use_modal = modal

    def is_using_modal(self) -> bool:
        return self.__use_modal
