import os
import gspread

from gspread import Worksheet
from dotenv import load_dotenv

load_dotenv()


class SheetsHelper:
    """Класс для работы с документом GoogleSheets.
    При инициализации принимает путь
    до данных авторизации сервисного аккаунта Google(по умолчанию
    '<путь до папки проекта>/.config/service_account.json')
    и название документа для работы(по умолчанию 'test')"""

    def __init__(
        self,
        book_name:str='test',
        service_account_settings_file_path:str=os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            '..',
            '.config',
            'service_account.json'
        )
    ):
        self.sas_file = service_account_settings_file_path
        self.service_account = gspread.service_account(
            filename=self.sas_file
        )
        self.sheet_handler = self.service_account.open(book_name)

    def get_worksheet(self, sheet_name:str='Лист1')-> Worksheet:
        """Принимает название листа, возращает объект для работы с листом"""
        return self.sheet_handler.worksheet(sheet_name)


if __name__ == '__main__':
    sh = SheetsHelper()
    ws = sh.get_worksheet()
    print(ws.get_all_records())
