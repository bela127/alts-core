"""
:doc:`Built-In Implementations </modules/oracle/data_source>`
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field

from alts.core.query.queryable import Queryable
from alts.core.data.constraints import QueryConstrain, ResultConstrain
from alts.core.configuration import init, Configurable

import numpy as np

if TYPE_CHECKING:
    from typing import Tuple, List
    from nptyping import NDArray, Shape, Number

@dataclass
class DataSource(Configurable, Queryable):
    """
    | **Description**
    |   A ``DataSource`` is a source of learning data for the model in training.
    |   It returns *results* (y-values) to given *queries* (x-values) upon request.
    |   The generation of its data depends on the individual implementation.

    :param query_shape: The expected shape of the queries
    :type query_shape: tuple of ints
    :param result_shape: The expected shape of the results
    :type result_shape: tuple of ints
    """
    query_shape: Tuple[int,...] = init()
    result_shape: Tuple[int,...] = init()

    def query(self, queries: NDArray[ Shape["query_nr, ... query_dim"], Number]) -> Tuple[NDArray[Shape["query_nr, ... query_dim"], Number], NDArray[Shape["query_nr, ... result_dim"], Number]]:
        """
        | **Description**
        |   ``query()`` is the access point to the data of the ``DataSource``.
        |   It returns the *result* to a given *query*.

        :param queries: Requested Query
        :type queries: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :return: Processed Query [#]_ , Result 
        :rtype: A tuple of two `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_

        | **Default Implementation**
        |   *None*

        :raises: ``NotImplementedError``

        .. [#] The actually processed query may differ from the requested one.
            | This may happen if the ``DataSource`` does not contain the exact query that is being requested, as the real-life case often is.
            | In this scenario, a "similar" query will be processed in its stead.
        """
        raise NotImplementedError
 
    def query_constrain(self) -> QueryConstrain:
        """
        | **Description**
        |   ``query_constrain()`` is a getter-function for the constraints around queries to the ``DataSource``. 
        |   Constraints can affect the ``count``, ``shape`` and the ``ranges`` of a query.
        |   For more information, see :doc:`Constraints </core/data/constraints>`

        | **Current Constraints**
        |   *Shape:* ``query_shape``
        |   *Value Range:* (-inf, inf) for all values

        :return: Constraints around queries
        :rtype: QueryConstrain
        """
        query_ranges = np.asarray(tuple((np.NINF, np.Inf) for i in range(self.query_shape[0])))
        return QueryConstrain(count=None, shape=self.query_shape, ranges=query_ranges)
    
    def result_constrain(self) -> ResultConstrain:
        """
        | **Description**
        |    ``result_constrain()`` is the equivalent of :func:`query_constrain()` for results from the ``DataSource``.

        | **Current Constraints**
        |    *Shape:* ``result_shape`` 

        :return: Constraints to results
        :rtype: ResultConstrain
        """
        return ResultConstrain(shape = self.result_shape)
    
    @property
    def exhausted(self):
        """
        | **Description**
        |    A ``DataSource`` is exhausted if all its available data has been querried.

        :return: Whether the ``DataSource`` has been exhausted
        :rtype: *boolean*

        | **Default Implementation**
        |    "``return False``"
        """
        return False

@dataclass
class TimeDataSource(DataSource):
    """
    | **Description**
    |   A ``TimeDataSource`` is a :class:`DataSource` in which the first entry of a query is a non-negative number (representing time).

    :param result_shape: The expected shape of results
    :type result_shape: tuple of ints
    """
    query_shape: Tuple[int,...] = (1,)
    
    def query(self, times: NDArray[Shape["time_step_nr, [time]"], Number]) -> Tuple[NDArray[Shape["time_step_nr, [time]"], Number], NDArray[Shape["time_step_nr, ... var_shape"], Number]]:
        """
        | **Description**
        |   See :func:`DataSource.query()` 

        :param queries: Requested Query
        :type queries: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :return: Processed Query, Result 
        :rtype: A tuple of two `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_

        | **Default Implementation**
        |   *None*

        :raises: ``NotImplementedError``
        """
        raise NotImplementedError()
    
    def query_constrain(self) -> QueryConstrain:
        """
        | **Description**
        |   See :func:`DataSource.query_constrain()`
        
        | **Current Constraints**
        |   *Shape:* ``query_shape``, (1,)
        |   *Range of first value:* [0, inf)
        |   *Range of other values:* (-inf, inf)

        :return: Constraints around queries
        :rtype: QueryConstrain
        """
        query_ranges = np.asarray(((0.0, np.Inf),))
        return QueryConstrain(count=None, shape=self.query_shape, ranges=query_ranges)

@dataclass
class TimeDataSourceWraper(TimeDataSource):
    """
    | **Description**
    |   A ``TimeDataSourceWrapper`` is a :class:`TimeDataSource` that queries from another :class:`DataSource`. 
    |   TODO [Explanation of what's the point of this]

    :param query_shape: The expected shape of queries
    :type query_shape: tuple of ints
    :param data_source: The :class:`DataSource` to query from.
    :type data_source: DataSource
    """
    query_shape: Tuple[int,...] = (1,)
    data_source: DataSource = init()

    def query(self, times: NDArray[Shape["time_step_nr, [time]"], Number]) -> Tuple[NDArray[Shape["time_step_nr, [time]"], Number], NDArray[Shape["time_step_nr, ... var_shape"], Number]]:
        """
        | **Description**
        |   ``query()`` queries from the initialized :class:`DataSource` ``data_source`` of the ``TimeDataSourceWrapper``. See :func:`DataSource.query()`.

        :param queries: Requested Query
        :type queries: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :return: Processed Query, Result 
        :rtype: A tuple of two `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        return self.data_source.query(times)
    
    def query_constrain(self) -> QueryConstrain:
        """
        | **Description**
        |   See :func:`DataSource.query_constrain()`
        
        | **Current Constraints**
        |   *Shape:* ``query_shape``, (1,)
        |   *Range of first value:* [0, t) where t is the upper bound of that value in ``data_source``
        |   *Range of other values:* (-inf, inf)

        :return: Constraints around queries
        :rtype: QueryConstrain
        """
        qc = self.data_source.query_constrain()
        query_ranges = np.asarray(((0.0, qc.ranges[0,1]),))
        return QueryConstrain(count=None, shape=self.query_shape, ranges=query_ranges)