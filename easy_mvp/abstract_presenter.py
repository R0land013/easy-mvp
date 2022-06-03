from easy_mvp.intent import Intent
from easy_mvp.presenter_manager import PresenterManager


class AbstractPresenter:

    def __init__(self, intent: Intent, manager: PresenterManager):
        self.__intent = intent
        self.__manager = manager

    def get_view(self):
        pass

    def _open_other_presenter(self, intent: Intent):
        self.__manager.push_presenter(intent, self)

    def _close_this_presenter(self):
        self.__manager.pop_presenter(self)

    def on_view_shown(self):
        pass

    def on_view_covered(self):
        pass

    def on_closing_presenter(self):
        pass

    def _get_intent_data(self) -> dict:
        return self.__intent.get_data()

    def _get_intent_action(self) -> str:
        return self.__intent.get_action()
