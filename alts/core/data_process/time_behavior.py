from __future__ import annotations
from typing import TYPE_CHECKING

from abc import abstractmethod

from alts.core.queryable import Queryable

if TYPE_CHECKING:
    from nptyping import NDArray, Shape, Number
    from typing import Tuple


class TimeBehavior(Queryable):

    @abstractmethod
    def query(self, times: NDArray[Shape["time_step_nr, [time]"], Number]) -> Tuple[NDArray[Shape["time_step_nr, [time]"], Number], NDArray[Shape["time_step_nr, ... var_shape"], Number]]:
        raise NotImplementedError()
        