#TODO D
#QUEST trigger_subscriber?
from __future__ import annotations
from typing import TYPE_CHECKING, Any

from dataclasses import dataclass

from alts.core.oracle.query_queue import QueryQueue
from alts.core.configuration import Configurable, is_set, init, post_init, pre_init
from alts.core.data.constrains import QueryConstrained


if TYPE_CHECKING:
    from typing_extensions import Self
    from alts.core.configuration import Required
    from alts.core.data.constrains import QueryConstrain

class Oracles(Configurable, QueryConstrained):

    def trigger_subscriber(self):
        pass

    def add(self, queries):
        pass

@dataclass
class POracles(Oracles):
    process: QueryQueue = init()

    def trigger_subscriber(self):
        super().trigger_subscriber()
        self.process.update()
    
    def add(self, queries):
        super().add(queries)
        self.process.add(queries)

    def query_constrain(self) -> QueryConstrain:
        return self.process.query_constrain()

    def __call__(self, *args: Any, **kwds: Any) -> Self:
        return self
