from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field

if TYPE_CHECKING:
    from typing_extensions import Self
    from typing import Tuple
    from nptyping import NDArray, Number, Shape
    from alts.core.configuration import Required

from alts.core.configuration import is_set, init, post_init, pre_init

from alts.core.data_process.time_source import TimeSource
from alts.core.data.constrains import DelayedConstrained
from alts.core.data.data_pools import SPRDataPools
from alts.core.queryable import Queryable

@dataclass
class Process(Queryable, DelayedConstrained):

    time_source: TimeSource = post_init()
    data_pools: SPRDataPools = post_init()

    last_queries: NDArray[Shape["data_nr, ... query_shape"], Number] = post_init()
    last_results: NDArray[Shape["data_nr, ... result_shape"], Number] = post_init()
    has_new_data: bool = pre_init(default=False)
    ready: bool = pre_init(default=True)

    def __post_init__(self):
        super().__post_init__()
        self.data_pools.process = self.data_pools.process(query_constrain=self.query_constrain, result_constrain=self.result_constrain)
        self.data_pools.result = self.data_pools.result(query_constrain=self.query_constrain, result_constrain=self.delayed_constrain)
    
    def update(self):
        raise NotImplementedError()

    def delayed_results(self) -> Tuple[NDArray[Shape["data_nr, ... query_shape"], Number], NDArray[Shape["data_nr, ... result_shape"], Number]]:
        raise NotImplementedError()
    
    def __call__(self, time_source: Required[TimeSource] = None, data_pools: Required[SPRDataPools] = None, **kwargs) -> Self:
        obj = super().__call__(**kwargs)
        obj.time_source = is_set(time_source)
        obj.data_pools = is_set(data_pools)

        return obj