import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

preferred_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(getattr(logging, 'DEBUG'))
stream_handler.setFormatter(preferred_format)

file_handler = logging.FileHandler('maple.log')
file_handler.setLevel(getattr(logging, 'DEBUG'))
file_handler.setFormatter(preferred_format)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)