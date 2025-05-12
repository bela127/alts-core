#Version 1.1.1 conform as of 18.12.2024
"""
| *alts.core.experiment_modules*
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field
from alts.core.configuration import Configurable, Required, is_set, post_init, pre_init, init
from alts.core.oracle.oracles import Oracles, POracles
from alts.core.subscribable import Publisher
from alts.core.estimator import Estimator


if TYPE_CHECKING:
    from alts.core.data.data_pools import DataPools
    from alts.core.query.query_selector import QuerySelector
    from alts.core.data_process.time_source import TimeSource
    from alts.core.query.query_sampler import QuerySampler

    from typing_extensions import Self #type: ignore

@dataclass
class ExperimentModules(Publisher):
    """
    ExperimentModules(query_selector)
    | **Description**
    |   ExperimentModules is a collection of configured modules necessary for an experiment.

    :param query_selector: Decider over the most useful datapoints for continued learning
    :type query_selector: QuerySelector
    """
    query_selector: QuerySelector = init()

    time_source: TimeSource = post_init()
    data_pools: DataPools = post_init()
    oracles: Oracles = post_init()

    def post_init(self):
        """
        post_init(self) -> None
        | **Description**
        |   Initializes the ``query_selector`` with its configuration.
        """
        super().post_init()
        self.query_selector = self.query_selector(exp_modules = self) # type: ignore
    
    def initialize(self):
        """
        initialize(self) -> None
        | **Description**
        |   Initializes the experiment.
        """
        pass

    def step(self, iteration):
        """
        step(self, iteration) -> None
        | **Description**
        |   Does a step in the experiment at time point ``iteration``.

        :param iteration: Current iteration of the experiment
        :type iteration: int
        """
        self.update()

    def __call__(self, time_source: Required[TimeSource] = None, data_pools: Required[DataPools] = None, oracles: Required[Oracles] = None, **kwargs) -> Self:
        """
        __call_(self, time_source, data_pools, oracles, **kwargs) -> ExperimentModules
        | **Description**
        |   Creates and returns a new insance of itself with the given configuration.

        :param query_selector: Decider over the most useful datapoints for continued learning
        :type query_selector: QuerySelector
        :param time_source: A time source for the experiment
        :type time_source: TimeSource
        :param data_pools: Collector of already acquired data
        :type data_pools: DataPools
        :param oracles: The source of new data
        :type oracles: Oracles
        :return: Newly configured ExperimentModules
        :rtype: ExperimentModules
        """
        obj = super().__call__(**kwargs)
        obj.time_source = is_set(time_source)
        obj.data_pools = is_set(data_pools)
        obj.oracles = is_set(oracles)
        return obj
    
@dataclass
class InitQueryExperimentModules(ExperimentModules):
    """
    InitQueryExperimentModules(query_selector, time_source, data_pools, poracles, initial_query_sampler)
    | **Description**
    |   InitQueryExperimentModules additionally has an initial QuerySampler and a Process Oracle.

    :param query_selector: Decider over the most useful datapoints for continued learning
    :type query_selector: QuerySelector
    :param time_source: A time source for the experiment
    :type time_source: TimeSource
    :param data_pools: Collector of already acquired data
    :type data_pools: DataPools
    :param oracles: The source of new data
    :type oracles: POracles
    :param initial_query_sampler: A sampler to get the very first datapoints
    :type initial_query_sampler: QuerySampler
    """
    initial_query_sampler: QuerySampler = init()

    oracles: POracles = post_init()

    def post_init(self):
        """
        post_init(self) -> None
        | **Description**
        |   Initializes the ``query_selector`` and ``init_query_sampler`` with its configuration.

        :raises TypeError: If ``oracles`` is not a ``POracle``
        """
        super().post_init()
        self.initial_query_sampler = self.initial_query_sampler(exp_modules = self) # type: ignore

        if not isinstance(self.oracles, POracles):
            raise TypeError(f"InitQueryExperimentModules requires POracles")
    
    def initialize(self):
        """
        initialize(self) -> None
        | **Description**
        |   Initializes the experiment by sampling the first queries for the experiment.
        """
        super().initialize()
        self.init_queries()
        
    def init_queries(self):
        """
        init_queries(self) -> None
        | **Description**
        |   Samples the inital queries and adds them to the oracle.

        :return: The sampled queries
        :rtype: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        queries = self.initial_query_sampler.sample()
        self.oracles.add(queries)
        return queries

@dataclass
class EstimatorExperiment(ExperimentModules):
    """
    EstimatorExperiment(query_selector, time_source, data_pools, poracles, estimator)
    | **Description**
    |   EstimatorExperiment additionally has an estimator to train on the data.

    :param query_selector: Decider over the most useful datapoints for continued learning
    :type query_selector: QuerySelector
    :param time_source: A time source for the experiment
    :type time_source: TimeSource
    :param data_pools: Collector of already acquired data
    :type data_pools: DataPools
    :param oracles: The source of new data
    :type oracles: Oracles
    :param estimator: An estimator that trains with the acquired data
    :type estimator: Estimator
    """
    estimator: Estimator = init()

    def post_init(self):
        """
        post_init(self) -> None
        | **Description**
        |   Initializes the ``query_selector`` and ``estimator`` with its configuration.
        """
        super().post_init()
        self.estimator = self.estimator(exp_modules = self) # type: ignore

@dataclass
class InitQueryEstimatorExperiment(InitQueryExperimentModules, EstimatorExperiment):
    """
    InitQueryEstimatorExperiment(query_selector, time_source, data_pools, poracles, initial_query_sampler, estimator)
    | **Description**
    |   InitQueryEstimatorExperiment is an experiment setup with an initial query sample and an estimator to train.

    :param query_selector: Decider over the most useful datapoints for continued learning
    :type query_selector: QuerySelector
    :param time_source: A time source for the experiment
    :type time_source: TimeSource
    :param data_pools: Collector of already acquired data
    :type data_pools: DataPools
    :param oracles: The source of new data
    :type oracles: POracles
    :param initial_query_sampler: A sampler to get the very first datapoints
    :type initial_query_sampler: QuerySampler
    :param estimator: An estimator that trains with the acquired data
    :type estimator: Estimator
    """
    pass