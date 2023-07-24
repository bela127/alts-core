from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING
from alts.core.configuration import Required, post_init

from alts.core.configuration import Configurable

if TYPE_CHECKING:
    from typing import Tuple, Callable
    from typing_extensions import Self #type: ignore
    from nptyping import NDArray, Number, Shape
    from alts.core.data.data_pools import DataPools, StreamDataPools, ProcessDataPools, ResultDataPools
    from alts.core.data_process.time_source import TimeSource
    from alts.core.subscribable import Subscribable
    from alts.core.oracle.oracles import Oracles, POracles
    from alts.core.experiment_modules import ExperimentModules




class Subscriber():

    def __init__(self):
        super().__init__()
        self.subscribe()        

    @abstractmethod
    def update(self, subscription: Subscribable) -> None:
        pass

    @abstractmethod
    def subscribe(self) -> None:
        pass


class DataPoolsSubscriber(Subscriber):
    data_pools: DataPools

class StreamDataSubscriber(DataPoolsSubscriber):
    data_pools: StreamDataPools

    def stream_update(self, subscription: Subscribable):
        self.update(subscription)

    def subscribe(self) -> None:
        super().subscribe()
        self.data_pools.stream.subscribe(self, self.stream_update)
        

class ProcessDataSubscriber(DataPoolsSubscriber):
    data_pools: ProcessDataPools

    def process_update(self, subscription: Subscribable):
        self.update(subscription)

    def subscribe(self) -> None:
        super().subscribe()
        self.data_pools.process.subscribe(self, self.process_update)
        

class ResultDataSubscriber(DataPoolsSubscriber):
    data_pools: ResultDataPools

    def result_update(self, subscription: Subscribable):
        self.update(subscription)

    def subscribe(self) -> None:
        super().subscribe()
        self.data_pools.result.subscribe(self, self.result_update)

class ExpModSubscriber(Subscriber):
    exp_modules: ExperimentModules = post_init()

    def experiment_update(self, subscription: Subscribable):
        self.update(subscription)

    def subscribe(self) -> None:
        super().subscribe()
        self.exp_modules.subscribe(self, self.experiment_update)

class TimeSubscriber(Subscriber):
    time_source: TimeSource = post_init()

    def time_update(self, subscription: Subscribable):
        self.update(subscription)

    def subscribe(self) -> None:
        super().subscribe()
        self.time_source.subscribe(self, self.time_update)

class OraclesSubscriber(Subscriber):
    oracles: Oracles

class ProcessOracleSubscriber(OraclesSubscriber):
    oracles: POracles

    def process_query(self, subscription: Subscribable):
        self.update(subscription)

    def subscribe(self) -> None:
        super().subscribe()
        self.oracles.process.subscribe(self, self.process_query)