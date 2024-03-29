from demo.presenter.second_presenter import SecondPresenter
from demo.view.first_view import FirstView
from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent


class FirstPresenter(AbstractPresenter):

    def _on_initialize(self):
        view = FirstView(self)
        self._set_view(view)
        self.__message = 'Hello, {}!'
        self.__name = 'Unknown'
        view.set_message(self.__message.format(self.__name))

    def open_second_screen(self):
        intent = Intent(SecondPresenter)
        data = {}
        data[SecondPresenter.GREETING_NAME] = self.__name
        intent.set_data(data)
        self._open_other_presenter(intent)

    def change_greeting_name(self):
        view = self.view
        self.__name = view.get_name()
        view.set_message(self.__message.format(self.__name))
        self._set_window_title(self.__message.format(self.__name))

    def close(self):
        self._close_this_presenter()

    def on_view_discovered_with_result(self, action: str, result_data: dict, result: str):
        self.__name = result_data[SecondPresenter.GREETING_NAME]
        self.view.set_message(self.__message.format(self.__name))
        self._set_window_title(self.__message.format(self.__name))

    def get_default_window_title(self) -> str:
        return 'First View'

    def on_window_closing(self):
        print('Cleaning FirstPresenter...')
