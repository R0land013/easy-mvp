from demo.view.fourth_view import FourthView
from easy_mvp.abstract_presenter import AbstractPresenter


class FourthPresenter(AbstractPresenter):

    CHANGE_NAME_ACTION = 'change_name_action'
    GREETING_NAME = 'name'

    NAME_CHANGED_RESULT = 'name_changed_result'

    def _on_initialize(self):
        view = FourthView(self)
        self._set_view(view)
        self.__name = self._get_intent_data()[self.GREETING_NAME]

    def on_view_shown(self):
        self.view.set_message("Hello one more time, {}!".format(self.__name))

    def change_name(self):
        self.__name = self.view.get_name()
        self.view.set_message("Hello one more time, {}!".format(self.__name))

    def go_back(self):
        if self.__is_name_changed():
            result_data = {}
            result_data[self.GREETING_NAME] = self.__name
            self._close_this_presenter_with_result(result_data, result=self.NAME_CHANGED_RESULT)
        else:
            self._close_this_presenter()

    def __is_name_changed(self) -> bool:
        return self._get_intent_data()[self.GREETING_NAME] != self.__name

    def on_window_closing(self):
        print('Cleaning FourthPresenter...')
