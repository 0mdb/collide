import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from sqlalchemy import create_engine
from app.core.config import settings

# use sync engine for checking db is awake
# TODO move to settings
uri = "postgresql://postgres:changethis@db:5432/app"
engine = create_engine(uri, pool_pre_ping=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        logger.info("Checking DB is awake")
        con = engine.connect()
        con.execute("SELECT 1")
        logger.info("DB is awake")
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
