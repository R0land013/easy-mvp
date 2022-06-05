from demo.presenter.third_presenter import ThirdPresenter
from demo.view.second_view import SecondView
from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent


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

    def open_new_window(self):
        intent = Intent(ThirdPresenter)
        intent.use_new_window(True)
        intent.use_modal(True)

        name = self._get_intent_data()[self.GREETING_NAME]
        data = {ThirdPresenter.GREETING_NAME: name}
        intent.set_data(data)
        self._open_other_presenter(intent)
