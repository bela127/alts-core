from __future__ import annotations
from typing import TYPE_CHECKING

from abc import abstractmethod


from alts.core.configuration import Configurable
from alts.core.data.constrains import ResultConstrained, ResultConstrain
from alts.core.subscribable import Subscribable


if TYPE_CHECKING:
    from nptyping import NDArray, Shape, Number

class TimeSource(ResultConstrained, Subscribable):
    time_step: float = 1

    def step(self, iteration: int) -> NDArray[Shape["time_step_nr, [time]"], Number]:
        self.update()
    
    @property
    def time(self)-> float:
        raise NotImplementedError()

    @property
    def result_constrain(self) -> ResultConstrain:
        return ResultConstrain(shape=(1,))
    
    @time.setter
    def time(self, time):
        raise NotImplementedError()