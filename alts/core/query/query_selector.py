from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass

from alts.core.subscriber import ProcessDataSubscriber, ResultDataSubscriber, StreamDataSubscriber
from alts.core.query.query_optimizer import QueryOptimizer
from alts.core.query.query_decider import QueryDecider
from alts.core.configuration import Required, init
from alts.core.experiment_module import ExperimentModule


if TYPE_CHECKING:
    from typing_extensions import Self #type: ignore
    from alts.core.configuration import Required
    from alts.core.subscribable import Subscribable

@dataclass
class QuerySelector(ExperimentModule, StreamDataSubscriber, ProcessDataSubscriber, ResultDataSubscriber):
    query_optimizer: QueryOptimizer = init()
    query_decider: QueryDecider = init()

    def __post_init__(self):
        super().__post_init__()
        self.query_optimizer = self.query_optimizer(exp_modules = self.exp_modules)
        self.query_decider = self.query_decider(exp_modules = self.exp_modules)


    def decide(self):
        query_candidates, scores = self.query_optimizer.select()
        query_flag, queries = self.query_decider.decide(query_candidates, scores)
        if query_flag:
            self.exp_modules.oracles.process.add(queries)
    
class ResultQuerySelector(QuerySelector):
    
    def result_update(self, subscription: Subscribable):
        super().result_update(subscription)
        self.decide()

    def update(self, subscription: Subscribable) -> None:
        super().update(subscription)