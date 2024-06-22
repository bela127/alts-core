from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass
from abc import abstractmethod

import numpy as np

from typing import Callable
from alts.core.configuration import ROOT

if TYPE_CHECKING:
    from typing import Tuple, Optional, Union
    from nptyping import NDArray, Number, Shape


@dataclass 
class Constraint():
    count: Optional[int]
    shape: Tuple[int, ...]
    ranges: Union[NDArray[Shape["... element_dims,[xi_min, xi_max]"], Number], NDArray[Shape["... element_dims,[xi]"], Number]]

    def matches_shape(self, shape):
        """
        | **Description**
        |   Checks whether the given element fulfills the shape constraints.

        :param shape: The shape of the element to check for shape conformity
        :type shape: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :return: Check result
        :rtype: Boolean
        """
        if len(self.shape) == len(shape):
            for dim_own, dim_ext in zip(self.shape, shape):
                if dim_own != dim_ext:
                    return False
            return True
        return False
    
    def matches_count(self, elements):
        """
        | **Description**
        |   Checks whether the given list of elements is shorter than the allowed number.

        :param elements: The list of elements to check for count conformity
        :type elements: iterable
        :return: Check result
        :rtype: Boolean
        """
        if len(elements) <= self.count:
            return True
        return False
    
    def matches_ranges(self, element):
        pass
    
    def constraints_met(self, elements):
        """
        | **Description**
        |   Checks whether the given list of elements fulfills count, shape and range constraints.

        :param elements: The list of elements to check for count conformity
        :type elements: iterable
        :return: Check result
        :rtype: Boolean
        """
        if not self.matches_count(elements): return False
        for element in elements:
            if not self.matches_shape(element.shape): return False
            if not self.matches_ranges(element): return False
        return True

    def add_constraint(self, elements: NDArray[Shape["element_count, ... element_shape"], Number]):
        if self.ranges is None:
            self.ranges = elements[..., None]
        else: 
            self.ranges = np.concatenate((self.ranges, elements[..., None]))
        self._last_added_constraint = elements
        self.element_count = self.ranges.shape[0]

    def last_added_constraint(self):
        if self._last_added_constraint is None:
            raise LookupError("there are infinite elements in a continuous pool")
        return self._last_added_constraint

    def elements_from_norm_pos(self, norm_pos: NDArray[Shape["element_nr, ... element_dims"], Number]) -> NDArray[Shape["element_nr, ... element_dims"], Number]:
        if self.ranges is None:
            raise LookupError("can not look up a position in a discrete pool")
        if np.any(np.isinf(self.ranges)):
            self.ranges = np.nan_to_num(self.ranges, nan=0, posinf=float(np.finfo(np.float64).max), neginf=float(np.finfo(np.float64).min))
            raise RuntimeWarning("ElementConstrain ranges are infinity, they will be converted to max float64, but most probably you forgot to provide constrains!")
        elements = self.ranges[..., 0] + (self.ranges[..., 1] - self.ranges[..., 0]) * norm_pos
        return elements
    
    def elements_from_index(self, indexes):
        if self.ranges is None:
            raise LookupError("can not look up a index in a continues pool")
        return self.ranges[indexes]
    
    def all_elements(self):
        if self.ranges is None:
            raise LookupError("there are infinite elements in a continuous pool")
        return self.ranges
    
@dataclass
class QueryConstrain():
    count: Optional[int]
    shape: Tuple[int, ...]
    ranges: Union[NDArray[Shape["... query_dims,[xi_min, xi_max]"], Number], NDArray[Shape["... query_dims,[xi]"], Number]]

    def matches_shape(self, shape):
        if len(self.shape) == len(shape):
            for dim_own, dim_ext in zip(self.shape, shape):
                if dim_own != dim_ext:
                    return False
            return True
        return False
    
    def constrains_met(self, queries):
        for query in queries:
            if not self.matches_shape(query.shape): return False

    def add_queries(self, queries: NDArray[Shape["query_count, ... query_shape"], Number]):
        if self.ranges is None:
            self.ranges = queries[..., None]
        else: 
            self.ranges = np.concatenate((self.ranges, queries[..., None]))
        self._last_queries = queries
        self.query_count = self.ranges.shape[0]

    def last_queries(self):
        if self._last_queries is None:
            raise LookupError("there are infinit queries continues pool")
        return self._last_queries

    def queries_from_norm_pos(self, norm_pos: NDArray[Shape["query_nr, ... query_dims"], Number]) -> NDArray[Shape["query_nr, ... query_dims"], Number]:
        if self.ranges is None:
            raise LookupError("can not look up a position in a discrete pool")
        if np.any(np.isinf(self.ranges)):
            self.ranges = np.nan_to_num(self.ranges, nan=0, posinf=float(np.finfo(np.float64).max), neginf=float(np.finfo(np.float64).min))
            raise RuntimeWarning("QueryConstrain ranges are infinity, they will be converted to max float64, but most probably you forgot to provide constrains!")
        elements = self.ranges[..., 0] + (self.ranges[..., 1] - self.ranges[..., 0]) * norm_pos
        return elements
    
    def queries_from_index(self, indexes):
        if self.ranges is None:
            raise LookupError("can not look up a index in a continues pool")
        return self.ranges[indexes]
    
    def all_queries(self):
        if self.ranges is None:
            raise LookupError("there are infinit queries continues pool")
        return self.ranges


@dataclass
class ResultConstrain():
    shape: Tuple[int,...]
    ranges: Optional[NDArray[Shape["... query_dims,[xi_min, xi_max]"], Number]] = None

class QueryConstrained():
    
    @abstractmethod
    def query_constrain(self) -> QueryConstrain:
        raise NotImplementedError()

class ResultConstrained():
    
    @abstractmethod
    def result_constrain(self) -> ResultConstrain:
        raise NotImplementedError()

class DelayedConstrained():
    
    @abstractmethod
    def delayed_constrain(self) -> ResultConstrain:
        raise NotImplementedError()

class Constrained(QueryConstrained, ResultConstrained):
    pass

ResultConstrainGetter = Callable[[],ResultConstrain]

QueryConstrainedGetter = Callable[[],QueryConstrain]