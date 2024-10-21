#TODO D queries_from_norm_pos
"""
:doc:`Built-In Implementations </modules/data/constrains>`
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass
from abc import abstractmethod

import numpy as np

from typing import Callable
from alts.core.configuration import ROOT

if TYPE_CHECKING:
    from typing import Tuple, Optional, Union
    from nptyping import NDArray, Shape

@dataclass
class QueryConstrain():
    """
    QueryConstrain(count, shape, ranges)
    | **Description**
    |   A ``QueryConstrain`` describes what kind of queries the given ``Queryable`` object accepts.
    |   Queries can be constrained in 3 ways: count, shape, and value ranges.

    :param count: How many queries can be made
    :type count: ``int``
    :param shape: What shape the queries must have
    :type shape: `Array Shape <https://www.w3schools.com/python/numpy/numpy_array_shape.asp>`_
    :param ranges: A set of all permitted query values
    :type ranges: Union of `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
    :return: No return
    :rtype: None
    """
    count: Optional[int]
    shape: Tuple[int, ...]
    ranges: Union[NDArray[Shape["... query_dims,[xi_min, xi_max]"], np.dtype[np.number]], NDArray[Shape["... query_dims,[xi]"], np.dtype[np.number]]] 

    def matches_shape(self, shape) -> bool:
        """
        matches_shape(shape) -> bool
        | **Description**
        |   Checks whether the query matches the shape constraints of the ``Queryable`` object.

        :param shape: The shape of the query
        :type shape: `Array Shape <https://www.w3schools.com/python/numpy/numpy_array_shape.asp>`_
        :return: Confirmation or Rejection
        :rtype: ``Boolean``
        """
        if len(self.shape) == len(shape):
            for dim_own, dim_ext in zip(self.shape, shape):
                if dim_own != dim_ext:
                    return False
            return True
        return False
    
    def constrains_met(self, queries) -> bool:
        """
        constrains_met(queries) -> bool
        | **Description**
        |   Checks whether the query matches the shape constraints of the ``Queryable`` object.

        :param shape: An iterable of queries
        :type shape: Iterable over `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :return: Confirmation or Rejection
        :rtype: ``Boolean``
        """
        for query in queries:
            if not self.matches_shape(query.shape): return False
        return True

    def add_queries(self, queries: NDArray[Shape["query_count, ... query_shape"], np.dtype[np.number]]): 
        """
        add_queries(queries) -> None
        | **Description**
        |   Adds the list of queries to ``ranges`` and updates the ``query_count``

        :param shape: An iterable of queries
        :type shape: Iterable over `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :return: No return
        :rtype: None
        """
        if self.ranges is None:
            self.ranges = queries[..., None]
        else: 
            self.ranges = np.concatenate((self.ranges, queries[..., None]))
        self._last_queries = queries
        self.query_count = self.ranges.shape[0]

    def last_queries(self) -> NDArray[Shape["query_nr, ... query_shape"], np.dtype[np.number]]: 
        """
        last_queries() -> queries
        | **Description**
        |   Returns the last added queries.

        :return: Last added query
        :rtype: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        if self._last_queries is None:
            raise LookupError("there are infinit queries continues pool")
        return self._last_queries

    def queries_from_norm_pos(self, norm_pos: NDArray[Shape["query_nr, ... query_dims"], np.dtype[np.number]]) -> NDArray[Shape["query_nr, ... query_dims"], np.dtype[np.number]]: 

        if self.ranges is None:
            raise LookupError("can not look up a position in a discrete pool")
        if np.any(np.isinf(self.ranges)):
            self.ranges = np.nan_to_num(self.ranges, nan=0, posinf=float(np.finfo(np.float64).max), neginf=float(np.finfo(np.float64).min))
            raise RuntimeWarning("QueryConstrain ranges are infinity, they will be converted to max float64, but most probably you forgot to provide constrains!")
        elements = self.ranges[..., 0] + (self.ranges[..., 1] - self.ranges[..., 0]) * norm_pos
        return elements
    
    def queries_from_index(self, indexes) -> NDArray[Shape["query_nr, ... query_shape"], np.dtype[np.number]]: 
        """
        queries_from_index(indexes) -> queries
        | **Description**
        |   Returns the ``indexes``-th added queries.

        :param indexes: The indexes to look up
        :type indexes: An ``iterable`` of ``int``
        :return: The queries at the indexes
        :rtype: ``iterable`` of `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        if self.ranges is None:
            raise LookupError("can not look up a index in a continues pool")
        return self.ranges[indexes]
    
    def all_queries(self) -> NDArray[Shape["query_nr, ... query_shape"], np.dtype[np.number]]: 
        """
        all_queries() -> queries
        | **Description**
        |   Returns all added queries.

        :return: All added queries
        :rtype: ``iterable`` of `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        if self.ranges is None:
            raise LookupError("there are infinit queries continues pool")
        return self.ranges


@dataclass
class ResultConstrain():
    """
    ResultConstrain(shape, ranges)
    | **Description**
    |   A ``ResultConstrain`` describes what kind of results the given ``Queryable`` object gives.
    |   Results can be constrained in 2 ways: shape, and value ranges.

    :param shape: What shape the queries must have
    :type shape: `Array Shape <https://www.w3schools.com/python/numpy/numpy_array_shape.asp>`_
    :param ranges: A set of all permitted query values
    :type ranges: Union of `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
    """
    shape: Tuple[int,...]
    ranges: Optional[NDArray[Shape["... query_dims,[xi_min, xi_max]"], np.dtype[np.number]]] = None 

class QueryConstrained():
    """
    QueryConstrained()
    | **Description**
    |   If a class inherits from ``QueryConstrained``, it means that its objects have a :class:`QueryConstrain` for all queries.

    """
    @abstractmethod
    def query_constrain(self) -> QueryConstrain:
        """
        query_constrain(self) -> QueryConstrain
        | **Description**
        |   Returns the :class:`QueryConstrain` of the object. 
        |   Not implemented here.
        """
        raise NotImplementedError()

class ResultConstrained():
    """
    ResultConstrained()
    | **Description**
    |   If a class is ``ResultConstrained``, its objects have a :class:`ResultConstrain` for all immediate results.

    """
    @abstractmethod
    def result_constrain(self) -> ResultConstrain:
        """
        result_constrain(self) -> ResultConstrain
        | **Description**
        |   Returns the :class:`ResultConstrain` of the object. 
        |   Not implemented here.
        """
        raise NotImplementedError()

class DelayedConstrained():
    """
    DelayedConstrained()
    | **Description**
    |   If a class is ``ResultConstrained``, its objects have a :class:`ResultConstrain` for all delayed results.

    """
    @abstractmethod
    def delayed_constrain(self) -> ResultConstrain:
        """
        delayed_constrain(self) -> ResultConstrain
        | **Description**
        |   Returns the :class:`ResultConstrain` of the object. 
        |   Not implemented here.
        """
        raise NotImplementedError()

class Constrained(QueryConstrained, ResultConstrained):
    """
    Constrained()
    | **Description**
    |   If a class is ``ResultConstrained``, its objects have a :class:`QueryConstrain` for all queries and a :class:`ResultConstrain` for all immediate results.
    """
    pass

ResultConstrainGetter = Callable[[],ResultConstrain]

QueryConstrainedGetter = Callable[[],QueryConstrain]