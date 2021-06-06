import configparser
import logging
import os

logger = logging.getLogger(__name__)


def get_config():
    config = configparser.ConfigParser()
    config.optionxform = str
    app_config = config.read(os.environ.get('LOGIN_APP_CONFIG_FILE'), 'application.conf')
    config.read(app_config)
    return config['DEFAULT']
