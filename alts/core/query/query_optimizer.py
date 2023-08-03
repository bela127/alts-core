from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass
from alts.core.configuration import Required, init

from alts.core.experiment_module import ExperimentModule
from alts.core.data.constrains import QueryConstrained

if TYPE_CHECKING:
    from typing_extensions import Self #type: ignore
    from typing import Tuple

    from alts.core.query.selection_criteria import SelectionCriteria
    from alts.core.experiment_modules import ExperimentModules
    from alts.core.query.query_sampler import QuerySampler

    from nptyping import NDArray, Number, Shape
    
@dataclass
class QueryOptimizer(ExperimentModule, QueryConstrained):
    selection_criteria: SelectionCriteria = init()

    def post_init(self):
        super().post_init()
        self.selection_criteria = self.selection_criteria(exp_modules = self.exp_modules)

    def select(self, num_queries = None) -> Tuple[NDArray[Shape["query_nr, ... query_dims"], Number], NDArray[Shape["query_nr, [query_score]"], Number]]:
        raise NotImplementedError
