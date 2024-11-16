#Version 1.1 conform as of 16.11.2024
from __future__ import annotations
from typing import TYPE_CHECKING

from abc import abstractmethod

from alts.core.experiment_module import ExperimentModule
from alts.core.subscriber import ExpModSubscriber, ResultDataSubscriber

if TYPE_CHECKING:
    from nptyping import  NDArray, Number, Shape
    from alts.core.subscribable import Subscribable

class Estimator(ExperimentModule, ExpModSubscriber, ResultDataSubscriber):
    """
    Estimator()
    | **Description**
    |   The Estimator is the training model, trying to find patterns in given data and extrapolate them to new data.
    """
    @abstractmethod
    def estimate(self, exp_mods) -> NDArray[Shape["query_nr, ... result_dim"], Number]: # type: ignore
        """
        estimate(self, exp_mods) -> results
        | **Description**
        |   Tries to estimate the data source given a certain experiment environment based on its current training.

        :param exp_mods: The experiment modules that configure the environment of the estimator
        :type exp_mods: ExperimentModules
        :return: The estimated data structure
        :rtype: data_points
        :raises: NotImplementedError
        """
        raise NotImplementedError()

    @abstractmethod
    def query(self, queries) -> NDArray[Shape["query_nr, ... result_dim"], Number]: # type: ignore
        """
        query(self, queries) -> results
        | **Description**
        |   Tries to predict the results to given queries.

        :param queries: Queries to predict results to
        :type queries: queries
        :return: Predicted results to queries
        :rtype: results
        :raises: NotImplementedError
        """
        raise NotImplementedError()

    def train(self, result_pool) -> None:
        """
        train(self, result_pool) -> None
        | **Description**
        |   Trains the Estimator on a set of data_points.

        :param result_pool: A set of data_points
        :type result_pool: ResultDataPool
        """
        pass

    def result_update(self, subscription: Subscribable):
        """
        result_update(self, subscription) -> None
        | **Description**
        |   Updates the subscription and trains itself on the new data.

        :param subscription: A subscription the Estimator depends on
        :type subscription: Subscribable
        """
        super().result_update(subscription)
        self.train(subscription)
        

    def experiment_update(self, subscription: Subscribable):
        """
        experiment_update(self, subscription) -> None
        | **Description**
        |   Updates the subscription and tries to estimate in the new environment.

        :param subscription: Subscription to be updated
        :type subscription: Subscribable
        :return: The estimated data structure
        :rtype: data_points
        """
        super().experiment_update(subscription)
        self.estimate(subscription)
        