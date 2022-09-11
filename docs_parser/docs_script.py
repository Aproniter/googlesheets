import sys
import os

from datetime import datetime
from dotenv import load_dotenv

logger_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/logger/')
data_helper_dir = (os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
+ '/data_helper/')

sys.path.append(data_helper_dir)
sys.path.append(logger_dir)


from logger import Logger
from db import DbHelper
from sheets_script import SheetsHelper

load_dotenv()
logger = Logger(__name__, 'docs_script').get_logger()
sheets_helper = SheetsHelper()
ws = sheets_helper.get_worksheet()
db = DbHelper()


def get_new_data():
    print(ws.get_all_records())

get_new_data()