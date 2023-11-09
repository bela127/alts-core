from __future__ import annotations
from typing import TYPE_CHECKING

from abc import abstractmethod

from alts.core.experiment_module import ExperimentModule
from alts.core.subscriber import ExpModSubscriber, ResultDataSubscriber

if TYPE_CHECKING:
    from nptyping import  NDArray, Number, Shape
    from alts.core.subscribable import Subscribable

class Estimator(ExperimentModule, ExpModSubscriber, ResultDataSubscriber):

    @abstractmethod
    def estimate(self, exp_mods) -> NDArray[Shape["query_nr, ... result_dim"], Number]:
        raise NotImplementedError()

    @abstractmethod
    def query(self, queries):
        raise NotImplementedError()

    def train(self, result_pool) -> None:
        pass

    def result_update(self, subscription: Subscribable):
        super().result_update(subscription)
        self.train(subscription)
        

    def experiment_update(self, subscription: Subscribable):
        super().experiment_update(subscription)
        self.estimate(subscription)
        