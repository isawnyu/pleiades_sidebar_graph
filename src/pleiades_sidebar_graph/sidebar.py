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
import logging
from pathlib import Path
from pleiades_sidebar_graph.text import clean_text
from pprint import pformat
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, SKOS, SDO
from urllib.parse import urlsplit
from validators import url as is_valid_url

ns = {
    "geojson": Namespace("https://purl.org/geojson/vocab#"),
    "RDF": RDF,
    "RDFS": RDFS,
    "SDO": SDO,
    "SKOS": SKOS,
}


class SidebarDataset:
    """
    A dataset of sidebar LPF JSON, parsed into a graph.
    """

    def __init__(self, json_data_path: Path):
        """
        Initialize the SidebarDataset with the given JSON data.

        :param json_data_path: The path to a directory tree containing JSON files.
        """
        self.logger = logging.getLogger("SidebarDataset")
        self.json_data = self._load_json(json_data_path)
        self.graph = self._parse_json_to_graph(self.json_data)
        for prefix in ns.keys():
            if prefix.lower() == prefix:
                self.graph.bind(prefix, ns[prefix])
        self.logger.debug(self.graph.serialize())

    def _load_json(self, json_data_path: Path) -> dict:
        """
        Load JSON data from a file.

        :param json_data_path: The path to a directory tree containing JSON files.
        :return: The loaded JSON data.
        """
        all_the_json = dict()
        count = 0
        for root, dirs, files in json_data_path.walk(on_error=print):
            json_files = [f for f in files if f.endswith(".json")]
            for file in json_files:
                pid = file.split(".")[0]
                try:
                    str(int(pid))
                except ValueError:
                    continue
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
                    count += 1
                else:
                    raise RuntimeError(
                        f"Duplicate JSON file found for PID {pid} in {root / file}."
                    )
                if count % 5000 == 0 and count > 0:
                    self.logger.info(f"Loaded {count} JSON files so far...")
        self.logger.info(f"Loaded a total of {count} JSON files.")
        return all_the_json

    def _parse_json_to_graph(self, json_data) -> Graph:
        """
        Parse the JSON data into a graph structure.

        :param json_data: The JSON data to parse.
        :return: A graph representation of the JSON data.
        """
        graph = Graph()
        # Implementation for parsing JSON into a graph goes here
        count = 0
        for pid, data in json_data.items():
            for external_feature in data.get("inbound", []):
                count += 1
                external_id = external_feature["@id"]
                if not is_valid_url(external_id):
                    raise ValueError(
                        f"Invalid URL found: {external_id} in inbound items for PID {pid}"
                    )
                external_id = URIRef(external_id)
                properties = external_feature.get("properties", {})
                pleiades_reciprocal = properties["reciprocal"]
                if not isinstance(pleiades_reciprocal, bool):
                    raise TypeError(
                        f"Invalid reciprocal value: {pleiades_reciprocal} for PID {pid}"
                    )

                # if external_id not in graph.subjects():
                # type
                if external_feature["type"] == "Feature":
                    graph.add((external_id, ns["RDF"].type, ns["geojson"].Feature))
                else:
                    raise ValueError(
                        f"Unexpected type found: {external_feature['type']} for PID {pid}"
                    )

                # title
                title = properties["title"]
                if title is None:
                    raise ValueError(f"Missing title for PID {pid}")
                title = clean_text(title)
                if not title:
                    self.logger.warning(
                        f"Empty title for PID {pid}\n{pformat(external_feature)}"
                    )
                graph.add(
                    (
                        external_id,
                        ns["RDFS"].label,
                        Literal(title, lang="und"),
                    )
                )

                # summary
                summary = properties["summary"]
                if summary is not None:
                    summary = clean_text(summary)
                if summary:
                    graph.add(
                        (
                            external_id,
                            ns["SDO"].description,
                            Literal(summary, lang="und"),
                        )
                    )
                # process relationships for external features
                for link in external_feature["links"]:
                    if link["type"] == "closeMatch":
                        predicate = ns["SKOS"].closeMatch
                    elif link["type"] == "relatedMatch":
                        predicate = ns["SKOS"].relatedMatch
                    else:
                        raise NotImplementedError(
                            f"Unexpected link type: {link['type']} for PID {pid}"
                        )
                    object_id = link["identifier"]
                    if not is_valid_url(object_id):
                        if " " in object_id and "en.wikipedia.org" in object_id:
                            object_id = object_id.replace(" ", "_")
                            if not is_valid_url(object_id):
                                raise ValueError(
                                    f"Invalid URL found: {object_id} in links for PID {pid}. "
                                    "URL contains spaces."
                                )
                        else:
                            raise ValueError(
                                f"Invalid URL found: {object_id} in links for PID {pid}"
                            )
                    reciprocate = False
                    if (
                        urlsplit(object_id).netloc == "pleiades.stoa.org"
                        and pleiades_reciprocal
                    ):
                        reciprocate = True
                    object_id = URIRef(object_id)
                    graph.add((external_id, predicate, object_id))
                    if reciprocate:
                        graph.add((object_id, ns["SKOS"].relatedMatch, external_id))
                if count % 5000 == 0 and count > 0:
                    self.logger.info(f"Processed {count} inbound items so far...")
        self.logger.info(f"Processed a total of {count} inbound items.")
        self.logger.info(f"Graph has {len(graph)} triples.")
        return graph
