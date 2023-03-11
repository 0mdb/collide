import asyncio
import logging

from app.db.init_db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:

    logger.info("Creating database and tables")
    asyncio.run(init_db())
    logger.info("Database and tables created")


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
