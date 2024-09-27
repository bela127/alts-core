#Fully documented as of 27.09.2024
from __future__ import annotations
from typing import TYPE_CHECKING, Any

from dataclasses import dataclass
from typing_extensions import Self
from alts.core.data.queried_data_pool import QueriedDataPool
from alts.core.configuration import Configurable, is_set, init, post_init, pre_init

class DataPools(Configurable):
    """
    | **Description**
    |   A ``DataPools`` stores all queries and results that have been supplied to it.
    """
    def trigger_subscriber(self):
        """
        | **Description**
        |   Updates its own available data.
        """
        pass

    def __call__(self, *args: Any, **kwds: Any) -> Self:
        """
        | **Description**
        |   Returns a new instance of itself. 

        :param any: Any parameters are being accepted but ignored
        :type any: Any
        :return: An instance of this object
        :rtype: DataPools
        """
        return self

@dataclass
class StreamDataPools(DataPools):
    """
    | **Description**
    |   A ``DataPools`` specifically for streams.
    """
    stream: QueriedDataPool = init()

    def trigger_subscriber(self):
        """
        | **Description**
        |   Updates its own available data stream.
        """
        super().trigger_subscriber()
        self.stream.update()

@dataclass
class ResultDataPools(DataPools):
    """
    | **Description**
    |   A ``DataPools`` specifically for results.
    """
    result: QueriedDataPool = init()

    def trigger_subscriber(self):
        """
        | **Description**
        |   Updates its own available data.
        """
        super().trigger_subscriber()
        self.result.update()


@dataclass
class ProcessDataPools(DataPools):
    """
    | **Description**
    |   A ``DataPools`` specifically for results.
    """
    process: QueriedDataPool = init()

    def trigger_subscriber(self):
        """
        | **Description**
        |   Updates its own available data.
        """
        super().trigger_subscriber()
        self.process.update()

@dataclass
class PRDataPools(ResultDataPools, ProcessDataPools):
    """
    | **Description**
    |   A ``DataPools`` specifically for process results.
    """
    pass

@dataclass
class SPRDataPools(StreamDataPools, PRDataPools):
    """
    | **Description**
    |   A ``DataPools`` specifically for stream process results.
    """
    pass