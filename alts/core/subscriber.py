from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING
from alts.core.configuration import Required

from alts.core.experiment_module import ExperimentModule
from alts.core.experiment_modules import ExperimentModules


if TYPE_CHECKING:
    from typing import Tuple, Callable
    from typing_extensions import Self #type: ignore
    from nptyping import NDArray, Number, Shape


class Subscriber(ExperimentModule):

    def __init__(self):
        self.__post_init__()

    def __post_init__(self):
        super().__post_init__()
        self.subscribe()

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def subscribe(self) -> None:
        pass


class StreamSubscriber(Subscriber):

    def stream_update(self):
        self.update()

    def subscribe(self) -> None:
        super().subscribe()
        self.exp_modules.data_pools.stream.subscribe(self, self.stream_update)
        

class ProcessSubscriber(Subscriber):

    def process_update(self):
        self.update()

    def subscribe(self) -> None:
        super().subscribe()
        self.exp_modules.data_pools.process.subscribe(self, self.process_update)
        

class ResultSubscriber(Subscriber):

    def result_update(self):
        self.update()

    def subscribe(self) -> None:
        super().subscribe()
        self.exp_modules.data_pools.result.subscribe(self, self.result_update)

class ExperimentSubscriber(Subscriber):

    def experiment_update(self):
        self.update()

    def subscribe(self) -> None:
        super().subscribe()
        self.exp_modules.subscribe(self, self.experiment_update)
        