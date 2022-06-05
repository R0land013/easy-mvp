from demo.presenter.first_presenter import FirstPresenter
from easy_mvp.presenter_manager import PresenterManager


manager = PresenterManager()
manager.set_initial_presenter(FirstPresenter)
manager.execute_app()
