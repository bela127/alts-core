from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass

from alts.core.oracle.query_queue import QueryQueue
from alts.core.configuration import Configurable, is_set, init, post_init, pre_init



if TYPE_CHECKING:
    from typing_extensions import Self
    from alts.core.configuration import Required

class Oracles(Configurable):
    pass

@dataclass
class POracles(Oracles):
    process: QueryQueue = init()

    def __call__(self, *args: Any, **kwds: Any) -> Self:
        return self
