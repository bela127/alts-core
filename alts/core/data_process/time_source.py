#Fully documented as of 27.09.2024
"""
:doc:`Built-In Implementations </modules/oracle/query_queue>`
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from abc import abstractmethod


from alts.core.configuration import Configurable
from alts.core.data.constrains import ResultConstrained, ResultConstrain
from alts.core.subscribable import Publisher


if TYPE_CHECKING:
    from nptyping import NDArray, Shape, Number

class TimeSource(Publisher, ResultConstrained):
    """
    | **Description**
    |   A TimeSource provides a custom time module for the :doc:`Process </core/data_process/process>` to use.
    """
    time_step: float = 1

    def step(self, iteration: int) -> NDArray[Shape["time_step_nr, [time]"], Number]: # type: ignore
        """
        | **Description**
        |   Advances time by ``iteration`` steps.

        :param iteration: Amount of steps to advance by
        :type iteration: int
        """
        self.update()
    
    @property
    def time(self)-> float:
        """
        | **Description**
        |   Returns its current time.
        |   Not implemented in abstract class.
        """
        raise NotImplementedError()

    def result_constrain(self) -> ResultConstrain:
        """
        | **Description**
        |   Returns its time constraints.

        :return: Time constraints
        :rtype: :doc:`ResultConstrain </core/data/constrains>` 
        """
        return ResultConstrain(shape=(1,))
    
    @time.setter
    def time(self, time):
        """
        | **Description**
        |   Modifies its current time with the given value.
        |   Not implemented in abstract class.

        :param time: Given value
        :type time: *abstract*
        """
        raise NotImplementedError()