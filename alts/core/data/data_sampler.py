#Version 1.1.1 conform as of 29.11.2024
"""
*alts.core.data.data_sampler*
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field


from alts.core.subscriber import ResultDataSubscriber, StreamDataSubscriber, ProcessDataSubscriber
from alts.core.query.queryable import Queryable
from alts.core.experiment_module import ExperimentModule


if TYPE_CHECKING:
    from typing import Tuple
    from typing_extensions import Self 
    from nptyping import NDArray, Number, Shape

@dataclass
class DataSampler(Queryable, ExperimentModule):
    """
    DataSampler()
    | **Description**
    |   Samples data from a :doc:`QueriedDataPools </core/data/queried_data_pool>`, meaning for each query the `DataSampler` returns a number of query-result pairs in the same area.
    """
    def query(self, queries: NDArray[Shape["query_nr, ... query_dim"], Number], size = None) -> Tuple[NDArray[Shape["query_nr, sample_size, ... query_dim"], Number], NDArray[Shape["query_nr, sample_size,... result_dim"], Number]]: # type: ignore
        """
        query(self, queries, size) -> data_points
        | **Description**
        |   Returns a tuple of ``size`` queries and ``size`` results in the area [#]_ of the requested queries.

        :param queries: A list of queries
        :type queries: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :param size: The preferred sample size
        :type size: Number
        :return: A tuple of queries and their associated results
        :rtype: Tuple[`NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_,`NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_]
        
        .. [#] The actually processed query may differ from the requested one.
            This may happen if the ``DataSource`` does not contain the exact query that is being requested, as the real-life case often is.
            In this scenario, a "similar" query will be processed or the query is dropped altogether.
        """
        raise NotImplementedError()

@dataclass
class ResultDataSampler(ResultDataSubscriber, DataSampler):
    """
    ResultDataSampler()
    | **Description**
    |   Samples data from a :doc:`ResultDataPools </core/data/data_pools>`.
    """
    pass

@dataclass
class StreamDataSampler(StreamDataSubscriber, DataSampler):
    """
    StreamDataSampler()
    | **Description**
    |   Samples data from a :doc:`StreamDataPools </core/data/data_pools>`.
    """
    pass

@dataclass
class ProcessDataSampler(ProcessDataSubscriber, DataSampler):
    """
    ProcessDataSampler()
    | **Description**
    |   Samples data from a :doc:`ProcessDataPools </core/data/data_pools>`.
    """
    pass
