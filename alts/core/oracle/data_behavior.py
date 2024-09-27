#TODO NID
from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field

import numpy as np

from alts.core.configuration import Configurable

if TYPE_CHECKING:
    from typing_extensions import Self
    from typing import Tuple
    from nptyping import  NDArray, Number, Shape

@dataclass
class DataBehavior(Configurable):
    """
    | **Description**
    |   Describes how the data is behaving over time.
    |   Dimensions: Frequency of change, lowest value, highest value, lowest/highest time data is available for
    """
    change_interval: float = 5
    lower_value: float=-1
    upper_value: float=1

    start_time: float = 0.
    stop_time: float = 600.

    def behavior(self) -> Tuple[NDArray[Shape["change_times"], Number], NDArray[Shape["change_values"], Number]]: # type: ignore
        raise NotImplementedError()
