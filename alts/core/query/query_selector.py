from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass

from alts.core.subscriber import ProcessSubscriber, ResultSubscriber, StreamSubscriber
from alts.core.query.query_optimizer import QueryOptimizer
from alts.core.query.query_decider import QueryDecider
from alts.core.configuration import Required, init

if TYPE_CHECKING:
    from typing_extensions import Self #type: ignore
    from alts.core.configuration import Required
    from alts.core.experiment_modules import ExperimentModules

@dataclass
class QuerySelector(StreamSubscriber, ProcessSubscriber, ResultSubscriber):
    query_optimizer: QueryOptimizer = init()
    query_decider: QueryDecider = init()

    def __post_init__(self):
        super().__post_init__()
        self.query_optimizer = self.query_optimizer( exp_modules = self.exp_modules)
        self.query_decider = self.query_decider(exp_modules = self.exp_modules)


    def decide(self):
        query_candidates, scores = self.query_optimizer.select()
        query_flag, queries = self.query_decider.decide(query_candidates, scores)
        if query_flag:
            self.exp_modules.oracles.process.add(queries)
    
class ResultQuerySelector(QuerySelector):
    
    def result_update(self):
        super().result_update()
        self.decide()

    def update(self) -> None:
        super().update()