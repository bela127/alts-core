#TODO D
from __future__ import annotations
from typing import TYPE_CHECKING

from abc import abstractmethod


from alts.core.configuration import Configurable
from alts.core.data.constrains import ResultConstrained, ResultConstrain
from alts.core.subscribable import Publisher


if TYPE_CHECKING:
    from nptyping import NDArray, Shape, Number

class TimeSource(Publisher, ResultConstrained):
    time_step: float = 1

    def step(self, iteration: int) -> NDArray[Shape["time_step_nr, [time]"], Number]: # type: ignore
        self.update()
    
    @property
    def time(self)-> float:
        raise NotImplementedError()

    def result_constrain(self) -> ResultConstrain:
        return ResultConstrain(shape=(1,))
    
    @time.setter
    def time(self, time):
        raise NotImplementedError()