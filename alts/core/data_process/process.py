from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field
import numpy as np

if TYPE_CHECKING:
    from typing_extensions import Self
    from typing import Tuple
    from nptyping import NDArray, Number, Shape
    from alts.core.configuration import Required
    from alts.core.oracle.oracles import Oracles
    from alts.core.data.data_pools import DataPools



from alts.core.configuration import is_set, init, post_init, pre_init, NOTSET, Configurable

from alts.core.data_process.time_source import TimeSource
from alts.core.query.queryable import Queryable


class Process(Configurable, Queryable):

    time_source: TimeSource = post_init()
    data_pools: DataPools = post_init()
    oracles: Oracles = post_init()

    last_queries: NDArray[Shape["data_nr, ... query_shape"], Number] = post_init()
    last_results: NDArray[Shape["data_nr, ... result_shape"], Number] = post_init()


    def initialize(self):
        pass
    
    def step(self, iteration):
        return None, None, None, None
    
    def __call__(self, time_source: Required[TimeSource] = None, oracles: Required[Oracles] = None, data_pools: Required[DataPools] = None, **kwargs) -> Self:
        obj = super().__call__(**kwargs)
        obj.time_source = is_set(time_source)
        obj.data_pools = is_set(data_pools)
        obj.oracles = is_set(oracles)

        return obj