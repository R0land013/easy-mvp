from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class FourthView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        loadUi('./demo/view/ui/fourth.ui', self)

        self.back_button.clicked.connect(presenter.go_back)
