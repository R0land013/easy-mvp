from demo.presenter.first_presenter import FirstPresenter
from easy_mvp.application_manager import ApplicationManager
from easy_mvp.intent import Intent


manager = ApplicationManager(
    app_name='easy_mvp demo',
    window_icon_path='./demo/view/ui/assets/icon.png'
)
intent = Intent(FirstPresenter)
manager.execute_app(intent)
