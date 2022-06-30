from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field
from alts.core.configuration import Configurable


if TYPE_CHECKING:
    from alts.core.data.queried_data_pool import QueriedDataPool
    from alts.core.data.data_pool import DataPool
    from alts.core.query.query_pool import QueryPool

    from typing_extensions import Self #type: ignore

@dataclass
class ExperimentModules(Configurable):
    queried_data_pool: QueriedDataPool = field(init=False)
    oracle_data_pool: DataPool = field(init=False)

    def run(self):
        ...

    def __call__(self, queried_data_pool: QueriedDataPool = None, oracle_data_pool: DataPool = None, **kwargs) -> Self:
        obj = super().__call__(**kwargs)
        if not queried_data_pool is None:
            obj.queried_data_pool = queried_data_pool
        else:
            raise ValueError
        if not oracle_data_pool is None:
            obj.oracle_data_pool = oracle_data_pool
        else:
            raise ValueError
        return obj
