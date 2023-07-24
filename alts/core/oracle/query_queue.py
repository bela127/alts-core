from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np

from alts.core.configuration import Configurable, Required, is_set, pre_init, post_init, init
from alts.core.data.constrains import QueryConstrained
from alts.core.subscribable import DelayedSubscribable

if TYPE_CHECKING:
    from typing_extensions import Self
    from nptyping import NDArray, Shape, Number
    from typing import  Tuple
    from alts.core.data.constrains import QueryConstrainedGetter, QueryConstrain

@dataclass
class QueryQueue(QueryConstrained, DelayedSubscribable):
    queries: NDArray[Shape["query_nr, ... query_shape"], Number] = post_init()
    _query_constrain: QueryConstrainedGetter = post_init()

    _latest_add: NDArray[Shape[" ... query_shape"], Number] = post_init()
    _latest_pop: NDArray[Shape[" ... query_shape"], Number] = post_init()


    def __post_init__(self):
        super().__post_init__()
        self.queries = np.empty((0, *self.query_constrain().shape))

    def add(self, queries: NDArray[Shape["query_nr, ... query_shape"], Number]):
        self.queries = np.concatenate((self.queries, queries))
        self._latest_add = queries[-1:]
        self.request_update()
    
    def pop(self, query_nr = 1) -> NDArray[Shape["query_nr, ... query_shape"], Number]:
        poped = self.queries[:query_nr,...]
        self.queries = self.queries[query_nr:,...]
        self._latest_pop = poped
        return poped

    @property
    def last(self)-> NDArray[Shape["1, ... query_shape"], Number]:
        return self.queries[-1:,...]
    
    @property
    def first(self)-> NDArray[Shape["1, ... query_shape"], Number]:
        return self.queries[:1,...]

    @property
    def latest_add(self)-> NDArray[Shape["1, ... query_shape"], Number]:
        return self._latest_add
    
    @property
    def latest_pop(self)-> NDArray[Shape["1, ... query_shape"], Number]:
        return self._latest_pop

    @property
    def empty(self):
        return self.queries.shape[0] == 0

    def query_constrain(self) -> QueryConstrain:
        return self._query_constrain()
       

    def __call__(self, query_constrain: Required[QueryConstrainedGetter], **kwargs) -> Self:
        obj =  super().__call__(**kwargs)
        obj._query_constrain = is_set(query_constrain)
        return obj
