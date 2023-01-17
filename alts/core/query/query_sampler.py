from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING

from dataclasses import dataclass, field

from alts.core.configuration import Configurable, Required, is_set
from alts.core.data.constrains import QueryConstrained, QueryConstrain
from alts.core.oracle.oracle import Oracle
from alts.core.experiment_module import ExperimentModule


if TYPE_CHECKING:
    from typing_extensions import Self #type: ignore
    from typing import Optional
    from nptyping import NDArray, Number, Shape


@dataclass
class QuerySampler(ExperimentModule, QueryConstrained):
    num_queries: int = 1

    @abstractmethod
    def sample(self, num_queries: Optional[int] = None) -> NDArray[Shape["query_nr, ... query_dims"], Number]:
        raise NotImplementedError

    @property
    def query_constrain(self) -> QueryConstrain:
        return self.exp_modules.oracle.query_constrain
