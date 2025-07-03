#Version 1.1.1 conform as of 18.12.2024
"""
| *alts.core.experiment_module*
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from alts.core.configuration import Configurable, Required, is_set, post_init

if TYPE_CHECKING:
    from typing_extensions import Self #type: ignore
    from alts.core.experiment_modules import ExperimentModules
    from alts.core.data.data_pools import DataPools
    from alts.core.oracle.oracles import Oracles

class ExperimentModule(Configurable):
    """
    ExperimentModule()
    | **Description**
    |   An ExperimentModule is any module which is configurable/swappable in a blueprint.
    |   Each ExperimentModule has access to the experiment's oracle, data pool and all other experiment modules.
    """
    exp_modules: ExperimentModules = post_init()

    def __call__(self, exp_modules: Required[ExperimentModules] = None, **kwargs) -> Self:
        """
        __call__(self, exp_modules, **kwargs) -> ExperimentModule
        | **Description**
        |   Creates a new instance of itself with the given configuration.

        :param exp_modules: A collection of already configured and setup experiment modules
        :type exp_modules: ExperimentModules
        :param **kwargs: Keyword arguments for configuration
        :type **kwargs: Any
        :return: Newly configured object
        :rtype: ExperimentModule
        """
        obj = super().__call__( **kwargs)
        obj.exp_modules = is_set(exp_modules, "ExperimentModule.exp_modules")
        return obj
    
    @property
    def data_pools(self) -> DataPools:
        """
        data_pools(self) -> DataPools
        | **Description**
        |   Returns the experiment's data pools.

        :return: The experiment's data pools
        :rtype: DataPools
        """
        return self.exp_modules.data_pools
    
    @property
    def oracles(self) -> Oracles:
        """
        oracles(self) -> Oracles
        | **Description**
        |   Returns the experiment's oracles.

        :return: The experiment's oracles
        :rtype: Oracles
        """
        return self.exp_modules.oracles