import logging, logging.handlers
from utils import get_logs_dir, args

# Create main logger
logger = logging.getLogger('Main')
logger.setLevel(logging.DEBUG)


# Set up logging to terminal
s_handler = logging.StreamHandler()
s_handler.setFormatter(logging.Formatter(
    '[%(levelname)-8s] %(module)-13s : %(message)s'))

if not args.debug:
    s_handler.setLevel(logging.INFO)

logger.addHandler(s_handler)


# Set up logging to file
folder = get_logs_dir()
file = folder.joinpath('log.txt')

f_handler = logging.handlers.TimedRotatingFileHandler(
    file, when='D', interval=1, backupCount=5)

f_handler.setFormatter(logging.Formatter(
    '%(asctime)s [%(levelname)-8s] %(module)-13s : %(message)s'))
f_handler.setLevel(logging.DEBUG)

logger.addHandler(f_handler)