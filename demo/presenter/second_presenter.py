from demo.view.second_view import SecondView
from easy_mvp.abstract_presenter import AbstractPresenter


class SecondPresenter(AbstractPresenter):

    GREETING_NAME = 'name'

    def _on_initialize(self):
        view = SecondView(self)
        self._set_view(view)
        intent_data = self._get_intent_data()
        name_from_first_presenter = intent_data[self.GREETING_NAME]
        message = 'Hello again {}!'.format(name_from_first_presenter)
        view.set_message(message)

    def return_to_first_presenter(self):
        self._close_this_presenter()
