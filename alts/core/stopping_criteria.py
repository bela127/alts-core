#Version 1.1 conform as of 05.10.2024
"""
:doc:`Built-In Implementations </modules/stopping_criteria>`
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field

from alts.core.configuration import Configurable, Required, is_set, post_init

if TYPE_CHECKING:
    from typing_extensions import Self
    from typing import Tuple, List
    from alts.core.experiment import Experiment

@dataclass
class StoppingCriteria(Configurable):
    """
    StoppingCriteria(exp)
    | **Description**
    |   Determines when the experiment has reached its goal.

    :param exp: The experiment to monitor
    :type exp: :doc:`Experiment </core/experiment>`
    """
    exp: Experiment = post_init()

    @property
    def next(self) -> bool:
        """
        next(self) -> bool
        | **Description**
        |   Determines whether the experiment should continue into another step.
        |   Currently always returns True.

        :return: Should the experiment continue? (True)
        :rtype: bool
        """
        return True
    
    def __call__(self, exp: Required[Experiment] = None, **kwargs) -> Self:
        """
        __call__(self, exp, **kwargs) -> Self
        | **Description**
        |   Returns a StoppingCriteria configured with the exp-argument.

        :param exp: The experiment to be checked
        :type exp: :doc:`Experiment </core/experiment>`
        :return: Configured StoppingCriteria
        :rtype: StoppingCriteria
        """
        obj = super().__call__( **kwargs)
        obj.exp = is_set(exp)
        return obj
    
