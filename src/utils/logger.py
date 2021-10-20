import logging, logging.handlers
from utils import get_program_dir, args

logger = logging.getLogger('Main')
logger.setLevel(logging.DEBUG)

s_handler = logging.StreamHandler()
s_handler.setFormatter(logging.Formatter(
    '[%(levelname)-8s] %(module)-13s : %(message)s'))

if not args.debug:
    s_handler.setLevel(logging.INFO)

logger.addHandler(s_handler)


folder = get_program_dir().joinpath('logs')
if not folder.is_dir(): folder.mkdir()
file = folder.joinpath('log.txt')

f_handler = logging.handlers.TimedRotatingFileHandler(
    file, when='D', interval=1, backupCount=5)

f_handler.setFormatter(logging.Formatter(
    '%(asctime)s [%(levelname)-8s] %(module)-13s : %(message)s'))
f_handler.setLevel(logging.DEBUG)

logger.addHandler(f_handler)