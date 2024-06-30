#TODO NID
from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field
from abc import abstractmethod

from alts.core.experiment_module import ExperimentModule
from alts.core.data.constrains import QueryConstrained, QueryConstrain

if TYPE_CHECKING:
    from typing import Tuple, Optional
    from nptyping import NDArray, Number, Shape

@dataclass
class QueryDecider(ExperimentModule, QueryConstrained):

    @abstractmethod
    def decide(self, query_candidates: NDArray[Shape["query_nr, ... query_dims"], Number], scores: NDArray[Shape["query_nr, [query_score]"], Number]) -> Tuple[bool, NDArray[Shape["query_nr, ... query_dims"], Number]]: # type: ignore
        raise NotImplementedError()