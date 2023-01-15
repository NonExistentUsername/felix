from controllers import TelegramPetsMainController

telegram_pets_main_controller = TelegramPetsMainController()

from core.database import init_database

init_database()

telegram_pets_main_controller.start()
