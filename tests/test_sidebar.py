#
# This file is part of pleiades_sidebar_graph
# by Tom Elliott for the Institute for the Study of the Ancient World (ISAW) at New York University.
# (c) Copyright 2026 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
test the sidebar module
"""

from pathlib import Path
from pleiades_sidebar_graph.sidebar import SidebarDataset


class TestSidebarDataset:
    def test_initialization(self):
        # Test that the SidebarDataset can be initialized with a JSON file path
        json_file_path = Path("tests/data/sidebar_json")
        dataset = SidebarDataset(json_file_path)
        assert len(dataset.json_data) == 56  # 56 unique pids in the test data
        assert dataset.graph is not None

    def test_graph_structure(self):
        # Test that the graph structure is as expected
        json_file_path = Path("tests/test_data/sidebar.json")
        dataset = SidebarDataset(json_file_path)
        graph = dataset.graph
        # Add assertions to check the structure of the graph, e.g., number of triples, specific nodes, etc.
