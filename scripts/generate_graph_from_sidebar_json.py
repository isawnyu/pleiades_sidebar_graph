#
# This file is part of pleiades_sidebar_graph
# by Tom Elliott for the Institute for the Study of the Ancient World (ISAW) at New York University.
# (c) Copyright 2026 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Generate RDF graph from sidebar LPF JSON"""

from airtight.cli import configure_commandline
import logging
from pathlib import Path
import sys
from platformdirs import user_documents_dir
from pleiades_sidebar_graph.sidebar import SidebarDataset

logger = logging.getLogger(__name__)

DEFAULT_SIDEBAR_JSON_PATH = (
    f"{user_documents_dir()}/files/P/pleiades.datasets/data/sidebar/"
)
DEFAULT_OUTPUT_PATH = str(
    (Path(__file__).parent.parent / "data" / "sidebar_graph.ttl").resolve()
)


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
    [
        "-j",
        "--json",
        DEFAULT_SIDEBAR_JSON_PATH,
        "path to sidebar LPF JSON data (default: " + DEFAULT_SIDEBAR_JSON_PATH + ")",
        False,
    ],
    [
        "-o",
        "--output",
        DEFAULT_OUTPUT_PATH,
        "path to output file (default: " + DEFAULT_OUTPUT_PATH + ")",
        False,
    ],
]
POSITIONAL_ARGUMENTS = [
    # each row is a list with 3 elements: name, type, help
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
    logging.getLogger("normalize_space").setLevel(logging.WARNING)
    json_path = Path(kwargs.get("json")).expanduser().resolve()  # type: ignore
    if not json_path.exists():
        logger.error(f"JSON path does not exist: {json_path}")
        sys.exit(EXIT_ERROR)
    elif not json_path.is_dir():
        logger.error(f"JSON path is not a directory: {json_path}")
        sys.exit(EXIT_ERROR)

    logger.debug(f"Loading sidebar dataset from JSON path: {json_path}")
    sidebar_dataset = SidebarDataset(json_path)
    logger.debug("done")

    output_path = Path(kwargs.get("output")).expanduser().resolve()  # type: ignore
    if not output_path.parent.exists():
        logger.error(f"Output path's parent directory does not exist: {output_path}")
        sys.exit(EXIT_ERROR)
    if output_path.exists() and not output_path.is_file():
        logger.error(f"Output path exists but is not a file: {output_path}")
        sys.exit(EXIT_ERROR)
    if output_path.exists():
        backup_path = output_path.with_suffix(output_path.suffix + ".bak")
        logger.warning(
            f"Output file already exists: {output_path}. Backing up to {backup_path}."
        )
        output_path.rename(backup_path)
    logger.debug(f"Serializing sidebar graph to output path: {output_path}")
    sidebar_dataset.graph.serialize(destination=str(output_path), format="turtle")
    logger.debug("done")

    sys.exit(EXIT_SUCCESS)  # if error, sys.exit(EXIT_ERROR)


if __name__ == "__main__":
    main(
        **configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL
        )
    )
