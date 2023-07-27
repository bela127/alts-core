from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field


from alts.core.subscriber import ResultDataSubscriber, StreamDataSubscriber, ProcessDataSubscriber
from alts.core.query.queryable import Queryable
from alts.core.experiment_module import ExperimentModule


if TYPE_CHECKING:
    from typing import Tuple
    from typing_extensions import Self #type: ignore
    from nptyping import NDArray, Number, Shape

@dataclass
class DataSampler(Queryable, ExperimentModule):

    def query(self, queries: NDArray[Shape["query_nr, ... query_dim"], Number], size = None) -> Tuple[NDArray[Shape["query_nr, sample_size, ... query_dim"], Number], NDArray[Shape["query_nr, sample_size,... result_dim"], Number]]:
        raise NotImplementedError()

@dataclass
class ResultDataSampler(ResultDataSubscriber, DataSampler):
    pass

@dataclass
class StreamDataSampler(StreamDataSubscriber, DataSampler):
    pass

@dataclass
class ProcessDataSampler(ProcessDataSubscriber, DataSampler):
    pass
