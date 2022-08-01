from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np

from alts.core.queryable import Queryable

if TYPE_CHECKING:
    from typing_extensions import Self #type: ignore
    from typing import Tuple, List, Dict

    from nptyping import  NDArray, Number, Shape

    from alts.core.data_subscriber import DataSubscriber
    from alts.core.query.query_pool import QueryPool
    from alts.core.data.data_pool import DataPool


class QueriedDataPool(Queryable):
    _oracle_query_pool: QueryPool
    _oracle_data_pool: DataPool

    def __init__(self):
        self._subscriber: List[DataSubscriber] = []

        self.queries: NDArray[Shape["query_nr, ... query_dim"], Number] = None
        self.results: NDArray[Shape["query_nr, ... result_dim"], Number] = None

        self.last_queries: NDArray[Shape["query_nr, ... query_dim"], Number] = None
        self.last_results: NDArray[Shape["query_nr, ... result_dim"], Number] = None

    def subscribe(self, subscriber):
        self._subscriber.append(subscriber)


    def add(self, data_points: Tuple[NDArray[Shape["query_nr, ... query_dim"], Number], NDArray[Shape["query_nr, ... result_dim"], Number]]):
        queries, results = data_points


        self.queries = np.concatenate((self.queries, queries))
        self.results = np.concatenate((self.results, results))
        
        self.last_queries = queries
        self.last_results = results

        for subscriber in self._subscriber:
            subscriber.update()
        
    def __call__(self, oracle_query_pool: QueryPool = None, oracle_data_pool: DataPool = None, **kwargs) -> Self:
        obj = super().__call__( **kwargs)
        obj._oracle_query_pool = oracle_query_pool
        obj._oracle_data_pool = oracle_data_pool

        obj.queries = np.empty((0,*obj._oracle_query_pool.query_shape))
        obj.results = np.empty((0,*obj._oracle_data_pool.result_shape))

        obj.last_queries = np.empty((0,*obj._oracle_query_pool.query_shape))
        obj.last_results = np.empty((0,*obj._oracle_data_pool.result_shape))


        return obj
    
