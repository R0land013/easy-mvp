

class BelowPresenterDoingCommandsException(Exception):

    def __init__(self):
        super().__init__('A presenter which is below in the stack is doing commands.\n' +
                         'For safety and clarity it is not possible for a below presenter\n' +
                         'to do commands. The top presenter is the only one who can do\n' +
                         'commands. In this way the stack model is always reached.')
