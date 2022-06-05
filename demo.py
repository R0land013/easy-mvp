from demo.presenter.first_presenter import FirstPresenter
from easy_mvp.application_manager import ApplicationManager
from easy_mvp.intent import Intent


manager = ApplicationManager()
intent = Intent(FirstPresenter)
manager.set_initial_intent(intent)
manager.execute_app()
