from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING
from alts.core.data.data_pool import DataPool

from alts.core.oracle.data_source import DataSource
from alts.core.query.query_pool import QueryPool


if TYPE_CHECKING:
    from typing_extensions import Self
    from typing import Tuple
    from nptyping import NDArray, Number, Shape

@dataclass
class Augmentation(DataSource):

    data_source: DataSource

    @property
    def query_shape(self):
        return self.data_source.query_shape

    @property
    def result_shape(self):
        return self.data_source.result_shape


    def query(self, queries: NDArray[ Shape["query_nr, ... query_dim"], Number]) -> Tuple[NDArray[Shape["query_nr, ... query_dim"], Number], NDArray[Shape["query_nr, ... result_dim"], Number]]:
        return self.data_source.query(queries)

    @property
    def query_pool(self) -> QueryPool:
        return self.data_source.query_pool

    @property
    def data_pool(self) -> DataPool:
        return self.data_source.data_pool
    
    @property
    def exhausted(self):
        return self.data_source.exhausted
    
    def __call__(self, **kwargs) -> Self:
        obj =  super().__call__(**kwargs)
        obj.data_source = obj.data_source()
        return obj