#Version 1.1.1 conform as of 14.12.2024
"""
| *alts.core.experiment*
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alts.core.blueprint import Blueprint
    from nptyping import NDArray, Number, Shape


class Experiment():
    """
    Experiment(blueprint, exp_nr)
    | **Description**
    |   Initializes the configured modules and does dependency injection based on the blueprint, then runs the experiment.

    :param blueprint: Blueprint with configuration
    :type blueprint: Blueprint
    :param exp_nr: The ID of the experminent
    :type exp_nr: int
    """
    exp_nr: int

    def __init__(self, blueprint: Blueprint, exp_nr: int):
        """
        __init__(self, blueprint, exp_nr) -> None
        | **Description**
        |   Loads configuration from the ``blueprint``.

        :param blueprint: Blueprint with configuration
        :type blueprint: Blueprint
        :param exp_nr: The ID of the experminent
        :type exp_nr: int
        """
        self.exp_nr = exp_nr
        self.exp_path = blueprint.exp_path
        self.exp_name = blueprint.exp_name

        self.data_pools = blueprint.data_pools()

        self.oracles = blueprint.oracles()

        self.time_source = blueprint.time_source()

        self.process = blueprint.process(time_source=self.time_source, oracles = self.oracles, data_pools=self.data_pools)

        self.experiment_modules = blueprint.experiment_modules(time_source=self.time_source, data_pools=self.data_pools, oracles=self.oracles)

        self.stopping_criteria = blueprint.stopping_criteria(exp = self) # type: ignore

        self.iteration = 0

    def run(self) -> int:
        """
        run(self) -> int
        | **Description**
        |   Initializes all modules and actually runs the experiment.

        :return: ``exp_nr`` of experiment once finished
        :rtype: int
        """
        self.time_source.step(self.iteration)
        self.process.initialize()
        self.experiment_modules.initialize()

        while True:
            self.oracles.trigger_subscriber()
            self.process.step(self.iteration)

            self.data_pools.trigger_subscriber()
            self.experiment_modules.step(self.iteration)
            self.iteration += 1

            if not self.stopping_criteria.next: break

            self.time_source.step(self.iteration)
            
        return self.exp_nr