from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class SecondView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        loadUi('./demo/view/ui/second.ui', self)
        self.back_button.clicked.connect(presenter.return_to_first_presenter)
        self.open_window_button.clicked.connect(presenter.open_new_window)

    def set_message(self, text: str):
        self.message_label.setText(text)
