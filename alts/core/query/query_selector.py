#Version 1.1.1 conform as of 13.12.2024
"""
| *alts.core.query.query_selector*
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass

from alts.core.subscriber import ProcessDataSubscriber, ResultDataSubscriber, StreamDataSubscriber
from alts.core.query.query_optimizer import QueryOptimizer
from alts.core.query.query_decider import QueryDecider
from alts.core.configuration import Required, init, is_set, post_init
from alts.core.experiment_module import ExperimentModule
from alts.core.data.constrains import QueryConstrained, QueryConstrain, ResultConstrain, QueryConstrainedGetter



if TYPE_CHECKING:
    from typing_extensions import Self #type: ignore
    from alts.core.configuration import Required
    from alts.core.subscribable import Subscribable

@dataclass
class QuerySelector(ExperimentModule, QueryConstrained):
    """
    QuerySelector(query_optimizer, query_decider)
    | **Description**
    |   The QuerySelector chooses the next queries to be queried.
    |   It utilizes the QueryOptimizer and the QueryDecider.

    :param query_optimizer: Chooses the most informative queries to be asked next
    :type query_optimizer: QueryOptimizer
    :param query_decider: Decided if the chosen queries are informative enough to be asked
    :type query_decider: QueryDecider
    """
    query_optimizer: QueryOptimizer = init()
    query_decider: QueryDecider = init()
    _query_constrain: QueryConstrainedGetter = post_init()

    def post_init(self):
        """
        post_init(self) -> None
        | **Description**
        |   Initializes ``query_optimizer`` and ``query_Decider`` with its experiment modules.
        """
        super().post_init()
        self._query_constrain = self.exp_modules.oracles.query_constrain
        self.query_optimizer = self.query_optimizer(exp_modules = self.exp_modules, query_constrain= self.query_constrain)
        self.query_decider = self.query_decider(exp_modules = self.exp_modules, query_constrain= self.query_constrain)


    def decide(self):
        """
        decide(self) -> None
        | **Description**
        |   1. Chooses the best queries with the optimizer
        |   2. Decides if chosen queries are worth the effort
        |   3. If they are worth it, forwards the chosen queries to the oracle
        """
        query_candidates, scores = self.query_optimizer.select()
        query_flag, queries = self.query_decider.decide(query_candidates, scores)
        if query_flag:
            self.oracles.add(queries)

    def query_constrain(self) -> QueryConstrain:
        """
        query_constrain(self) -> QueryConstrain
        | **Description**
        |   Returns its query constrains.

        :return: Own query constrains
        :rtype: :doc:`QueryConstrain </core/data/constrains>`
        """
        return self._query_constrain()
    
    def result_constrain(self) -> ResultConstrain:
        """
        result_constrain(self) -> ResultConstrain
        | **Description**
        |   Returns its result constrains.

        :return: Own result constrains
        :rtype: :doc:`ResultConstrain </core/data/constrains>`
        """
        return ResultConstrain(None, self._query_constrain().shape, None)



class ResultQuerySelector(QuerySelector, ResultDataSubscriber):
    """
    ResultQuerySelector(query_optimizer, query_decider)
    | **Description**
    |   Has additional access to a result data pool foor decision making.

    :param query_optimizer: Chooses the most informative queries to be asked next
    :type query_optimizer: QueryOptimizer
    :param query_decider: Decided if the chosen queries are informative enough to be asked
    :type query_decider: QueryDecider
    """
    def result_update(self, subscription: Subscribable):
        super().result_update(subscription)
        self.decide()

class StreamQuerySelector(QuerySelector, StreamDataSubscriber):
    """
    StreamQuerySelector(query_optimizer, query_decider)
    | **Description**
    |   Has additional access to a stream for decision making.

    :param query_optimizer: Chooses the most informative queries to be asked next
    :type query_optimizer: QueryOptimizer
    :param query_decider: Decided if the chosen queries are informative enough to be asked
    :type query_decider: QueryDecider
    """
    def stream_update(self, subscription: Subscribable):
        super().stream_update(subscription)
        self.decide()

class ProcessQuerySelector(QuerySelector, ProcessDataSubscriber):
    """
    ProcessQuerySelector(query_optimizer, query_decider)
    | **Description**
    |   Has additional access to a process for decision making.

    :param query_optimizer: Chooses the most informative queries to be asked next
    :type query_optimizer: QueryOptimizer
    :param query_decider: Decided if the chosen queries are informative enough to be asked
    :type query_decider: QueryDecider
    """
    def process_update(self, subscription: Subscribable):
        super().process_update(subscription)
        self.decide()