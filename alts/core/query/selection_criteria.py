#Version 1.1.1 conform as of 29.11.2024
"""
| *alts.core.query.selection_criteria*
| :doc:`Built-In Implementations </modules/query/selection_criteria>`
"""
from __future__ import annotations
from abc import abstractmethod
import numpy as np
from typing import TYPE_CHECKING

from alts.core.configuration import post_init, Required, is_set
from alts.core.experiment_module import ExperimentModule
from alts.core.data.constrains import QueryConstrain, ResultConstrain, QueryConstrainedGetter
from alts.core.query.queryable import Queryable

if TYPE_CHECKING:
    from typing import Tuple
    from typing_extensions import Self
    from nptyping import NDArray, Shape, Number
    



class SelectionCriteria(ExperimentModule, Queryable):
    """
    SelectionCriteria()
    | **Description**
    |   A ``SelectionCriteria`` is an algorithm which gives scores to query candidates. Higher scores correspond to more informative/valuable queries.    
    """
    _query_constrain: QueryConstrainedGetter = post_init()

    def post_init(self):
        self._query_constrain = self.exp_modules.query_selector.query_constrain

    @abstractmethod
    def query(self, queries: NDArray[Shape["query_nr, ... query_shape"], Number]) -> Tuple[NDArray[Shape["query_nr, ... query_shape"], Number], NDArray[Shape["query_nr, [score]"], Number]]: # type: ignore
        """
        query(self, queries) -> data_points
        | **Description**
        |   Gives each query from the list a score based on the implementation.
        |   Is not implemented here.

        :param queries: A list of queries to evaluate
        :type queries: Iterable over `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_ 
        :return: queries, associated scores
        :rtype: Iterable over `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_, Iterable over `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_ 
        :raises: NotImplementedError
        """
        raise NotImplementedError
    
    def query_constrain(self) -> QueryConstrain:
        """
        query_constrain(self) -> QueryConstrain
        | **Description**
        |   Returns the query constrains for scores.

        :return: Constrains around queries
        :rtype: QueryConstrain
        """
        return QueryConstrain(count=None, shape=(2,), ranges=None)
        #return self.query_constrain()

    def result_constrain(self) -> ResultConstrain:
        """
        result_constrain(self) -> ResultConstrain
        | **Description**
        |   Returns the result constrains for scores.

        :return: Constrains around results
        :rtype: ResultConstrain
        """
        return ResultConstrain(count=self._query_constrain().count, shape=(self.query_constrain().shape[0],1), ranges=np.asarray((0,1)))

    def __call__(self, query_constrain: Required[QueryConstrainedGetter], **kwargs) -> Self:
        """
        __call__(self, query_constrain, **kwargs) -> Self
        | **Description**
        |   Returns a SelectionCriteria with the given query constraint.

        :param query_constrain: Constraints of the SelectionCriteria.
        :type query_constrains: :doc:`QueryConstrain </core/data/constrains>`
        :return: Configured SelectionCriteria
        :rtype: SelectionCriteria
        """
        obj =  super().__call__(**kwargs)
        obj._query_constrain = is_set(query_constrain, "SelectionCriteria.query_constrain")
        return obj