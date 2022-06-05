from easy_mvp.intent import Intent


class AbstractPresenter:

    def __init__(self, intent: Intent, manager):
        self.__intent = intent
        self.__manager = manager
        self.__view = None
        self._on_initialize()

    def get_view(self):
        return self.__view

    def _set_view(self, view):
        self.__view = view

    def _open_other_presenter(self, intent: Intent):
        self.__manager.push_presenter(intent, self)

    def _close_this_presenter(self):
        self.__manager.pop_presenter(self)

    def _on_initialize(self):
        pass

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
