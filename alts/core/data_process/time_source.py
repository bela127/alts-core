from __future__ import annotations
from typing import TYPE_CHECKING

from abc import abstractmethod

from alts.core.configuration import Configurable
from alts.core.data.constrains import ResultConstrained, ResultConstrain


if TYPE_CHECKING:
    from nptyping import NDArray, Shape, Number


class TimeSource(Configurable, ResultConstrained):

    @abstractmethod
    def step(self, iteration: int) -> NDArray[Shape["time_step_nr, [time]"], Number]:
        raise NotImplementedError()
    
    @property
    def time(self)-> float:
        raise NotImplementedError()

    @property
    def result_constrain(self) -> ResultConstrain:
        return ResultConstrain(shape=(1,))
    
    @time.setter
    def time(self, time):
        raise NotImplementedError()