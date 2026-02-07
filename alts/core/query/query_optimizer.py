#Version 1.1.1 conform as of 13.12.2024
"""
| *alts.core.query.query_optimizer*
| :doc:`Built-In Implementations </modules/query/query_optimizer>`
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass
from alts.core.configuration import Required, init, post_init, is_set

from alts.core.experiment_module import ExperimentModule
from alts.core.data.constrains import QueryConstrained, QueryConstrainedGetter, ResultConstrain
from numpy import shape

if TYPE_CHECKING:
    from typing_extensions import Self #type: ignore
    from typing import Tuple

    from alts.core.query.selection_criteria import SelectionCriteria
    from alts.core.experiment_modules import ExperimentModules
    from alts.core.query.query_sampler import QuerySampler
    from alts.core.data.constrains import QueryConstrain

    from nptyping import NDArray, Number, Shape
    
@dataclass
class QueryOptimizer(ExperimentModule, QueryConstrained):
    """
    QueryOptimizer(selection_criteria)
    | **Description**
    |   The QueryOptimizer tries to find the most worthy queries to evaluate next.
    |   The worthiness of a query symbolizes the information content of its result.
    |   Worthiness is measured by a score given by ``selection_criteria``. So QueryOptimizer
        tries to maximize said score. 

    :param selection_criteria: Tells the QueryOptimizer the scores of queries
    :type selection_criteria: SelectionCriteria
    """
    selection_criteria: SelectionCriteria = init()
    _query_constrain: QueryConstrainedGetter = post_init()

    def post_init(self):
        """
        post_init(self) -> None
        | **Description**
        |   Initializes ``selection_criteria`` with its experiment modules.
        """
        super().post_init()
        self.selection_criteria = self.selection_criteria(query_constrain=self.query_constrain ,exp_modules = self.exp_modules)

    def select(self, num_queries = None) -> Tuple[NDArray[Shape["query_nr, ... query_dims"], Number], NDArray[Shape["query_nr, [query_score]"], Number]]: # type: ignore
        """
        select(self, num_queries) -> queries, scores
        | **Description**
        |   Tries to find the queries with the highest scores and returns them.

        :param num_queries: Number of requested queries
        :type num_queries: int
        :return: queries, scores
        :rtype: Iterable over `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_, Iterable over `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :raises: NotImplementedError
        """
        raise NotImplementedError
    
    def query_constrain(self) -> QueryConstrain:
        if not is_set(self._query_constrain):
            raise ValueError
        return self._query_constrain()
    
    def result_constrain(self) -> ResultConstrain:
        return ResultConstrain(shape=self.query_constrain().shape)
    
    def __call__(self, query_constrain: Required[QueryConstrainedGetter], **kwargs) -> Self:
        """
        __call__(self, query_constrain, **kwargs) -> Self
        | **Description**
        |   Returns a QueryOptimizer with the given query constraint.

        :param query_constrain: Constrains of the queries the queue holds.
        :type query_constrains: :doc:`QueryConstrain </core/data/constrains>`
        :return: Configured QueryOptimizer
        :rtype: QueryOptimizer
        """
        obj =  super().__call__(**kwargs)
        obj._query_constrain = is_set(query_constrain, "QueryOptimizer.query_constrain")
        return obj
