#TODO D
from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING

from dataclasses import dataclass, field

from alts.core.experiment_module import ExperimentModule
from alts.core.configuration import init


if TYPE_CHECKING:
    from typing_extensions import Self #type: ignore
    from typing import Optional
    from nptyping import NDArray, Number, Shape


@dataclass
class QuerySampler(ExperimentModule):
    num_queries: int = init(default=1)

    @abstractmethod
    def sample(self, num_queries: Optional[int] = None) -> NDArray[Shape["query_nr, ... query_dims"], Number]: # type: ignore
        raise NotImplementedError("Please use a non abstract ...QuerySampler.")
