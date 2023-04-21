from easy_mvp.intent import Intent


class AbstractPresenter:

    def __init__(self, intent: Intent, window, app_manager):
        self.__intent = intent
        self.__window_handler = window
        self.__app_manager = app_manager
        self.__view = None
        self._on_initialize()

    @property
    def view(self):
        return self.__view

    def get_view(self):
        return self.__view

    def _set_view(self, view):
        self.__view = view

    def _open_other_presenter(self, intent: Intent):
        if intent.is_using_new_window():
            self.__app_manager.add_new_window(intent,
                                              parent_window=self.__window_handler,
                                              calling_presenter=self)
        else:
            self.__window_handler.add_presenter(intent, self)

    def _close_this_presenter(self):
        self.__window_handler.pop_presenter(self)

    def _close_this_presenter_with_result(self, result_data: dict, result: str = Intent.NO_RESULT):
        self.__window_handler.pop_presenter_with_result(self.__intent,
                                                        calling_presenter=self,
                                                        result_data=result_data,
                                                        result=result)

    def _on_initialize(self):
        pass

    def on_view_shown(self):
        pass

    def on_view_covered(self):
        pass

    def on_view_discovered(self):
        pass

    def on_view_discovered_with_result(self, action: str, result_data: dict, result: str):
        pass

    def on_closing_presenter(self):
        pass

    def _get_intent_data(self) -> dict:
        return self.__intent.get_data()

    def _get_intent_action(self) -> str:
        return self.__intent.get_action()

    def exit_app(self, code: int = 0):
        self.__window_handler.exit_app(code)

    def set_global_data(self, key: str, data):
        self.__app_manager.set_global_data(key, data)

    def get_global_data(self, key: str):
        return self.__app_manager.get_global_data(key)

    def has_global_data(self, key: str) -> bool:
        return self.__app_manager.has_global_data(key)

    def get_default_window_title(self) -> str:
        # This method will be called before the presenter receives the
        # on_view_show, on_view_discovered and on_view_discovered_with_result
        # calls.
        return 'No Title, reimplement get_default_window_title'

    def _set_window_title(self, window_title: str):
        self.__window_handler.set_window_title(window_title)

    def on_window_closing(self):
        pass
