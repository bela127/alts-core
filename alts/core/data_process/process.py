from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field
import numpy as np

if TYPE_CHECKING:
    from typing_extensions import Self
    from typing import Tuple
    from nptyping import NDArray, Number, Shape
    from alts.core.configuration import Required
    from alts.core.oracle.oracles import POracles
    from alts.core.data_process.time_behavior import TimeBehavior



from alts.core.configuration import is_set, init, post_init, pre_init, NOTSET

from alts.core.data_process.time_source import TimeSource
from alts.core.data.constrains import DelayedConstrained
from alts.core.data.data_pools import SPRDataPools
from alts.core.queryable import Queryable

@dataclass
class Process(Queryable, DelayedConstrained):

    time_source: TimeSource = post_init()
    data_pools: SPRDataPools = post_init()
    oracles: POracles = post_init()

    time_behavior: TimeBehavior = init()

    last_queries: NDArray[Shape["data_nr, ... query_shape"], Number] = post_init()
    last_results: NDArray[Shape["data_nr, ... result_shape"], Number] = post_init()
    has_new_data: bool = pre_init(default=False)
    ready: bool = pre_init(default=True)

    def __post_init__(self):
        super().__post_init__()
        self.oracles.process = self.oracles.process(query_constrain=self.query_constrain)
        self.time_behavior = self.time_behavior(data_pools=self.data_pools)
        self.data_pools.process = self.data_pools.process(query_constrain=self.query_constrain, result_constrain=self.result_constrain)
        self.data_pools.result = self.data_pools.result(query_constrain=self.query_constrain, result_constrain=self.delayed_constrain)
    
    def step(self):
        queries, results = self.add_intermediate_results()

        self.update()
        
        delayed_queries, delayed_results = self.add_results()
        return queries, results, delayed_queries, delayed_results

    
    def stream_update(self):
        times = np.asarray([[self.time_source.time]])
        times, vars = self.time_behavior.query(times)
        self.data_pools.stream.add((times, vars))
        return times, vars
    
    def add_intermediate_results(self):
        queries = None
        results = None
        if not self.oracles.process.empty and self.ready:
            queries = self.oracles.process.pop()
            queries, results = self.query(queries)
            self.data_pools.process.add((queries, results))
        return queries, results

    def add_results(self):
        delayed_queries = None
        delayed_results = None
        if self.has_new_data:
            delayed_queries, delayed_results = self.delayed_results()
            self.data_pools.result.add((delayed_queries, delayed_results))
        return delayed_queries, delayed_results
        

    def update(self):
        raise NotImplementedError()

    def delayed_results(self) -> Tuple[NDArray[Shape["data_nr, ... query_shape"], Number], NDArray[Shape["data_nr, ... result_shape"], Number]]:
        raise NotImplementedError()
    
    def __call__(self, time_source: Required[TimeSource] = None, oracles: Required[POracles] = None, data_pools: Required[SPRDataPools] = None, **kwargs) -> Self:
        obj = super().__call__(**kwargs)
        obj.time_source = is_set(time_source)
        obj.data_pools = is_set(data_pools)
        obj.oracles = is_set(oracles)

        return obj