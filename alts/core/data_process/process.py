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


from alts.core.configuration import is_set, init, post_init, pre_init, NOTSET

from alts.core.data_process.time_source import TimeSource
from alts.core.data.data_pools import SPRDataPools
from alts.core.queryable import Queryable


@dataclass
class Process(Queryable):

    time_source: TimeSource = post_init()
    data_pools: SPRDataPools = post_init()
    oracles: POracles = post_init()

    last_queries: NDArray[Shape["data_nr, ... query_shape"], Number] = post_init()
    last_results: NDArray[Shape["data_nr, ... result_shape"], Number] = post_init()

    def __post_init__(self):
        super().__post_init__()
        self.oracles.process = self.oracles.process(query_constrain=self.query_constrain)

    def step(self):
        raise NotImplementedError()
    
    def __call__(self, time_source: Required[TimeSource] = None, oracles: Required[POracles] = None, data_pools: Required[SPRDataPools] = None, **kwargs) -> Self:
        obj = super().__call__(**kwargs)
        obj.time_source = is_set(time_source)
        obj.data_pools = is_set(data_pools)
        obj.oracles = is_set(oracles)

        return obj