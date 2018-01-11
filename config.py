import configparser
import os
import logging

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

conf = configparser.RawConfigParser()
conf.read(str(os.getcwd())+"/config.properties")

def get_token():
    try:
        return conf.get("telegramBot", "token")
    except configparser.NoSectionError as err:
        logging.error(u'' + str(err) + '')