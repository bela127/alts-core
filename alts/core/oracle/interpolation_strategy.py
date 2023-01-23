from __future__ import annotations
from typing import TYPE_CHECKING
from alts.core.data_sampler import DataSampler

from alts.core.configuration import Configurable
from alts.core.query.query_pool import QueryPool

from alts.core.data.constrains import QueryConstrain, QueryConstrained

if TYPE_CHECKING:
    from typing import Tuple, List, Dict
    from nptyping import NDArray, Number, Shape

class InterpolationStrategy(Configurable, QueryConstrained):
    data_sampler: DataSampler

    def interpolate(self, data_points: Tuple[NDArray[Shape["query_nr, sample_nr, ... query_dim"], Number], NDArray[Shape["query_nr, sample_nr, ... result_dim"], Number]]) -> Tuple[NDArray[Shape["query_nr, ... query_dim"], Number], NDArray[Shape["query_nr, ... result_dim"], Number]]:
        return data_points

    @property
    def query_constrain(self) -> QueryConstrain:
        return self.data_sampler.query_constrain

class NoInterpolation(InterpolationStrategy):
    ...
