"""
Primary functions for orchestrating analysis of Kick Open the Door data
"""
from typing import Optional
from logging import getLogger

from sqlalchemy.engine import Engine

from kotd_analytics.db import get_engine

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
    print("good to go!")
