import os
import logging
import datetime
import news_scraper_update.utils.constants as constants


def set(name):
    # make a new log file for each day for clear understanding of logs
    today_date = datetime.date.today().strftime('%Y-%m-%d_%H-%M-%S')
    # log_file = constants.ROOT_DIR + '/log/' + today_date + '.txt'
    log_file = constants.ROOT_DIR + '/log/' + today_date + '.txt'
    # make the log file if it doesn't exist
    if not os.path.exists(log_file):
        file = open(log_file, 'w+')
        # close the file if it was made
        file.close()

    # set the logging config
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file)
    # logger = logging.basicConfig(filename=log_file, level=logging.INFO)
    log_format = '%(asctime)s|%(name)s|%(levelname)s|MSG: %(msg)s'
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
