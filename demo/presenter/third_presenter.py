from demo.presenter.fourth_presenter import FourthPresenter
from demo.view.third_view import ThirdView
from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent


class ThirdPresenter(AbstractPresenter):

    GREETING_NAME = 'name'

    def _on_initialize(self):

        view = ThirdView(self)
        self._set_view(view)

    def on_view_shown(self):
        name = self._get_intent_data()[self.GREETING_NAME]
        message = 'Hello from new window, {}!'.format(name)
        self.get_view().set_message(message)

    def open_fourth_presenter(self):
        self._open_other_presenter(Intent(FourthPresenter))

    def close(self):
        self._close_this_presenter()
