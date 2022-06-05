from demo.presenter.second_presenter import SecondPresenter
from demo.view.first_view import FirstView
from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent


class FirstPresenter(AbstractPresenter):

    def _on_initialize(self):
        view = FirstView(self)
        self._set_view(view)
        self.__message = 'Hello, {}!'
        view.set_message(self.__message.format('Unknown'))

    def open_second_screen(self):
        intent = Intent(SecondPresenter)
        data = {}
        data[SecondPresenter.GREETING_NAME] = self.get_view().get_name()
        intent.set_data(data)
        self._open_other_presenter(intent)

    def change_greeting_name(self):
        view = self.get_view()
        name = view.get_name()
        view.set_message(self.__message.format(name))
