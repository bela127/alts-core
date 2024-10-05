#Version 1.1 conform as of 05.10.2024
"""
:doc:`Built-In Implementations </core/query/query_decider>`
"""
#TODO Handle empty Query Candidates
from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field
from abc import abstractmethod

from alts.core.experiment_module import ExperimentModule
from alts.core.data.constrains import QueryConstrained, QueryConstrain

if TYPE_CHECKING:
    from typing import Tuple, Optional
    from nptyping import NDArray, Number, Shape

@dataclass
class QueryDecider(ExperimentModule, QueryConstrained):
    """
    QueryDecider()
    | **Description**
    |   This module decides which best-scoring queries are worth the resources needed to obtain their results.
    |   Outside the first learning iteration of the model you can expect the QueryDecider to receive a non-empty list of query candidates.
    """

    @abstractmethod
    def decide(self, query_candidates: NDArray[Shape["query_nr, ... query_dims"], Number], scores: NDArray[Shape["query_nr, [query_score]"], Number]) -> Tuple[bool, NDArray[Shape["query_nr, ... query_dims"], Number]]: # type: ignore
        """
        decide(self, queries, scores) -> (bool, queries)
        | **Description**
        |   Returns its favorite query/queries out of a list of candidates with associated scores from 0 to 1.
        |   Is not implemented here.

        :param query_candidates: A list of queries to choose from
        :type query_candidates: Iterable over `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_ 
        :param scores: A list of scores associated to the queries in ``query_candidates``
        :type scores: Iterable over `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_ 
        :return: Whether it wants to decide, Favorite query/queries
        :rtype: ``boolean``, Iterable over `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_ 
        :raises: NotImplementedError
        """
        raise NotImplementedError()