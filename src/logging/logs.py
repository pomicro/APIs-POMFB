import logging, os
from datetime import date

today = date.today()
logger = logging.getLogger()
filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs_' + str(today.strftime("%d-%m-%Y")))
fhandler = logging.FileHandler(filename=filename, mode='a')
formatter = logging.Formatter('%(asctime)s||%(levelname)s||%(message)s')
fhandler.setFormatter(formatter)
logger.addHandler(fhandler)
logger.setLevel(logging.DEBUG)