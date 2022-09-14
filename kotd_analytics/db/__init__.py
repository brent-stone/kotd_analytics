from typing import Optional, Tuple
from logging import getLogger
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.engine import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import declarative_base

logger = getLogger(__name__)

valid_db_extensions: Tuple[str, ...] = (".sqlite", ".db")
sqlite_prefix: str = "sqlite:///"

Base = declarative_base()


class Comments(Base):
    """
    Reddit comment with the following fields and examples:

    :param id: An auto-increment integer ID
    :type id: int
    :param comment_id: A reddit provided unique comment id: "iml85st"
    :type comment_id: Text
    :param body: The actual comment: "!attack"
    :type body: Text
    :param author: Reddit user name: "_Not_An_Elf_"
    :type author: Text
    :param link_id: A reddit provided unique link id: "t3_x2nbp5"
    :type link_id: Text
    :param author_flair_text: A KOTD string '{Race} {Prestige Stars}': "Elf ★★"
    :type author_flair_text: Text
    :param author_flair_css_class: Similar to flair text with just race: "Elf"
    :type author_flair_css_class: Text
    :param permalink: An abbreviated url: "/r/kickopenthedoor/comments/x2nbp5/bee_k...3000/iml85st/"
    :type permalink: Text
    :param parent_id: Another reddit unique ID string: "t3_x2nbp5"
    :type parent_id: Text
    :param created_utc: An integer formatted epoch timestamp: 1661988064
    :type created_utc: Integer
    """
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    comment_id = Column(Text)
    body = Column(Text)
    author = Column(Text)
    link_id = Column(Text)
    author_flair_text = Column(Text)
    author_flair_css_class = Column(Text)
    permalink = Column(Text)
    parent_id = Column(Text)
    created_utc = Column(Integer)


def get_engine(a_sqlite_path: str) -> Optional[Engine]:
    """
    Create a SQLAlchemy database engine from the provided sqlite database file path
    :param a_sqlite_path:
    :return:
    """
    # Strip any lefthand '/' from the path prior to concatenation
    if a_sqlite_path[0] == "/":
        a_sqlite_path = a_sqlite_path[1:]
    l_dsn_str: str = sqlite_prefix + a_sqlite_path
    try:
        l_engine: Engine = create_engine(l_dsn_str, echo=True)
        logger.debug(f"[get_engine] Successfully created SQLAlchemy engine from DSN: {l_dsn_str}")
    except (ArgumentError, ValueError) as e:
        logger.error(f"[get_engine] Failed to create the engine from DSN: {l_dsn_str}")
        raise e
    return l_engine
