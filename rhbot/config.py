import os
import sys
import yaml
import logging
import datetime

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_FILE = os.path.join(ROOT_DIR, 'config.yaml')
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

log_filename = datetime.datetime.now().strftime('RHBot-%Y-%m-%d_%H-%M-%S.log')
log_path = os.path.join(LOG_DIR, log_filename)

formatter = logging.Formatter(
    fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler = logging.FileHandler(log_path, encoding='utf-8')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(file_handler)
root_logger.addHandler(stream_handler)

logger = logging.getLogger('RHBot')

with open(CONFIG_FILE) as f:
    config = yaml.safe_load(f)

DISCORD_TOKEN = config['discord_token']
OPENROUTER_API_KEY = config['openrouter_api_key']
ANTHROPIC_API_KEY = config['anthropic_api_key']
DEVELOPER_ID = int(config['developer_id'])
DEVELOPER_USERNAME = config['developer_username']

