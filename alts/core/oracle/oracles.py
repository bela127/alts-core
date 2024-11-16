#Version 1.1 conform as of 16.11.2024

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
    """
    Oracles()
    | **Description**
    |   The Oracle is the interaction point between the process and the data source
    """

    def trigger_subscriber(self):
        """
        trigger_subscriber(self) -> None
        | **Description**
        |   Updates its own state upon request.
        |   Does nothing here.
        """
        pass

    def add(self, queries):
        """
        add(self, queries) -> None
        | **Description**
        |   Adds the query to it own structure.
        |   Does nothing here.

        :param queries: Requested queries
        :type queries: queries
        """
        pass

@dataclass
class POracles(Oracles):
    """
    POracles(process)
    | **Description**
    |   A Process Oracle manages the added queries into a :class:`QueryQueue`.

    :param process: The managed query queue
    :type process: QueryQueue
    """
    process: QueryQueue = init()

    def trigger_subscriber(self):
        """
        trigger_subscriber(self) -> None
        | **Description**
        |   Updates its query queue upon request.
        """
        super().trigger_subscriber()
        self.process.update()
    
    def add(self, queries):
        """
        add(self, queries) -> None
        | **Description**
        |   Adds the query to its own query queue.

        :param queries: Requested queries
        :type queries: queries
        """
        super().add(queries)
        self.process.add(queries)

    def query_constrain(self) -> QueryConstrain:
        """
        query_constrain(self) -> QueryConstrain
        | **Description**
        |   Returns the query constraints of the queue.

        :return: Its query queue's query constraints
        :rtype: QueryConstrain
        """
        return self.process.query_constrain()

    def __call__(self, *args: Any, **kwds: Any) -> Self:
        """
        __call__(self, any) -> self
        | **Description**
        |   Returns itself.

        :return: Self
        :rtype: POracles
        """
        return self
