from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass

from alts.core.configuration import Configurable

if TYPE_CHECKING:
    from typing import Tuple, List

@dataclass
class StoppingCriteria(Configurable):

    def next(self, iteration: int) -> bool:
        return True