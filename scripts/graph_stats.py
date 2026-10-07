#
# This file is part of pleiades_sidebar_graph
# by Tom Elliott for the Institute for the Study of the Ancient World (ISAW) at New York University.
# (c) Copyright 2026 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Get statistics on a graph
"""

from airtight.cli import configure_commandline
import logging
from pathlib import Path
from rdflib import Graph
import sys

logger = logging.getLogger(__name__)

DEFAULT_LOG_LEVEL = logging.WARNING
OPTIONAL_ARGUMENTS = [
    [
        "-l",
        "--loglevel",
        "NOTSET",
        "desired logging level ("
        + "case-insensitive string: DEBUG, INFO, WARNING, or ERROR",
        False,
    ],
    ["-v", "--verbose", False, "verbose output (logging level == INFO)", False],
    [
        "-w",
        "--veryverbose",
        False,
        "very verbose output (logging level == DEBUG)",
        False,
    ],
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
    ["rdffile", str, "path to RDF file"]
]

EXIT_SUCCESS = 0
EXIT_ERROR = 1


def main(**kwargs):
    """
    main function
    """
    # logger = logging.getLogger(sys._getframe().f_code.co_name)
    # code here
    # when all is done and goes well
    rdfpath = Path(kwargs["rdffile"]).expanduser().resolve()
    g = Graph()
    g.parse(rdfpath)
    sys.exit(EXIT_SUCCESS)  # if error, sys.exit(EXIT_ERROR)


if __name__ == "__main__":
    main(
        **configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL
        )
    )
