from demo.view.fourth_view import FourthView
from easy_mvp.abstract_presenter import AbstractPresenter


class FourthPresenter(AbstractPresenter):

    CHANGE_NAME_ACTION = 'change_name_action'
    GREETING_NAME = 'name'

    def _on_initialize(self):
        view = FourthView(self)
        self._set_view(view)
        self.__name = self._get_intent_data()[self.GREETING_NAME]

    def on_view_shown(self):
        self.get_view().set_message("Hello one more time, {}!".format(self.__name))

    def change_name(self):
        self.__name = self.get_view().get_name()
        self.get_view().set_message("Hello one more time, {}!".format(self.__name))

    def go_back(self):
        result_data = {}
        result_data[self.GREETING_NAME] = self.__name
        self._close_this_presenter_with_result(result_data)
