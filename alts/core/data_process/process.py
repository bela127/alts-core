#Version 1.1 conform as of 05.10.2024
"""
:doc:`Built-In Implementations </modules/data_process/process>`
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field
import numpy as np

if TYPE_CHECKING:
    from typing_extensions import Self
    from typing import Tuple
    from nptyping import NDArray, Number, Shape
    from alts.core.configuration import Required
    from alts.core.oracle.oracles import Oracles
    from alts.core.data.data_pools import DataPools



from alts.core.configuration import is_set, init, post_init, pre_init, NOTSET, Configurable

from alts.core.data_process.time_source import TimeSource
from alts.core.query.queryable import Queryable


class Process(Configurable, Queryable):
    """
    Process(time_source, data_pools, oracles)
    | **Description**
    |   The Process is the module responsible for processing the :doc:`Estimator's </core/estimator>` queries and providing their results as well as saving all the queried data. 

    :param time_source: Source of time
    :type time_source: :doc:`TimeSource </core/data_process/process>`
    :param data_pools: A data structure which saves all processed queries and results
    :type data_pools: :doc:`DataPools </core/data/data_pools>`
    :param oracles: The place that contains the results to all queries.
    :type oracles: :doc:`Oracles </core/oracle/Oracles>`
    """
    time_source: TimeSource = post_init()
    data_pools: DataPools = post_init()
    oracles: Oracles = post_init()

    last_queries: NDArray[Shape["data_nr, ... query_shape"], Number] = post_init() # type: ignore
    last_results: NDArray[Shape["data_nr, ... result_shape"], Number] = post_init() # type: ignore


    def initialize(self):
        """
        initialize(self) -> None
        | **Description**
        |   Does everything that needs to be done for the Process to be ready.
        """
        pass
    
    def step(self, iteration) -> Tuple[NDArray[Shape["query_nr, ... query_dim"], Number], NDArray[Shape["query_nr, ... result_dim"], Number], NDArray[Shape["query_nr, ... query_dim"], Number], NDArray[Shape["query_nr, ... result_dim"], Number]]: # type: ignore
        """
        step(self, iteration) -> (pre_step_data_points, post_step_data_points)
        | **Description**
        |   Advances the time (of its time source) by ``iteration`` step and returns the new data.

        :param iteration: Amount of steps to do
        :type iteration: int
        :return: Processed Queries before step, Results before step, Processed Queries after step, Results after step
        :rtype: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_, `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_, `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_, `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_ 
        """
        return None, None, None, None # type: ignore
    
    def __call__(self, time_source: Required[TimeSource] = None, oracles: Required[Oracles] = None, data_pools: Required[DataPools] = None, **kwargs) -> Self:
        """
        __call__(self, time_source, oracles, data_pools) -> Self
        | **Description**
        |   Returns an object of itself configured with all the parsed arguments.

        :param time_source: An custom source of time
        :type time_source: :doc:`TimeSource </core/data_process/process>`
        :param data_pools: A data structure which saves all processed queries and results
        :type data_pools: :doc:`DataPools </core/data/data_pools>`
        :param oracles: The place that contains the results to all queries.
        :type oracles: :doc:`Oracles </core/oracle/Oracles>`
        :return: The configured object
        :rtype: Process
        """
        obj = super().__call__(**kwargs)
        obj.time_source = is_set(time_source)
        obj.data_pools = is_set(data_pools)
        obj.oracles = is_set(oracles)

        return obj