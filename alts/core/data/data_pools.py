#Version 1.1 conform as of 03.10.2024
from __future__ import annotations
from typing import TYPE_CHECKING, Any

from dataclasses import dataclass
from typing_extensions import Self
from alts.core.data.queried_data_pool import QueriedDataPool
from alts.core.configuration import Configurable, is_set, init, post_init, pre_init

class DataPools(Configurable):
    """
    DataPools()
    | **Description**
    |   A ``DataPools`` stores all queries and results that have been supplied to it.
    """
    def trigger_subscriber(self):
        """
        trigger_subscriber() -> None
        | **Description**
        |   Updates its own available data.
        """
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Self:
        """
        __call__(self, any) -> Self
        | **Description**
        |   Returns a new instance of itself. 

        :param argsKeywords: Any parameters are being accepted but ignored
        :type argsKeywords: Any
        :return: An instance of this object
        :rtype: DataPools
        """
        return self

@dataclass
class StreamDataPools(DataPools):
    """
    StreamDataPools(stream)
    | **Description**
    |   A ``DataPools`` specifically for streams.

    :param stream: The stream to be pooled
    :type stream: :doc:`QueriedDataPool </core/data/queried_data_pool>`
    """
    stream: QueriedDataPool = init()

    def trigger_subscriber(self):
        """
        trigger_subscriber(self) -> None
        | **Description**
        |   Updates its own available data stream.
        """
        super().trigger_subscriber()
        self.stream.update()

@dataclass
class ResultDataPools(DataPools):
    """
    ResultDataPools(result) 
    | **Description**
    |   A ``DataPools`` specifically for results.

    :param result: The results to be pooled
    :type result: :doc:`QueriedDataPool </core/data/queried_data_pool>`
    """
    result: QueriedDataPool = init()

    def trigger_subscriber(self):
        """
        trigger_subscriber(self) -> None
        | **Description**
        |   Updates its own available data.
        """
        super().trigger_subscriber()
        self.result.update()


@dataclass
class ProcessDataPools(DataPools):
    """
    ProcessDataPools(process)
    | **Description**
    |   A ``DataPools`` specifically for results.

    :param process: The process to be pooled
    :type process: :doc:`QueriedDataPool </core/data/queried_data_pool>`
    """
    process: QueriedDataPool = init()

    def trigger_subscriber(self):
        """
        trigger_subscriber(self) -> None
        | **Description**
        |   Updates its own available data.
        """
        super().trigger_subscriber()
        self.process.update()

@dataclass
class PRDataPools(ResultDataPools, ProcessDataPools):
    """
    PRDataPools()
    | **Description**
    |   A ``DataPools`` specifically for process results.
    """
    pass

@dataclass
class SPRDataPools(StreamDataPools, PRDataPools):
    """
    SPRDataPools()
    | **Description**
    |   A ``DataPools`` specifically for stream process results.
    """
    pass