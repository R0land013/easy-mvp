from demo.view.fourth_view import FourthView
from easy_mvp.abstract_presenter import AbstractPresenter


class FourthPresenter(AbstractPresenter):

    def _on_initialize(self):
        view = FourthView(self)
        self._set_view(view)

    def go_back(self):
        self._close_this_presenter()
