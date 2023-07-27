from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass

import numpy as np
from alts.core.configuration import Required, is_set, pre_init, post_init

from alts.core.query.queryable import Queryable
from alts.core.subscribable import DelayedPublisher

if TYPE_CHECKING:
    from typing_extensions import Self #type: ignore
    from typing import Tuple

    from nptyping import  NDArray, Number, Shape

    from alts.core.data.constrains import ResultConstrainGetter, QueryConstrainedGetter, Constrained


class QueriedDataPool(DelayedPublisher, Queryable):
    _query_constrain: QueryConstrainedGetter = post_init()
    _result_constrain: ResultConstrainGetter = post_init()

    def __init__(self):
        super().init(QueriedDataPool)

        self.queries: NDArray[Shape["query_nr, ... query_dim"], Number]
        self.results: NDArray[Shape["query_nr, ... result_dim"], Number]

        self.last_queries: NDArray[Shape["query_nr, ... query_dim"], Number]
        self.last_results: NDArray[Shape["query_nr, ... result_dim"], Number]

        self.queries = np.empty((0,*self._query_constrain().shape))
        self.results = np.empty((0,*self._result_constrain().shape))

        self.last_queries = np.empty((0,*self._query_constrain().shape))
        self.last_results = np.empty((0,*self._result_constrain().shape))


    def add(self, data_points: Tuple[NDArray[Shape["query_nr, ... query_dim"], Number], NDArray[Shape["query_nr, ... result_dim"], Number]]):
        queries, results = data_points

        self.queries = np.concatenate((self.queries, queries))
        self.results = np.concatenate((self.results, results))
        
        self.last_queries = queries
        self.last_results = results

        self.request_update()
        
    def __call__(self, query_constrain: Required[QueryConstrainedGetter] = None, result_constrain: Required[ResultConstrainGetter] = None, **kwargs) -> Self:
        obj = super().__call__( **kwargs)
        obj._query_constrain = is_set(query_constrain)
        obj._result_constrain = is_set(result_constrain)
        return obj
    
