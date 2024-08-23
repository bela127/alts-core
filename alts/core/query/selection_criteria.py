#Fully documented as of 20.07.2024
"""
:doc:`Built-In Implementations </module/query/selection_criteria>`
"""
from __future__ import annotations
from abc import abstractmethod, abstractproperty
from typing import TYPE_CHECKING

from alts.core.experiment_module import ExperimentModule
from alts.core.data.constrains import ResultConstrain
from alts.core.query.queryable import Queryable

if TYPE_CHECKING:
    from typing import Tuple
    from nptyping import NDArray, Shape, Number
    



class SelectionCriteria(ExperimentModule, Queryable):
    """
    | **Description**
    |   A ``SelectionCriteria`` is an algorithm which gives scores to query candidates.
    """

    @abstractmethod
    def query(self, queries: NDArray[Shape["query_nr, ... query_shape"], Number]) -> Tuple[NDArray[Shape["query_nr, ... query_shape"], Number], NDArray[Shape["query_nr, [score]"], Number]]: # type: ignore
        """
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
    
    def result_constrain(self) -> ResultConstrain:
        """
        | **Description**
        |   Returns the result constraints for scores.

        | **Current Constraints**
        |   *None*

        :return: Constraints around results
        :rtype: ResultConstrain
        """
        return ResultConstrain((self.query_constrain().shape[0], 1))
