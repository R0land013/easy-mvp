from easy_mvp.intent import Intent


class AbstractPresenter:

    NO_ACTION = 'no_action'

    def __init__(self, intent: Intent, window, app_manager):
        self.__intent = intent
        self.__window = window
        self.__app_manager = app_manager
        self.__view = None
        self._on_initialize()

    def get_view(self):
        return self.__view

    def _set_view(self, view):
        self.__view = view

    def _open_other_presenter(self, intent: Intent):
        self.__set_default_intent_action_if_none(intent)
        if intent.is_using_new_window():
            self.__app_manager.add_new_window(intent,
                                              parent_window=self.__window,
                                              calling_presenter=self)
        else:
            self.__window.add_presenter(intent, self)

    def __set_default_intent_action_if_none(self, intent: Intent):
        intent.set_action(self.NO_ACTION)

    def _close_this_presenter(self):
        self.__window.pop_presenter(self)

    def _close_this_presenter_with_result(self, result_data: dict):
        self.__window.pop_presenter_with_result(self.__intent,
                                                calling_presenter=self,
                                                result_data=result_data)

    def _on_initialize(self):
        pass

    def on_view_shown(self):
        pass

    def on_view_covered(self):
        pass

    def on_view_discovered(self):
        pass

    def on_view_discovered_with_result(self, action: str, data: dict):
        pass

    def on_closing_presenter(self):
        pass

    def _get_intent_data(self) -> dict:
        return self.__intent.get_data()

    def _get_intent_action(self) -> str:
        return self.__intent.get_action()

    def exit_app(self, code: int = 0):
        self.__window.exit_app(code)
