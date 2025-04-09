#Version 1.1.1 conform as of 16.12.2024
"""
| *alts.core.subscriber*
"""
from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING
from alts.core.configuration import Required, post_init

from alts.core.configuration import Configurable

if TYPE_CHECKING:
    from typing import Tuple, Callable
    from typing_extensions import Self #type: ignore
    from nptyping import NDArray, Number, Shape
    from alts.core.data.data_pools import DataPools, StreamDataPools, ProcessDataPools, ResultDataPools
    from alts.core.data_process.time_source import TimeSource
    from alts.core.subscribable import Subscribable
    from alts.core.oracle.oracles import Oracles, POracles
    from alts.core.experiment_modules import ExperimentModules




class Subscriber(Configurable):
    """
    Subscriber()
    | **Description**
    |   A Subscriber is capable of subscribing to a Subscribable and trying to update a Subscribable.
    """
    def post_init(self):
        """
        post_init(self) -> None
        | **Description**
        |   Initializes the Configurable and subscribes.
        """
        super().post_init()
        self.subscribe()        

    @abstractmethod
    def update(self, subscription: Subscribable) -> None:
        """
        update(self, subscription) -> None
        | **Description**
        |   Receives notification of the updated subscription.
        |   Abstract Method

        :param subscription: The subscription that is updated
        :type subscription: Subscribable
        """
        pass

    @abstractmethod
    def subscribe(self) -> None:
        """
        subscribe(self) -> None
        | **Description**
        |   Subscribes to all necessary things... nothing right now.
        |   Abstract Method
        """
        print(f"{self.__class__} subscribed...")
        pass


class DataPoolsSubscriber(Subscriber):
    """
    DataPoolsSubscriber()
    | **Description**
    |   A Subscriber of DataPools.
    """
    data_pools: DataPools

class StreamDataSubscriber(DataPoolsSubscriber):
    """
    StreamDataSubscriber()
    | **Description**
    |   A Subscriber of StreamDataPools.
    """
    data_pools: StreamDataPools

    def stream_update(self, subscription: Subscribable):
        """
        stream_update(self, subscription) -> None
        | **Description**
        |   Receives notification of the updated subscription.

        :param subscription: The updated subscription
        :type subscription: Subscribable
        """
        self.update(subscription)

    def subscribe(self) -> None:
        """
        subscribe(self) -> None
        | **Description**
        |   Subscribes to its ``StreamDataPools``.
        """
        super().subscribe()
        self.data_pools.stream.subscribe(self, self.stream_update) # type: ignore
        print(f"to {self.data_pools.stream.__class__}")
        

class ProcessDataSubscriber(DataPoolsSubscriber):
    """
    ProcessDataSubscriber()
    | **Description**
    |   A Subscriber of StreamDataPools.
    """
    data_pools: ProcessDataPools

    def process_update(self, subscription: Subscribable):
        """
        process_update(self, subscription) -> None
        | **Description**
        |   Receives notification of the updated subscription.

        :param subscription: The updated subscription
        :type subscription: Subscribable
        """
        self.update(subscription)

    def subscribe(self) -> None:
        """
        subscribe(self) -> None
        | **Description**
        |   Subscribes to its ``ProcessDataPools``.
        """
        super().subscribe()
        self.data_pools.process.subscribe(self, self.process_update) # type: ignore
        print(f"to {self.data_pools.process.__class__}")
        

class ResultDataSubscriber(DataPoolsSubscriber):
    """
    ResultDataSubscriber()
    | **Description**
    |   A Subscriber of ResultDataPools.
    """
    data_pools: ResultDataPools

    def result_update(self, subscription: Subscribable):
        """
        result_update(self, subscription) -> None
        | **Description**
        |   Receives notification of the updated subscription.

        :param subscription: The updated subscription
        :type subscription: Subscribable
        """
        self.update(subscription)

    def subscribe(self) -> None:
        """
        subscribe(self) -> None
        | **Description**
        |   Subscribes to its ``ResultDataPools``.
        """
        super().subscribe()
        self.data_pools.result.subscribe(self, self.result_update) # type: ignore
        print(f"to {self.data_pools.result.__class__}")

class ExpModSubscriber(Subscriber):
    """
    ExpModSubscriber()
    | **Description**
    |   A Subscriber of ExperimentModules.
    """
    exp_modules: ExperimentModules = post_init()

    def experiment_update(self, subscription: Subscribable):
        """
        experiment_update(self, subscription) -> None
        | **Description**
        |   Receives notification of the updated subscription.

        :param subscription: The updated subscription
        :type subscription: Subscribable
        """
        self.update(subscription)

    def subscribe(self) -> None:
        """
        subscribe(self) -> None
        | **Description**
        |   Subscribes to its ``ExperimentDataPools``.
        """
        super().subscribe()
        self.exp_modules.subscribe(self, self.experiment_update) # type: ignore
        print(f"to {self.exp_modules.__class__}")

class TimeSubscriber(Subscriber):
    """
    TimeSubscriber()
    | **Description**
    |   A Subscriber of TimeSource.
    """
    time_source: TimeSource = post_init()

    def time_update(self, subscription: Subscribable):
        """
        time_update(self, subscription) -> None
        | **Description**
        |   Receives notification of the updated subscription.

        :param subscription: The updated subscription
        :type subscription: Subscribable
        """
        self.update(subscription)

    def subscribe(self) -> None:
        """
        subscribe(self) -> None
        | **Description**
        |   Subscribes to its ``TimeSource``.
        """
        super().subscribe()
        self.time_source.subscribe(self, self.time_update) # type: ignore
        print(f"to {self.time_source.__class__}")

class OraclesSubscriber(Subscriber):
    """
    OraclesSubscriber()
    | **Description**
    |   A Subscriber of Oracles.
    """
    oracles: Oracles

class ProcessOracleSubscriber(OraclesSubscriber):
    """
    ProcessOracleSubscriber()
    | **Description**
    |   A Subscriber of POracles.
    """
    oracles: POracles

    def process_query(self, subscription: Subscribable):
        """
        process_query(self, subscription) -> None
        | **Description**
        |   Receives notification of the updated subscription.

        :param subscription: The updated subscription
        :type subscription: Subscribable
        """
        self.update(subscription)

    def subscribe(self) -> None:
        """
        subscribe(self) -> None
        | **Description**
        |   Subscribes to its ``Oracles``.
        """
        super().subscribe()
        self.oracles.process.subscribe(self, self.process_query) # type: ignore
        print(f"to {self.oracles.process.__class__}")