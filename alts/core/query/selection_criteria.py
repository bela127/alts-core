from __future__ import annotations
from abc import abstractmethod, abstractproperty
from typing import TYPE_CHECKING
from alts.core.data.data_pool import DataPool


from alts.core.experiment_module import ExperimentModule
from alts.core.data.constrains import ResultConstrain
from alts.core.queryable import Queryable

if TYPE_CHECKING:
    from typing import Tuple
    from nptyping import NDArray, Shape, Number
    



class SelectionCriteria(ExperimentModule, Queryable):

    @abstractmethod
    def query(self, queries: NDArray[Shape["query_nr, ... query_shape"], Number]) -> Tuple[NDArray[Shape["query_nr, ... query_shape"], Number], NDArray[Shape["query_nr, [score]"], Number]]:
        raise NotImplementedError
    
    @property
    def result_constrain(self) -> ResultConstrain:
        return ResultConstrain((self.query_constrain.shape[0], 1))
