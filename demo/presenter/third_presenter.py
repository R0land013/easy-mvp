from demo.presenter.fourth_presenter import FourthPresenter
from demo.view.third_view import ThirdView
from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent


class ThirdPresenter(AbstractPresenter):

    GREETING_NAME = 'name'

    def _on_initialize(self):

        view = ThirdView(self)
        self._set_view(view)
        self.__name = self._get_intent_data()[self.GREETING_NAME]

    def on_view_shown(self):
        message = 'Hello from new window, {}!'.format(self.__name)
        self.get_view().set_message(message)

    def open_fourth_presenter(self):
        intent = Intent(FourthPresenter)
        data = {FourthPresenter.GREETING_NAME: self.__name}
        intent.set_data(data)
        self._open_other_presenter(intent)

    def close(self):
        data = {self.GREETING_NAME: self.__name}
        self._close_this_presenter_with_result(data)

    def on_view_discovered_with_result(self, action: str, result_data: dict):
        self.__name = result_data[FourthPresenter.GREETING_NAME]
        message = 'Hello from new window, {}!'.format(self.__name)
        self.get_view().set_message(message)

