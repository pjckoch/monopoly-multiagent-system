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

# create logger with 'spam_application'
logger2 = logging.getLogger('spam_application2')
logger2.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh2 = logging.FileHandler('businessman_sales.log', mode='w')
fh2.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch2 = logging.StreamHandler()
ch2.setLevel(logging.ERROR)
# add formatter to the handlers
fh2.setFormatter(formatter)
ch2.setFormatter(formatter)
# add the handlers to the logger
logger2.addHandler(fh2)
logger2.addHandler(ch2)

# create logger with 'spam_application'
logger3 = logging.getLogger('spam_application3')
logger3.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh3 = logging.FileHandler('company_sales.log', mode='w')
fh3.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch3 = logging.StreamHandler()
ch3.setLevel(logging.ERROR)
# add formatter to the handlers
fh3.setFormatter(formatter)
ch3.setFormatter(formatter)
# add the handlers to the logger
logger3.addHandler(fh3)
logger3.addHandler(ch3)

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
    log_msg = 'BM '
    log_msg += str(creator.id)
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

# Sales Logger Functions

def testLog(days):
    time = data_manager.getTime(days)
    log_msg = 'Buenos Dias Matosinhos'
    logger2.info(log_msg, extra= get_log_argument_dict(time, Logtype.SALES_INFO))

# TODO: Sales and Costs functions per Businessman and per Company

def log_businessman_sales(days, bm):
    sales = 0
    turnover = 0
    for company in bm.companies:
        sales += len(company.companySales)
        turnover += len(company.companySales) * company.price
    
    time = data_manager.getTime(days)
    log_msg = 'Businessman with the ID: '
    log_msg += str(bm.id)
    log_msg += ' had a number of: '
    log_msg += str(sales)
    log_msg += ' consumers. Turnover: '
    log_msg += str(turnover)
    logger2.info(log_msg, extra= get_log_argument_dict(time, Logtype.SALES_INFO))

def log_split(days):
    time = data_manager.getTime(days)
    logger2.info('-------------------------------', extra= get_log_argument_dict(time, Logtype.SALES_INFO))

# Not sure if useful function

# def log_businessman_cost(days, bm):
#     cost = 0
#     turnover = 0
#     for company in bm.companies:
#         cost += len(company.companySales)
#         turnover += len(company.companySales) * company.price

def log_company_sales(days, company):
    time = data_manager.getTime(days)
    log_msg = 'Company with the ID: '
    log_msg += str(company.id)
    log_msg += ' had a number of: '
    log_msg += str(len(company.companySales))
    log_msg += ' consumers'
    logger3.info(log_msg, extra= get_log_argument_dict(time, Logtype.SALES_INFO))

# Not sure if useful function

# def log_company_cost(days, company):
#     return
    

class Logtype(Enum):
    INVESTMENT = 1
    ACQUIRE_COMPANY = 2
    CREATE_COMPANY = 3
    AUCTION = 4
    ELECTION = 5
    EPIDEMY = 6
    SALES_INFO = 7
    COSTS_INFO = 8