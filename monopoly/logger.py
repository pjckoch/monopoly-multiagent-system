import logging
from enum import Enum
from data_manager import getTime

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
formatter = logging.Formatter('%(envtime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


def log_investment(time, investor, company, invest_value):
    time = getTime(days)
    log_msg = str(investor)
    log_msg += ' invested '
    log_msg += str(invest_value)
    log_msg += ' in '
    log_msg += str(company.name)
    logger.info(log_msg, extra={'envtime': str(time)})

def log_acquireCompany(time, buyer, seller, company, price):
    time = getTime(days)
    log_msg = str(buyer.id)
    log_msg += ' bought '
    log_msg += str(company.name)
    log_msg += ' from '
    log_msg += str(seller.id)
    log_msg += 'for '
    log_msg += str(price)
    logger.info(log_msg, extra = {'envtime': str(time)})

def log_createCompany(time, creator, company):
    time = getTime(days)
    log_msg = str(creator.id)
    log_msg += ' created a new company with name '
    log_msg += str(company.name)
    logger.info(log_msg, extra = {'envtime': str(time)})

def log_auction(time, company, buyer, seller):
    time = getTime(days)
    log_msg = str(buyer.id)
    log_msg += ' bought '
    log_msg += str(company.name)
    log_msg += ' in an auction. Previous owner: '
    log_msg += str(seller)
    logger.info(log_msg, extra = {'envtime': str(time)}

def log_election(time, president, strategy):
    time = getTime(days)
    log_msg = 'We have a new president! ' 
    log_msg += str(president.name)
    log_msg += ' won the election! He is known to support '
    log_msg += str(strategy)
    log_msg += ' fiscal politics.'
    logger.info(log_msg, extra = {'envtime': str(time)}

def log_epidemy(time, epidemytype, deathcount):
    time = getTime(days)
    log_msg = str(deathcount)
    log_msg += ' businessmen left their lives due to '    
    log_msg += str(epidemy)
    logger.info(log_msg, extra = {'envtime': str(time)}