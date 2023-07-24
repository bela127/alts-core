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

    from alts.core.query.query_pool import QueryPool
    from alts.core.data.data_pool import DataPool

class Queryable(Configurable, Constrained):

    @abstractmethod
    def query(self, queries: NDArray[Shape["query_nr, ... query_shape"], Number]) -> Tuple[NDArray[Shape["query_nr, ... query_shape"], Number], NDArray[Shape["query_nr, ... result_shape"], Number]]:
        raise NotImplementedError


class QueryHandler(Protocol):

    def __call__(self, queries: NDArray[Shape["query_nr, ... query_shape"], Number]) -> Tuple[NDArray[Shape["query_nr, ... query_shape"], Number], NDArray[Shape["query_nr, ... result_shape"], Number]]:
        ...

class QueryableWrapper(Queryable):
    _query_handler: QueryHandler
    _query_constrain: QueryConstrainedGetter
    _result_constrain: ResultConstrainGetter

    def query(self, queries: NDArray[Shape["query_nr, ... query_shape"], Number]) -> Tuple[NDArray[Shape["query_nr, ... query_shape"], Number], NDArray[Shape["query_nr, ... result_shape"], Number]]:
        return self._query_handler(queries)

    def query_constrain(self) -> QueryConstrain:
        return self._query_constrain()

    def result_constrain(self) -> ResultConstrain:
        return self._result_constrain()

    def __call__(self, queryable: Required[Queryable] = None, **kwargs) -> Self:
        obj = super().__call__(**kwargs)
        queryable = is_set(queryable)
        obj._query_handler = queryable.query
        obj._query_constrain = queryable.query_constrain
        obj._result_constrain = queryable.result_constrain
        return obj