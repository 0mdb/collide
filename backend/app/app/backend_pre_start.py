import logging

from sqlalchemy import create_engine
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.core.config import settings
from app.crud.memgraph_make_graph import conn

# use sync engine for checking db is awake
# TODO move to settings
uri = "postgresql://postgres:changethis@db:5432/app"
engine = create_engine(uri, pool_pre_ping=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


def check_postgres() -> None:
        logger.info("Checking DB is awake")
        con = engine.connect()
        con.execute("SELECT 1")
        logger.info("DB is awake")
        con.close()


def check_memgraph() -> None:
        cursor = conn.cursor()
        logger.info("Checking Memgraph is awake")
        cursor.execute('MATCH (n: MGPerson {match_name: "waynewouters"}) RETURN n')
        val = cursor.fetchone()
        cursor.close()
        logger.info("Memgraph is awake")

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        check_postgres()
        check_memgraph()
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
