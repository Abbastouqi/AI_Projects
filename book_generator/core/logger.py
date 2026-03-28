import sys
from loguru import logger

logger.remove()
logger.add(sys.stdout, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} | {message}", level="INFO")
logger.add("logs/book_generator.log", rotation="10 MB", retention="14 days", level="DEBUG")
