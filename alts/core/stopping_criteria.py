from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field

from alts.core.configuration import Configurable

if TYPE_CHECKING:
    from typing import Tuple, List
    from alts.core.experiment import Experiment

@dataclass
class StoppingCriteria(Configurable):
    exp: Experiment = field(init=False)

    def next(self, iteration: int) -> bool:
        return True
    
    def __call__(self, exp: Experiment = None, **kwargs) -> Self:
        obj = super().__call__( **kwargs)
        obj.exp = exp
        return obj
    
