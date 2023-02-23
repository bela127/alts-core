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
from alts.core.data.queried_data_pool import QueriedDataPool
from alts.core.queryable import Queryable

@dataclass
class Process(Queryable, DelayedConstrained):

    time_source: TimeSource = post_init()
    stream_data_pool: QueriedDataPool = post_init()

    last_queries: NDArray[Shape["data_nr, ... query_shape"], Number] = post_init()
    last_results: NDArray[Shape["data_nr, ... result_shape"], Number] = post_init()
    has_new_data: bool = pre_init(default=False)
    ready: bool = pre_init(default=True)

    
    def update(self):
        raise NotImplementedError()

    def delayed_results(self) -> Tuple[NDArray[Shape["data_nr, ... query_shape"], Number], NDArray[Shape["data_nr, ... result_shape"], Number]]:
        raise NotImplementedError()
    
    def __call__(self, time_source: Required[TimeSource] = None, stream_data_pool: Required[QueriedDataPool] = None, **kwargs) -> Self:
        obj = super().__call__(**kwargs)
        obj.time_source = is_set(time_source)
        obj.stream_data_pool = is_set(stream_data_pool)
        return obj