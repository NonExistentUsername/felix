from controllers import TelegramPetsMainController
from core.database import init_database

init_database()

telegram_pets_main_controller = TelegramPetsMainController()

telegram_pets_main_controller.start()
