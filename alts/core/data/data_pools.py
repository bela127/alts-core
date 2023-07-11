from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from alts.core.subscribable import Subscribable
from alts.core.data.queried_data_pool import QueriedDataPool
from alts.core.configuration import is_set, init, post_init, pre_init


class DataPools(Subscribable):

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self

@dataclass
class SPRDataPools(DataPools):
    stream: QueriedDataPool = init()
    process: QueriedDataPool = init()
    result: QueriedDataPool = init()