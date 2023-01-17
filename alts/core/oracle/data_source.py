from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field

from alts.core.queryable import Queryable
from alts.core.data.constrains import QueryConstrain, ResultConstrain

import numpy as np

if TYPE_CHECKING:
    from typing import Tuple, List
    from nptyping import NDArray, Shape, Number

@dataclass
class DataSource(Queryable):

    query_shape: Tuple[int,...]
    result_shape: Tuple[int,...]

    def query(self, queries: NDArray[ Shape["query_nr, ... query_dim"], Number]) -> Tuple[NDArray[Shape["query_nr, ... query_dim"], Number], NDArray[Shape["query_nr, ... result_dim"], Number]]:
        raise NotImplementedError
 
    @property
    def query_constrain(self) -> QueryConstrain:
        query_ranges = np.asarray(tuple((np.NINF, np.Inf) for i in range(self.query_shape[0])))
        return QueryConstrain(count=None, shape=self.query_shape, ranges=query_ranges)
    
    @property
    def result_constrain(self) -> ResultConstrain:
        return ResultConstrain(shape = self.result_shape)
    
    @property
    def exhausted(self):
        return False