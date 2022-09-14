"""
Primary functions for orchestrating analysis of Kick Open the Door data
"""
from typing import Optional
from logging import getLogger

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from kotd_analytics.db import get_engine
from kotd_analytics.db import Comments

logger = getLogger(__name__)


def start(a_db_path: str) -> None:
    """
    Entrypoint for starting ingest of the database and analysis. May be called programmatically or from the CLI
    :param a_db_path: An absolute path to a sqlite database of reddit comments
    :return: None
    """
    l_engine: Optional[Engine] = get_engine(a_db_path)
    if not l_engine:
        logger.error("[start] Failed to create sqlite engine.")
        exit(-1)

    l_session = sessionmaker(bind=l_engine)

    with l_session.begin() as session:
        results = session.query(Comments).filter_by(author_flair_css_class="Elf").all()
    for line in results:
        print(line)


