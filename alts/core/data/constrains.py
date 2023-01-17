from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass
from abc import abstractproperty

import numpy as np

if TYPE_CHECKING:
    from typing import Tuple, Optional, Union
    from nptyping import NDArray, Number, Shape


@dataclass
class QueryConstrain():
    count: Optional[int]
    shape: Tuple[int, ...]
    ranges: Union[NDArray[Shape["... query_dims,[xi_min, xi_max]"], Number], NDArray[npt.Shape["... query_dims,[xi]"], Number]]


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
            self.ranges = np.nan_to_num(self.ranges, nan=0, posinf=np.finfo(np.float64).max, neginf=np.finfo(np.float64).min)
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
    
    @abstractproperty
    def query_constrain(self) -> QueryConstrain:
        raise NotImplementedError()

class ResultConstrained():
    
    @abstractproperty
    def result_constrain(self) -> ResultConstrain:
        raise NotImplementedError()

class Constrained(QueryConstrained, ResultConstrained):
    pass