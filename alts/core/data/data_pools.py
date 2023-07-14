from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass
from typing_extensions import Self
from alts.core.data.queried_data_pool import QueriedDataPool
from alts.core.configuration import Configurable, is_set, init, post_init, pre_init


class DataPools(Configurable):

    def trigger_subscriber(self):
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Self:
        return self

@dataclass
class SPRDataPools(DataPools):
    stream: QueriedDataPool = init()
    process: QueriedDataPool = init()
    result: QueriedDataPool = init()

    def trigger_subscriber(self):
        super().trigger_subscriber()
        self.process.update()
        self.result.update()
        self.stream.update()