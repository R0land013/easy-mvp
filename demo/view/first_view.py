from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class FirstView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        loadUi('./demo/view/ui/first.ui', self)
        self.go_to_second_button.clicked.connect(presenter.open_second_screen)
        self.change_name_button.clicked.connect(presenter.change_greeting_name)

    def set_message(self, text: str):
        self.name_label.setText(text)

    def get_name(self) -> str:
        return self.name_line_edit.text()
