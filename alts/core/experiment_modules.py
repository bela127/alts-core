from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field
from alts.core.configuration import Configurable, Required, is_set, post_init, pre_init, init
from alts.core.oracle.oracle import Oracle
from alts.core.subscribable import Subscribable


if TYPE_CHECKING:
    from alts.core.data.queried_data_pool import QueriedDataPool
    from alts.core.query.query_selector import QuerySelector

    from typing_extensions import Self #type: ignore

@dataclass
class ExperimentModules(Configurable, Subscribable):
    query_selector: QuerySelector = init()

    stream_data_pool: QueriedDataPool = post_init()
    process_data_pool: QueriedDataPool = post_init()
    result_data_pool: QueriedDataPool = post_init()
    oracle: Oracle = post_init()

    def __post_init__(self):
        super().__post_init__()
        self.query_selector = self.query_selector(exp_modules = self)

    def run(self):
        self.update()

    def __call__(self, stream_data_pool: Required[QueriedDataPool] = None, process_data_pool: Required[QueriedDataPool] = None, result_data_pool: Required[QueriedDataPool] = None, oracle: Required[Oracle] = None, **kwargs) -> Self:
        obj = super().__call__(**kwargs)
        obj.stream_data_pool = is_set(stream_data_pool)
        obj.process_data_pool = is_set(process_data_pool)
        obj.result_data_pool = is_set(result_data_pool)
        obj.oracle = is_set(oracle)
        return obj
