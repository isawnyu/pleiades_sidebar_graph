#
# This file is part of pleiades_sidebar_graph
# by Tom Elliott for the Institute for the Study of the Ancient World (ISAW) at New York University.
# (c) Copyright 2026 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Read and parse sidebar LPF JSON into a graph
"""

import json
from pathlib import Path
from pprint import pformat
from rdflib import Graph


class SidebarDataset:
    """
    A dataset of sidebar LPF JSON, parsed into a graph.
    """

    def __init__(self, json_data_path: Path):
        """
        Initialize the SidebarDataset with the given JSON data.

        :param json_data_path: The path to a directory tree containing JSON files.
        """
        self.json_data = self._load_json(json_data_path)
        self.graph = self._parse_json_to_graph(self.json_data)

    def _load_json(self, json_data_path: Path) -> dict:
        """
        Load JSON data from a file.

        :param json_data_path: The path to a directory tree containing JSON files.
        :return: The loaded JSON data.
        """
        all_the_json = dict()
        for root, dirs, files in json_data_path.walk(on_error=print):
            json_files = [f for f in files if f.endswith(".json")]
            for file in json_files:
                pid = file.split(".")[0]
                try:
                    all_the_json[pid]
                except KeyError:
                    all_the_json[pid] = {
                        "pid": pid,
                        "file": str(root / file),
                        "inbound": None,
                    }
                    with open(root / file, "r", encoding="utf-8") as f:
                        all_the_json[pid]["inbound"] = json.load(f)
                else:
                    raise RuntimeError(
                        f"Duplicate JSON file found for PID {pid} in {root / file}."
                    )
        return all_the_json

    def _parse_json_to_graph(self, json_data) -> Graph:
        """
        Parse the JSON data into a graph structure.

        :param json_data: The JSON data to parse.
        :return: A graph representation of the JSON data.
        """
        graph = Graph()
        # Implementation for parsing JSON into a graph goes here
        return graph
