from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass


if TYPE_CHECKING:
    from typing import Iterable, Optional

    from alts.core.data.data_pools import DataPools
    from alts.core.evaluator import Evaluator
    from alts.core.experiment_modules import ExperimentModules
    from alts.core.stopping_criteria import StoppingCriteria
    from alts.core.data_process.observable_filter import ObservableFilter
    from alts.core.data_process.process import Process
    from alts.core.data_process.time_source import TimeSource
    from alts.core.oracle.oracles import Oracles



@dataclass
class Blueprint():
    repeat: int

    time_source: TimeSource

    oracles: Oracles

    data_pools: DataPools

    process: Process

    stopping_criteria: StoppingCriteria

    experiment_modules: ExperimentModules

    evaluators: Iterable[Evaluator]

    exp_name: Optional[str]= None
    exp_path: Optional[str]= None