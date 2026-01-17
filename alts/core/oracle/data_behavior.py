#Version 1.1.1 conform as of 29.11.2024
"""
| *alts.core.oracle.data_behavior*
| :doc:`Built-In Implementations </modules/behavior>`
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field

import numpy as np

from alts.core.configuration import init, post_init, Configurable, Required, is_set
from alts.core.data.constrains import QueryConstrain, QueryConstrained, ResultConstrain

if TYPE_CHECKING:
    from typing_extensions import Self
    from typing import Tuple
    from nptyping import  NDArray, Shape
    from alts.core.data.constrains import QueryConstrainedGetter, QueryConstrain

@dataclass
class DataBehavior(Configurable, QueryConstrained):
    """
    DataBehavior(change_interval, lower_value, upper_value, start_time, stop_time)
    | **Description**
    |   Dictates how the data is behaving/changing over time.
    |   Useful for simulating changes in environment during the observed time frame.

    :param change_interval: Amount of time steps between behaviour changes (default=5.0)
    :type change_interval: float
    :param lower_value: Lower extent of data value changes (default=-1.0)
    :type lower_value: float
    :param upper_value: Upper extent of data value changes (default=1.0)
    :type upper_value: float
    :param start_time: Start of affected time (default=0.0)
    :type start_time: float
    :param stop_time: Stop of affected time (default=600.0)
    :type stop_time: float
    """
    change_interval: float = init(default=5)
    lower_value: float = init(default=-1)
    upper_value: float = init(default=1)

    start_time: float = init(default=0)
    stop_time: float = init(default=600)

    _query_constrain: QueryConstrainedGetter = post_init()

    def behavior(self) -> 'Tuple[NDArray[Shape["change_times"], np.dtype[np.number]], NDArray[Shape["change_values"], np.dtype[np.number]]]': 
        """
        behaviour(self) -> change_times, change_values
        | **Description**
        |   Describes when the data changes and by what value it does

        :return: change_times, change_values
        :rtype: `NDArray[float] <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_, `NDArray[float] <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :raises: NotImplementedError
        """
        raise NotImplementedError()
    
    def query_constrain(self) -> QueryConstrain:
        return self._query_constrain()
    
    def result_constrain(self) -> ResultConstrain:
        return ResultConstrain(shape=self.query_constrain().shape)

    def __call__(self, query_constrain: Required[QueryConstrainedGetter], **kwargs) -> Self:
        """
        __call__(self, query_constrain, **kwargs) -> Self
        | **Description**
        |   Returns a DataBehavior with the given query constraint.

        :param query_constrain: Constrains of the DataBehvaior.
        :type query_constrains: :doc:`QueryConstrain </core/data/constrains>`
        :return: Configured DataBehavior
        :rtype: DataBehavior
        """
        obj =  super().__call__(**kwargs)
        obj._query_constrain = is_set(query_constrain, "DataBehavior.query_constrain")
        return obj
