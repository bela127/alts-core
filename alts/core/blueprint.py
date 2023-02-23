from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass


if TYPE_CHECKING:
    from typing import Iterable, Optional

    from alts.core.data.queried_data_pool import QueriedDataPool
    from alts.core.query.query_sampler import QuerySampler
    from alts.core.evaluator import Evaluator
    from alts.core.experiment_modules import ExperimentModules
    from alts.core.stopping_criteria import StoppingCriteria
    from alts.core.data_process.observable_filter import ObservableFilter
    from alts.core.data_process.process import Process
    from alts.core.data_process.time_behavior import TimeBehavior
    from alts.core.data_process.time_source import TimeSource
    from alts.core.oracle.query_queue import QueryQueue



@dataclass
class Blueprint():
    repeat: int

    time_source: TimeSource
    time_behavior: TimeBehavior

    query_queue: QueryQueue

    process: Process

    stopping_criteria: StoppingCriteria

    stream_data_pool: QueriedDataPool
    process_data_pool: QueriedDataPool
    result_data_pool: QueriedDataPool

    initial_query_sampler: QuerySampler

    experiment_modules: ExperimentModules

    evaluators: Iterable[Evaluator]

    exp_name: Optional[str]= None
    exp_path: Optional[str]= None