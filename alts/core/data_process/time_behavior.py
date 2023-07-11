from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass

from alts.core.queryable import Queryable

from alts.core.configuration import is_set, init, post_init, pre_init


if TYPE_CHECKING:
    from nptyping import NDArray, Shape, Number
    from typing import Tuple
    from typing_extensions import Self
    from alts.core.configuration import Required
    from alts.core.data.data_pools import SPRDataPools

@dataclass
class TimeBehavior(Queryable):
    data_pools: SPRDataPools = post_init()

    def __post_init__(self):
        super().__post_init__()
        self.data_pools.stream = self.data_pools.stream(constrained = self)


    def query(self, times: NDArray[Shape["time_step_nr, [time]"], Number]) -> Tuple[NDArray[Shape["time_step_nr, [time]"], Number], NDArray[Shape["time_step_nr, ... var_shape"], Number]]:
        raise NotImplementedError()
    
    def __call__(self, data_pools: Required[SPRDataPools] = None, **kwargs) -> Self:
        obj = super().__call__(**kwargs)
        obj.data_pools = is_set(data_pools)
        return obj
        