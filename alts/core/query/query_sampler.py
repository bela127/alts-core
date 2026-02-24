#Version 1.1.1 conform as of 18.12.2024
"""
| *alts.core.query.query_sampler*
| :doc:`Built-In Implementations </modules/query/query_sampler>`
"""
from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING

from dataclasses import dataclass, field
from typing_extensions import Self

from alts.core.experiment_module import ExperimentModule
from alts.core.configuration import init, post_init, Required, is_set
from alts.core.experiment_modules import ExperimentModules
from alts.core.data.constrains import ResultConstrained, ResultConstrain

if TYPE_CHECKING:
    from typing_extensions import Self #type: ignore
    from typing import Optional
    from nptyping import NDArray, Number, Shape


@dataclass
class QuerySampler(ExperimentModule, ResultConstrained):
    """
    QuerySampler(num_queries)
    | **Description**
    |   A QuerySampler samples a number of queries given its internal logic.
    |   It is mostly used to get the first datapoints for the experiment.

    :param num_queries: The amount of queries to sample by default (default= 1)
    :type num_queries: int
    """
    num_queries: int = init(default=1)

    @abstractmethod
    def sample(self, num_queries: Optional[int] = None) -> NDArray[Shape["query_nr, ... query_dims"], Number]: # type: ignore
        """
        sample(self, num_queries) -> queries
        | **Description**
        |   Samples and returns a collection of ``num_queries``-many queries

        :param num_queries: The amount of queries to sample by default (default= )
        :type num_queries: int
        :return: Sampled queries
        :rtype: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :raises NotImplementedError: QuerySampler is abstract
        """
        raise NotImplementedError("Please use a non abstract ...QuerySampler.")
    
    def result_constrain(self) -> ResultConstrain:
        """
        result_constrain(self) -> ResultConstrain
        | **Description**
        |   See :func:`DataSource.result_constrain()`

        :return: Constrains around results
        :rtype: QueryResult
        """
        return ResultConstrain(count=None, shape=self.oracles.query_constrain().shape, ranges=self.oracles.query_constrain().ranges)