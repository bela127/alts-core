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


if TYPE_CHECKING:
    from typing_extensions import Self #type: ignore
    from typing import Optional
    from nptyping import NDArray, Number, Shape
    from alts.core.data.constrains import QueryConstrain, ResultConstrain, QueryConstrainedGetter


@dataclass
class QuerySampler(ExperimentModule):
    """
    QuerySampler(num_queries)
    | **Description**
    |   A QuerySampler samples a number of queries given its internal logic.
    |   It is mostly used to get the first datapoints for the experiment.

    :param num_queries: The amount of queries to sample by default (default= 1)
    :type num_queries: int
    """
    num_queries: int = init(default=1)
    _query_constrain: QueryConstrain = post_init()
    _result_constrain: ResultConstrain = post_init()

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
    
    @abstractmethod
    def query_constrain(self) -> QueryConstrain:
        """
        query_constrain(self) -> QueryConstrain
        | **Description**
        |   See :func:`DataSource.query_constrain()`
        |   This method is abstract.

        :return: Constrains around queries
        :rtype: QueryConstrain
        :throws: NotImplemntedError
        """
        return self._query_constrain
    
    @abstractmethod
    def result_constrain(self) -> ResultConstrain:
        """
        resuöt_constrain(self) -> ResultConstrain
        | **Description**
        |   See :func:`DataSource.result_constrain()`
        |   This method is abstract.

        :return: Constrains around results
        :rtype: QueryResult
        :throws: NotImplemntedError
        """
        return self._result_constrain
    
    def __call__(self, query_constrain: Required[QueryConstrainedGetter], **kwargs) -> Self:
        """
        __call__(self, query_constrain, **kwargs) -> Self
        | **Description**
        |   Returns a QuerySampler with the given query constraint.

        :param query_constrain: Constrains of the queries the queue holds.
        :type query_constrains: :doc:`QueryConstrain </core/data/constrains>`
        :return: Configured QueryOptimizer
        :rtype: QueryOptimizer
        """
        obj =  super().__call__(**kwargs)
        obj._query_constrain = is_set(query_constrain, "QuerySampler.query_constrain") # type: ignore
        return obj
