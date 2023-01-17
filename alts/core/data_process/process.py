from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field

from alts.core.oracle.query_queue import QueryQueue

if TYPE_CHECKING:
    from typing_extensions import Self
    from typing import Tuple
    from nptyping import NDArray, Number, Shape
    from alts.core.configuration import Required

from alts.core.configuration import Configurable, is_set, init, post_init

from alts.core.data_process.time_source import TimeSource
from alts.core.data_process.time_behavior import TimeBehavior
from alts.core.data.constrains import Constrained, ResultConstrain, QueryConstrain

@dataclass
class Process(Configurable, Constrained):
    query_queue: QueryQueue = init()

    time_source: TimeSource = post_init()
    var_constrain: ResultConstrain  = post_init()


    def __post_init__(self):
        super().__post_init__()
        self.query_queue = self.query_queue(query_constrain = self.query_constrain)

        

    def run(self, times, vars) -> Tuple[NDArray[Shape["data_nr, ... query_shape"], Number], NDArray[Shape["data_nr, ... output_shape"], Number]]:
        raise NotImplementedError()

    @property
    def finished(self) -> bool:
        raise NotImplementedError()

    @property
    def results(self) -> Tuple[NDArray[Shape["data_nr, ... query_shape"], Number], NDArray[Shape["data_nr, ... result_shape"], Number]]:
        raise NotImplementedError()

    @property
    def queried(self) -> bool:
        return not self.query_queue.empty
    
    def __call__(self, time_source: Required[TimeSource] = None, time_behavior: Required[TimeBehavior] = None, **kwargs) -> Self:
        obj = super().__call__(**kwargs)
        obj.time_source = is_set(time_source)
        obj.var_constrain = is_set(time_behavior).result_constrain
        return obj