from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class ThirdView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        loadUi('./demo/view/ui/third.ui', self)

        self.go_fourth_screen_button.clicked.connect(presenter.open_fourth_presenter)
        self.close_window_button.clicked.connect(presenter.close)

    def set_message(self, message: str):
        self.message_label.setText(message)
