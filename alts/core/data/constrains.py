#Version 1.1.1 conform as of 18.04.2025
"""
| *alts.core.data.constrains*
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
class Constrain():
    """
    Constrain(count, shape, ranges)
    | **Description**
    |   A ``Constrain`` describes constraints around data.
    |   Data can be constrained in 3 ways: count, shape, and value ranges.

    :param count: How many data elements are expected
    :type count: ``int``
    :param shape: What shape the elements must have
    :type shape: `Array Shape <https://www.w3schools.com/python/numpy/numpy_array_shape.asp>`_
    :param ranges: A set of all permitted element values for discrete data sources OR of lower/upper bound per dimension for continuous data sources
    :type ranges: Union of `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
    """
    count: Optional[int] = None
    shape: Tuple[int, ...] = (1,)
    ranges: Optional[Union[NDArray[Shape["... element_dims,[xi_min, xi_max]"], np.dtype[np.number]], NDArray[Shape["... element_dims,[xi]"], np.dtype[np.number]]]] = None

    def matches_shape(self, elements) -> bool:
        """
        matches_shape(self, elements) -> bool
        | **Description**
        |   Checks whether the elements matches the shape constrains of the ``Constrained`` object, i.e. if the given shape is identical to the constraint shape.
        |   Returns True if shape is not set.

        :param elements: The list of elements
        :type elements: `Array Shape <https://www.w3schools.com/python/numpy/numpy_array_shape.asp>`_
        :return: Whether shape constraint is met
        :rtype: ``Boolean``
        """
        if self.shape is None:
            return True
        if self.shape == elements.shape[1:]:
            return True
        return False
    
    def matches_count(self, elements) -> bool:
        """
        matches_count(elements) -> bool
        | **Description**
        |   Checks whether the amount of elements matches the count constraint of the ``Queryable`` object, i.e. len(elements) <= count.
        |   Returns True if count is not set.

        :param elements: The list of elements
        :type elements: Iterable over `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :return: Whether count constraint is met
        :rtype: ``Boolean``
        """
        if self.count is None:
            return True
        if len(elements) <= self.count:
            return True
        return False
    
    def matches_ranges(self, elements):
        """
        matches_ranges(elements) -> bool
        | **Description**
        |   Checks whether the elements' values match the range constraint of the ``Queryable`` object, i.e. each value is in its allowed range.
        |   Returns True if count is not set.

        :param elements: The list of elements
        :type elements: Iterable over `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :return: Whether ranges constraint is met
        :rtype: ``Boolean``
        """
        if self.ranges is None:
            return True
        try:
            for element in elements:
                for idx, value in np.ndenumerate(element):
                    if value < self.ranges[idx][0] or value >= self.ranges[idx][1]:
                        return False
            return True
        except(IndexError):
            for element in elements:
                if not element in self.ranges:
                    return False
            return True
    
    def constrains_met(self, elements) -> bool:
        """
        constrains_met(elements) -> bool
        | **Description**
        |   Checks whether the element matches the shape constrains of the ``Queryable`` object.

        :param shape: An iterable of elements
        :type shape: Iterable over `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :return: Confirmation or Rejection
        :rtype: ``Boolean``
        """
        return self.matches_count(elements) and self.matches_shape(elements) and self.matches_ranges(elements)

    def add_elements(self, elements: NDArray[Shape["element_count, ... element_shape"], np.dtype[np.number]]): 
        """
        add_elements(elements) -> None
        | **Description**
        |   Adds the list of elements to ``ranges`` and updates the ``element_count``

        :param shape: An iterable of elements
        :type shape: Iterable over `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :return: No return
        :rtype: None
        """
        if self.ranges is None:
            self.ranges = elements[..., None]
        else: 
            self.ranges = np.concatenate((self.ranges, elements[..., None]))
        self._last_elements = elements
        self.element_count = self.ranges.shape[0]

    def last_elements(self) -> NDArray[Shape["element_nr, ... element_shape"], np.dtype[np.number]]: 
        """
        last_elements() -> elements
        | **Description**
        |   Returns the last added elements.

        :return: Last added element
        :rtype: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        if self._last_elements is None:
            raise LookupError("there are infinit elements continues pool")
        return self._last_elements

    def elements_from_norm_pos(self, norm_pos: NDArray[Shape["element_nr, ... element_dims"], np.dtype[np.number]]) -> NDArray[Shape["element_nr, ... element_dims"], np.dtype[np.number]]: 
        """
        elements_from_norm_pos(self, norm_pos) -> elements
        | **Description**
        |   Transforms the given normed element into the permitted value range given by its element constraints.
        |   Example: Let ranges be [[[0,12], [0,12]] , [[2,14], [1,3]]] and norm_pos = [[1,0.5] , [0.25,0.5]]
        |   Then this function returns the element [[0 + 1 * 12,0 + 0.5 * 12] , [2 + 0.25 * 12, 1 + 0.5 * 2]] = [[12, 6] , [5, 2]]

        :param norm_pos: A element with values in range of [0,1]
        :type norm_pos: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :return:
        :rtype: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_

        :raises LookupError: If the set of permitted element values is discrete and empty
        :raises RuntimeWarning: If infinite is a permitted value
        """
        if self.ranges is None:
            raise LookupError("can not look up a position in a discrete pool")
        if np.any(np.isinf(self.ranges)):
            self.ranges = np.nan_to_num(self.ranges, nan=0, posinf=float(np.finfo(np.float64).max), neginf=float(np.finfo(np.float64).min))
            raise RuntimeWarning("QueryConstrain ranges are infinity, they will be converted to max float64, but most probably you forgot to provide constrains!")
        elements = self.ranges[..., 0] + (self.ranges[..., 1] - self.ranges[..., 0]) * norm_pos
        return elements
    
    def elements_from_index(self, indexes) -> NDArray[Shape["element_nr, ... element_shape"], np.dtype[np.number]]: 
        """
        elements_from_index(indexes) -> elements
        | **Description**
        |   Returns the ``indexes``-th added elements.

        :param indexes: The indexes to look up
        :type indexes: An ``iterable`` of ``int``
        :return: The elements at the indexes
        :rtype: ``iterable`` of `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        if self.ranges is None:
            raise LookupError("can not look up a index in a continues pool")
        return self.ranges[indexes]
    
    def all_elements(self) -> NDArray[Shape["element_nr, ... element_shape"], np.dtype[np.number]]: 
        """
        all_elements() -> elements
        | **Description**
        |   Returns all added elements.

        :return: All added elements
        :rtype: ``iterable`` of `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        if self.ranges is None:
            raise LookupError("there are infinit elements continues pool")
        return self.ranges

@dataclass
class QueryConstrain(Constrain):
    """
    QueryConstrain(count, shape, ranges)
    | **Description**
    |   A ``QueryConstrain`` describes what kind of queries the given ``Queryable`` object accepts.
    |   Queries can be constrained in 3 ways: count, shape, and value ranges.

    :param count: How many queries can be made
    :type count: ``int``
    :param shape: What shape the queries must have
    :type shape: `Array Shape <https://www.w3schools.com/python/numpy/numpy_array_shape.asp>`_
    :param ranges: A set of all permitted query values for discrete data sources OR of lower/upper bound per dimension for continuous data sources
    :type ranges: Union of `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
    :return: No return
    :rtype: None
    """
    def queries_from_norm_pos(self, norm_pos: NDArray[Shape["element_nr, ... element_dims"], np.dtype[np.number]]) -> NDArray[Shape["element_nr, ... element_dims"], np.dtype[np.number]]: 
        return self.elements_from_norm_pos(norm_pos=norm_pos)
    
    def queries_from_index(self, indexes) -> NDArray[Shape["element_nr, ... element_shape"], np.dtype[np.number]]: 
        return self.elements_from_index(indexes= indexes)
    
    def all_queries(self) -> NDArray[Shape["element_nr, ... element_shape"], np.dtype[np.number]]: 
        return self.all_queries()

@dataclass
class ResultConstrain(Constrain):
    """
    ResultConstrain(shape, ranges)
    | **Description**
    |   A ``ResultConstrain`` describes what kind of results the given ``Queryable`` object gives.
    |   Results can be constrained in 2 ways: shape, and value ranges.

    :param count: How many queries can be made
    :type count: ``int``
    :param shape: What shape the queries must have
    :type shape: `Array Shape <https://www.w3schools.com/python/numpy/numpy_array_shape.asp>`_
    :param ranges: A set of all permitted query values
    :type ranges: Union of `NDArrays <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
    """
    ...

    
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