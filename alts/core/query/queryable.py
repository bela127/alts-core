from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from abc import abstractmethod, abstractproperty


from alts.core.configuration import Configurable, Required, is_set
from alts.core.data.constrains import Constrained, QueryConstrain, ResultConstrain, QueryConstrainedGetter, ResultConstrainGetter


if TYPE_CHECKING:
    from typing_extensions import Self
    from typing import Tuple, List, Protocol
    from nptyping import NDArray, Shape, Number

class Queryable(Constrained):

    @abstractmethod
    def query(self, queries: NDArray[Shape["query_nr, ... query_shape"], Number]) -> Tuple[NDArray[Shape["query_nr, ... query_shape"], Number], NDArray[Shape["query_nr, ... result_shape"], Number]]:
        raise NotImplementedError()