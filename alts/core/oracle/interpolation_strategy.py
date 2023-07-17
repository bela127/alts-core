from __future__ import annotations
from typing import TYPE_CHECKING
from alts.core.data_sampler import DataSampler

from alts.core.configuration import Configurable, post_init, Required, is_set
from alts.core.query.query_pool import QueryPool

from alts.core.data.constrains import QueryConstrain, QueryConstrained

if TYPE_CHECKING:
    from typing import Tuple, List, Dict
    from nptyping import NDArray, Number, Shape

class InterpolationStrategy(Configurable, QueryConstrained):
    data_sampler: DataSampler = post_init()

    def interpolate(self, data_points: Tuple[NDArray[Shape["query_nr, sample_nr, ... query_dim"], Number], NDArray[Shape["query_nr, sample_nr, ... result_dim"], Number]]) -> Tuple[NDArray[Shape["query_nr, ... query_dim"], Number], NDArray[Shape["query_nr, ... result_dim"], Number]]:
        return data_points

    @property
    def query_constrain(self) -> QueryConstrain:
        return self.data_sampler.query_constrain
    
    def __call__(self, data_sampler: Required[DataSampler] = None, **kwargs) -> Self:
        obj = super().__call__(**kwargs)
        obj.data_sampler = is_set(data_sampler)
        return obj

class NoInterpolation(InterpolationStrategy):
    ...
