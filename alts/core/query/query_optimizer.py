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
from alts.core.data.constrains import ResultConstrained, QueryConstraintGetter, ResultConstrain
from numpy import shape
import numpy as np

if TYPE_CHECKING:
    from typing_extensions import Self #type: ignore
    from typing import Tuple

    from alts.core.query.selection_criteria import SelectionCriteria
    from alts.core.experiment_modules import ExperimentModules
    from alts.core.query.query_sampler import QuerySampler
    from alts.core.data.constrains import QueryConstrain

    from nptyping import NDArray, Number, Shape
    
@dataclass
class QueryOptimizer(ExperimentModule, ResultConstrained):
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

    def post_init(self):
        """
        post_init(self) -> None
        | **Description**
        |   Initializes ``selection_criteria`` with its experiment modules.
        """
        super().post_init()
        self.selection_criteria = self.selection_criteria(exp_modules = self.exp_modules, query_constrain = self.result_constrain().to_query_constrain)

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
    
    def result_constrain(self) -> ResultConstrain:
        return ResultConstrain(count=None, shape=self.oracles.query_constrain().shape, ranges=self.oracles.query_constrain().ranges)