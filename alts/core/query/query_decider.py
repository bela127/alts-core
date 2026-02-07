#Version 1.1.1 conform as of 29.11.2024
"""
| *alts.core.query.query_decider*
| :doc:`Built-In Implementations </modules/query/query_decider>`
"""
#TODO Handle empty Query Candidates
from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field
from abc import abstractmethod
from typing_extensions import Self

from alts.core.configuration import post_init, is_set, Required
from alts.core.experiment_module import ExperimentModule
from alts.core.data.constrains import QueryConstrained, QueryConstrain, ResultConstrain, QueryConstrainedGetter
from alts.core.experiment_modules import ExperimentModules

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
    _query_constrain: QueryConstrainedGetter = post_init()

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

    def query_constrain(self) -> QueryConstrain:
        return self._query_constrain()
    
    def result_constrain(self) -> ResultConstrain:
        return ResultConstrain(count=None,shape=self._query_constrain().shape,ranges=None)
    
    def __call__(self, query_constrain: Required[QueryConstrainedGetter], **kwargs) -> Self:
        """
        __call__(self, query_constrain, **kwargs) -> Self
        | **Description**
        |   Returns a QueryDecider with the given query constraint.

        :param query_constrain: Constraints of the QueryDecider.
        :type query_constrains: :doc:`QueryConstrain </core/data/constrains>`
        :return: Configured QueryDecider
        :rtype: QueryDecider
        """
        obj =  super().__call__(**kwargs)
        obj._query_constrain = is_set(query_constrain, "QueryDecider.query_constrain")
        return obj
