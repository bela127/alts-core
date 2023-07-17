from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field
from alts.core.configuration import Configurable, Required, is_set, post_init, pre_init, init
from alts.core.oracle.oracles import Oracles, POracles
from alts.core.subscribable import Subscribable


if TYPE_CHECKING:
    from alts.core.data.data_pools import DataPools
    from alts.core.query.query_selector import QuerySelector
    from alts.core.data_process.time_source import TimeSource
    from alts.core.query.query_sampler import QuerySampler

    from typing_extensions import Self #type: ignore

@dataclass
class ExperimentModules(Subscribable):
    query_selector: QuerySelector = init()

    time_source: TimeSource = post_init()
    data_pools: DataPools = post_init()
    oracles: Oracles = post_init()

    def __post_init__(self):
        super().__post_init__()
        self.query_selector = self.query_selector(exp_modules = self)
    
    def init(self):
        pass

    def step(self, iteration):
        self.update()

    def __call__(self, time_source: Required[TimeSource] = None, data_pools: Required[DataPools] = None, oracles: Required[Oracles] = None, **kwargs) -> Self:
        obj = super().__call__(**kwargs)
        obj.time_source = is_set(time_source)
        obj.data_pools = is_set(data_pools)
        obj.oracles = is_set(oracles)
        return obj
    
@dataclass
class InitQueryExperimentModules(ExperimentModules):

    initial_query_sampler: QuerySampler = init()

    oracles: POracles = post_init()

    def __post_init__(self):
        super().__post_init__()
        self.initial_query_sampler = self.initial_query_sampler(exp_modules = self)

        if not isinstance(self.oracles, POracles):
            raise TypeError(f"InitQueryExperimentModules requires POracles")
    
    def init(self):
        super().init()
        self.init_queries()
        
    def init_queries(self):
        queries = self.initial_query_sampler.sample()
        self.oracles.process.add(queries)
        return queries
