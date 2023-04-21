from demo.presenter.third_presenter import ThirdPresenter
from demo.view.second_view import SecondView
from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent


class SecondPresenter(AbstractPresenter):

    GREETING_NAME = 'name'

    def _on_initialize(self):
        view = SecondView(self)
        self._set_view(view)

        self.__name = self._get_intent_data()[self.GREETING_NAME]
        message = 'Hello again {}!'.format(self.__name)
        view.set_message(message)

    def return_to_first_presenter(self):
        data = {self.GREETING_NAME: self.__name}
        self._close_this_presenter_with_result(data)

    def open_new_window(self):
        intent = Intent(ThirdPresenter)
        intent.use_new_window(True)
        intent.use_modal(True)

        data = {ThirdPresenter.GREETING_NAME: self.__name}
        intent.set_data(data)
        self._open_other_presenter(intent)

    def on_view_discovered_with_result(self, action: str, result_data: dict, result: str):
        self.__name = result_data[ThirdPresenter.GREETING_NAME]
        message = 'Hello again {}!'.format(self.__name)
        self.view.set_message(message)
        self._set_window_title(message)

    def get_default_window_title(self) -> str:
        return 'Second view, Hello again {}'.format(self.__name)

    def on_window_closing(self):
        print('Cleaning SecondPresenter...')
