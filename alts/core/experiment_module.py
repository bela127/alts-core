from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from alts.core.configuration import Configurable, Required, is_set, post_init

if TYPE_CHECKING:
    from typing_extensions import Self #type: ignore
    from alts.core.experiment_modules import ExperimentModules

@dataclass
class ExperimentModule(Configurable):
    exp_modules: ExperimentModules = post_init()

    def __call__(self, exp_modules: Required[ExperimentModules] = None, **kwargs) -> Self:
        obj = super().__call__( **kwargs)
        obj.exp_modules = is_set(exp_modules)
        return obj
    
    @property
    def data_pools(self):
        return self.exp_modules.data_pools