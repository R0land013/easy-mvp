

class Intent:

    def __init__(self, presenter_class: type):
        self.__presenter_data = {}
        self.__presenter_action = None
        self.__presenter_class = presenter_class

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
