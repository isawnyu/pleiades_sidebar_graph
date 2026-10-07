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
import networkx as nx
from pathlib import Path
from rdflib import Graph
from rdflib.extras.external_graph_libs import rdflib_to_networkx_graph
import sys
from urllib.parse import urlsplit

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
    print(f"Stats from rdflib")
    print("-" * 80)
    subjects = [s for s in g.subjects()]
    u_subjects = set(subjects)
    u_subj_netlocs = {urlsplit(str(s)).netloc for s in u_subjects}
    predicates = [p for p in g.predicates()]
    u_predicates = set(predicates)
    objects = [o for o in g.objects()]
    u_objects = set(objects)
    u_obj_netlocs = {urlsplit(str(o)).netloc for o in u_objects}
    for k, v in {
        "Statements": len(g),
        "Subjects": len(subjects),
        "Unique Subjects": len(u_subjects),
        "Unique Subject Netlocs": sorted(list(u_subj_netlocs)),
        "Predicates": len(predicates),
        "Unique Predicates": len(u_predicates),
        "Unique Predicate Values": sorted(
            [p.n3(g.namespace_manager) for p in u_predicates]
        ),
        "Objects": len(objects),
        "Unique Objects": len(u_objects),
        "Unique Object Netlocs (not in subject netlocs)": sorted(
            list(u_obj_netlocs.difference(u_subj_netlocs))
        ),
    }.items():
        if isinstance(v, int):
            print(f"  {k}: {v:,}")
        elif isinstance(v, list):
            print(f"  {k}:\n    - {'\n    - '.join(v)}")
        else:
            raise TypeError(f"")

    nxg = rdflib_to_networkx_graph(g)

    print("")
    print(f"Stats from networkx")
    print("-" * 80)
    degrees = [d for n, d in nxg.degree()]

    for k, v in {
        "Edges": nxg.number_of_edges(),
        "Nodes": nxg.number_of_nodes(),
        "Density": nx.is_connected(nxg),
        "Degree (maximum)": max(degrees),
        "Degree (minimum)": min(degrees),
        "Degree (average)": sum(degrees) / len(degrees),
    }.items():
        if isinstance(v, int):
            print(f"  {k}: {v:,}")
        elif isinstance(v, float):
            print(f"  {k}: {v:,.3}")
        elif isinstance(v, list):
            print(f"  {k}:\n    - {'\n    - '.join(v)}")
        else:
            raise TypeError(f"{k}: {type(v)}")

    sys.exit(EXIT_SUCCESS)  # if error, sys.exit(EXIT_ERROR)


if __name__ == "__main__":
    main(
        **configure_commandline(
            OPTIONAL_ARGUMENTS, POSITIONAL_ARGUMENTS, DEFAULT_LOG_LEVEL
        )
    )
