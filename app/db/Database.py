from app import setup_logger

logger = setup_logger(__name__)


class Database:
    def __init__(self):
        logger.info("Init db")
        pass
