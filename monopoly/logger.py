import logging
from enum import Enum
import data_manager

# create logger with 'spam_application'
logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('timeline.log', mode='w')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(envtime)s - %(logtype)s: %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

def get_log_argument_dict(time, logtype):
    return {'envtime': '['+str(time)+']', 'logtype': str(logtype.name)}

def log_investment(days, investor, company, invest_value):
    time = data_manager.getTime(days)
    log_msg = str(investor)
    log_msg += ' invested '
    log_msg += str(invest_value)
    log_msg += ' in '
    log_msg += str(company.name)
    logger.info(log_msg, extra= get_log_argument_dict(time, Logtype.INVESTMENT))

def log_acquireCompany(days, buyer, seller, company, price):
    time = data_manager.getTime(days)
    log_msg = 'BM '
    log_msg += str(buyer.id)
    log_msg += ' bought '
    log_msg += str(company.name)
    log_msg += ' from BM '
    log_msg += str(seller.id)
    log_msg += ' for '
    log_msg += str(price)
    logger.info(log_msg, extra= get_log_argument_dict(time, Logtype.ACQUIRE_COMPANY))

def log_createCompany(days, creator, company):
    time = data_manager.getTime(days)
    log_msg = str(creator.id)
    log_msg += ' created a new company with name '
    log_msg += str(company.name)
    logger.info(log_msg, extra= get_log_argument_dict(time, Logtype.CREATE_COMPANY))

def log_auction(days, company, buyer, seller):
    time = data_manager.getTime(days)
    log_msg = 'BM '
    log_msg += str(buyer.id)
    log_msg += ' bought '
    log_msg += str(company.name)
    log_msg += ' in an auction. Previous owner: BM '
    log_msg += str(seller)
    logger.info(log_msg, extra= get_log_argument_dict(time, Logtype.AUCTION))

def log_election(days, president, strategy):
    time = data_manager.getTime(days)
    log_msg = 'We have a new president! ' 
    log_msg += str(president.name)
    log_msg += ' won the election! He is known to support '
    log_msg += str(strategy)
    log_msg += ' fiscal politics.'
    logger.info(log_msg, extra= get_log_argument_dict(time, Logtype.ELECTION))

def log_epidemy(days, epidemytype, deathcount):
    time = data_manager.getTime(days)
    log_msg = str(deathcount)
    log_msg += ' businessmen left their lives due to '    
    log_msg += str(epidemy)
    logger.info(log_msg, extra= get_log_argument_dict(time, Logtype.EPIDEMY))

class Logtype(Enum):
    INVESTMENT = 1
    ACQUIRE_COMPANY = 2
    CREATE_COMPANY = 3
    AUCTION = 4
    ELECTION = 5
    EPIDEMY = 6