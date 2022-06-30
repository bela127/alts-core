from __future__ import annotations
from abc import abstractmethod
from typing import TYPE_CHECKING

from alts.core.experiment_module import ExperimentModule
from alts.core.experiment_modules import ExperimentModules


if TYPE_CHECKING:
    from typing import Tuple
    from typing_extensions import Self #type: ignore
    from nptyping import NDArray, Number, Shape



class DataSubscriber(ExperimentModule):

    @abstractmethod
    def update(self):
        raise NotImplementedError

    def __call__(self, exp_modules: ExperimentModules = None, **kwargs) -> Self:
        obj = super().__call__(exp_modules, **kwargs)
    
        if isinstance(exp_modules, ExperimentModules):
            exp_modules.queried_data_pool.subscribe(obj)

        return obj
