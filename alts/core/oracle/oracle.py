from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field

from alts.core.configuration import Configurable, Required, is_set

from alts.core.oracle.query_queue import QueryQueue
from alts.core.data.constrains import QueryConstrained, QueryConstrain


if TYPE_CHECKING:
    from typing_extensions import Self #type: ignore
    from typing import Tuple
    from nptyping import NDArray, Number, Shape


class Oracle(QueryConstrained):
    """
    Request a query
    """
    query_queue: QueryQueue

    def __init__(self, query_queue: QueryQueue) -> None:
        self.query_queue = is_set(query_queue)

    def request(self, query_candidates: NDArray[Shape["query_nr, ... query_dim"], Number]):
        self.query_queue.add(query_candidates)

    @property
    def query_constrain(self) -> QueryConstrain:
        return self.query_queue.query_constrain