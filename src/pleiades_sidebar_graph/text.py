#
# This file is part of pleiades_sidebar_graph
# by Tom Elliott for the Institute for the Study of the Ancient World (ISAW) at New York University.
# (c) Copyright 2026 by New York University
# Licensed under the AGPL-3.0; see LICENSE.txt file.
#

"""
Work with text in strings
"""

from textnorm import normalize_space, normalize_unicode


def clean_text(text: str) -> str:
    """
    Clean text by stripping whitespace and replacing multiple spaces with a single space.

    :param text: The input text to clean.
    :return: The cleaned text.
    """
    if not isinstance(text, str):
        raise TypeError(f"Input must be a string. Got {type(text).__name__} instead.")
    return normalize_space(normalize_unicode(text))
