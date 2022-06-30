from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass

if TYPE_CHECKING:
    from typing import Iterable, Optional

    from alts.core.data.queried_data_pool import QueriedDataPool
    from alts.core.oracle.oracle import Oracle
    from alts.core.query.query_optimizer import QueryOptimizer
    from alts.core.query.query_sampler import QuerySampler
    from alts.core.evaluator import Evaluator
    from alts.core.experiment_modules import ExperimentModules
    from alts.core.stopping_criteria import StoppingCriteria


@dataclass
class Blueprint():
    repeat: int

    stopping_criteria: StoppingCriteria

    oracle: Oracle

    queried_data_pool: QueriedDataPool

    initial_query_sampler: QuerySampler

    query_optimizer: QueryOptimizer

    experiment_modules: ExperimentModules

    evaluators: Iterable[Evaluator]

    exp_name: Optional[str]= None

    exp_path: Optional[str]= None