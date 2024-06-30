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
    shape: Tuple[int, ...]
    ranges: NDArray[Shape["... element_dims,[xi_min, xi_max]"], Number]

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
    
    def matches_ranges(self, element):
        """
        | **Description**
        |   Checks whether the entries of the given element fall within their respective allowed range.
        |   Checks for shape conformity first.

        :param elements: The element to check for range conformity
        :type elements: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :return: Check result
        :rtype: Boolean
        """
        if not self.matches_shape(element.shape()): return False
        for index, value in np.ndenumerate(element):
            if self.ranges[index][0] > value or self.ranges[index][1] < value: return False
        return True
    
    def constraints_met(self, elements):
        """
        | **Description**
        |   Checks whether the given list of elements fulfills count, shape and range constraints.

        :param elements: The list of elements to check for count conformity
        :type elements: iterable
        :return: Check result
        :rtype: Boolean
        """
        for element in elements:
            if not self.matches_shape(element.shape): return False
            if not self.matches_ranges(element): return False
        return True

    def add_constraint(self, element: NDArray[Shape["... element_dims,[xi_min, xi_max]"], Number]):
        if self.ranges is None:
            self.ranges = element
        else: 
            lower = True
            for index, value in np.ndenumerate(element):
                if lower and value > self.ranges[index]:
                    self.ranges[index] = value
                elif not lower and value < self.ranges[index]:
                    self.ranges[index] = value
                lower = not lower
                
        self._last_added_constraint = element

    def last_added_constraint(self):
        if self._last_added_constraint is None:
            raise LookupError("there are infinite elements in a continuous pool")
        return self._last_added_constraint

@dataclass
class QueryConstraint(Constraint):
    count: Optional[int]
    
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

@dataclass
class ResultConstraint(Constraint):
    ...

class QueryConstrained():
    
    @abstractmethod
    def query_constrain(self) -> QueryConstraint:
        raise NotImplementedError()

class ResultConstrained():
    
    @abstractmethod
    def result_constrain(self) -> ResultConstraint:
        raise NotImplementedError()

class DelayedConstrained():
    
    @abstractmethod
    def delayed_constrain(self) -> ResultConstraint:
        raise NotImplementedError()

class Constrained(QueryConstrained, ResultConstrained):
    pass

ResultConstrainGetter = Callable[[],ResultConstraint]

QueryConstrainedGetter = Callable[[],QueryConstraint]