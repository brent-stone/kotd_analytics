"""
CLI entrypoint for the package
"""
from argparse import ArgumentParser
from argparse import ArgumentError
from argparse import ArgumentTypeError
from argparse import Namespace
from logging import getLogger

from kotd_analytics import start
from kotd_analytics.db import valid_db_extensions
from os.path import exists
from os.path import abspath

logger = getLogger(__name__)  # return an open file handle


def check_path(a_path: str) -> str:
    """
    Verify that the user provided path appears to be both a valid path and appears to be sqlite database based on the
    file extension.
    :param a_path: A path to a sqlite database
    :return: A relative path to the sqlite database
    """
    # Verify the path exists
    if not exists(a_path):
        raise ArgumentError(argument=None, message=f"File doesn't exist: {a_path}")

    # Verify the path superficially appears to be a sqlite database
    l_path: str = ""
    for valid_extension in valid_db_extensions:
        if valid_extension in a_path:
            l_path = a_path
            break
    if not bool(l_path):
        raise ArgumentError(argument=None, message=f"File doesn't appear to be a sqlite database. Valid types are: {valid_db_extensions}")

    # Return the absolute path to the database file
    return abspath(l_path)


if __name__ == "__main__":
    """
    CLI Argument Parser setup and execution handoff to the rest of the package.
    """
    parser = ArgumentParser(description="Examine sqlite database with the kotd_analytics package.")
    parser.add_argument(
        "-f",
        "--file",
        dest="filename",
        required=True,
        help="Path to the sqlite database of KOTD comments",
        metavar="FILE",
        type=check_path,
    )
    try:
        args: Namespace = parser.parse_args()
        start(a_db_path=args.filename)
    except (ArgumentError, ArgumentTypeError) as e:
        l_message: str = f"Failed to parse CLI arguments: {e}"
        logger.error(l_message)
        print(l_message)
        exit(-1)
