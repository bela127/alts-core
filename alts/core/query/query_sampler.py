from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING

from dataclasses import dataclass, field

from alts.core.configuration import Configurable, Required, is_set, init, post_init
from alts.core.data.constrains import QueryConstrained, QueryConstrain
from alts.core.experiment_module import ExperimentModule
from alts.core.oracle.oracles import POracles


if TYPE_CHECKING:
    from typing_extensions import Self #type: ignore
    from typing import Optional
    from nptyping import NDArray, Number, Shape


@dataclass
class QuerySampler(ExperimentModule, QueryConstrained):
    num_queries: int = init(default=1)

    @abstractmethod
    def sample(self, num_queries: Optional[int] = None) -> NDArray[Shape["query_nr, ... query_dims"], Number]:
        raise NotImplementedError

class ProcessQuerySampler(QuerySampler):

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(super().oracles, POracles):
            raise TypeError("ProcessQuerySampler requires POracles")


    @property
    def oracles(self) -> POracles:
        oracles = super().oracles
        if isinstance(oracles, POracles):
            return oracles
        else:
            raise TypeError("ProcessQuerySampler requires POracles")

    def query_constrain(self) -> QueryConstrain:
        return self.oracles.process.query_constrain()
