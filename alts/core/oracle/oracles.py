from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass

from alts.core.oracle.query_queue import QueryQueue
from alts.core.data_process.process import Process
from alts.core.configuration import is_set, init, post_init, pre_init


if TYPE_CHECKING:
    from typing_extensions import Self
    from alts.core.configuration import Required

class Oracles():
    pass

@dataclass
class POracles(Oracles):
    process: QueryQueue = init()

    def __call__(self, process: Required[Process] = None, **kwargs) -> Self:
        process = is_set(process)
        self.process = self.process(query_constrain = process.query_constrain)
        return self
