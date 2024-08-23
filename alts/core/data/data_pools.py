#TODO D
from __future__ import annotations
from typing import TYPE_CHECKING, Any

from dataclasses import dataclass
from typing_extensions import Self
from alts.core.data.queried_data_pool import QueriedDataPool
from alts.core.configuration import Configurable, is_set, init, post_init, pre_init

class DataPools(Configurable):
    """
    | **Description**
    |   A ``DataPools`` stores all queries and results that have been supplied to or requested by the trained model.
    """
    def trigger_subscriber(self):
        """
        | **Description**
        |   Updates its own available data.

        :return: No return
        :rtype: None
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
    #QUESTION ASK DIFFERENCE
    stream: QueriedDataPool = init()

    def trigger_subscriber(self):
        super().trigger_subscriber()
        self.stream.update()

@dataclass
class ResultDataPools(DataPools):
    result: QueriedDataPool = init()

    def trigger_subscriber(self):
        super().trigger_subscriber()
        self.result.update()


@dataclass
class ProcessDataPools(DataPools):
    process: QueriedDataPool = init()

    def trigger_subscriber(self):
        super().trigger_subscriber()
        self.process.update()

@dataclass
class PRDataPools(ResultDataPools, ProcessDataPools):
    #ProcessResult
    pass

@dataclass
class SPRDataPools(StreamDataPools, PRDataPools):
    #StreamProcessResult
    pass