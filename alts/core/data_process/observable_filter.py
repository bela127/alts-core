from __future__ import annotations
from typing import TYPE_CHECKING

from abc import abstractmethod
from dataclasses import dataclass, field

from alts.core.configuration import Configurable, Required, is_set, post_init
from alts.core.data.constrains import Constrained, QueryConstrainedGetter, ResultConstrainGetter,QueryConstrain, ResultConstrain

if TYPE_CHECKING:
    from typing_extensions import Self
    from nptyping import NDArray, Shape, Number
    from typing import Tuple

@dataclass
class ObservableFilter(Configurable, Constrained):
    _query_constrain: QueryConstrainedGetter = post_init()
    _result_constrain: ResultConstrainGetter = post_init()

    def filter(self, data_points: Tuple[NDArray[Shape["input_nr, ... input_dim"], Number], NDArray[Shape["input_nr, ... result_dim"], Number]]) -> Tuple[NDArray[Shape["input_nr, ... input_dim"], Number], NDArray[Shape["query_nr, ... filtered_result_dim"], Number]]:
        return data_points

    def query_constrain(self) -> QueryConstrain:
        return self._query_constrain()
    
    def result_constrain(self) -> ResultConstrain:
        return self._result_constrain()

    def __call__(self, constrained: Required[Constrained] = None, **kwargs) -> Self:
        obj = super().__call__(**kwargs)
        obj._query_constrain = is_set(constrained).query_constrain
        obj._result_constrain = is_set(constrained).result_constrain
        return obj
