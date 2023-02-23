from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np

from alts.core.configuration import Configurable, Required, is_set, pre_init, post_init, init
from alts.core.data.constrains import QueryConstrained, QueryConstrain

if TYPE_CHECKING:
    from typing_extensions import Self
    from nptyping import NDArray, Shape, Number
    from typing import  Tuple

@dataclass
class QueryQueue(Configurable, QueryConstrained):
    queries: NDArray[Shape["query_nr, ... query_shape"], Number] = post_init()
    _query_constrain: QueryConstrain = post_init()

    _last: NDArray[Shape[" ... query_shape"], Number] = post_init()

    def __post_init__(self):
        super().__post_init__()
        self.queries = np.empty((0, *is_set(self.query_constrain).shape))

    def add(self, queries: NDArray[Shape["query_nr, ... query_shape"], Number]):
        self.queries = np.concatenate((self.queries, queries))
        self._last = queries[-1:]
    
    def pop(self, query_nr = 1) -> NDArray[Shape["query_nr, ... query_shape"], Number]:
        poped = self.queries[:query_nr,...]
        self.queries = self.queries[query_nr:,...]
        return poped

    @property
    def last(self):
        return self._last


    @property
    def empty(self):
        return self.queries.shape[0] == 0

    @property
    def query_constrain(self) -> QueryConstrain:
        return self._query_constrain
       

    def __call__(self, query_constrain: Required[QueryConstrain], **kwargs) -> Self:
        obj =  super().__call__(**kwargs)
        obj._query_constrain = is_set(query_constrain)
        return obj