

class BelowPresenterDoingCommandsException(Exception):

    def __init__(self):
        super().__init__('A presenter which is below in the stack is doing commands.\n' +
                         'For safety and clarity it is not possible for a below presenter\n' +
                         'to do commands. The top presenter is the only one who can do\n' +
                         'commands. In this way the stack model is always reached.')


class NoBelowPresenterToBeNotifiedWithResultException(Exception):

    def __init__(self):
        super().__init__('A presenter can not be closed with result if there is not a below\n' +
                         'presenter on the same window. If there is not below presenter then\n' +
                         'it is necessary to the presenter\'s window to have a parent window.')


class NoGlobalDataWithKeyException(Exception):

    def __init__(self, key: str):
        super().__init__('No global data with key {}.'.format(key))
