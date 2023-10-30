from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass, field

from alts.core.query.queryable import Queryable
from alts.core.data.constrains import QueryConstrain, ResultConstrain
from alts.core.configuration import init, Configurable

import numpy as np

if TYPE_CHECKING:
    from typing import Tuple, List
    from nptyping import NDArray, Shape, Number

@dataclass
class DataSource(Configurable, Queryable):

    query_shape: Tuple[int,...] = init()
    result_shape: Tuple[int,...] = init()

    def query(self, queries: NDArray[ Shape["query_nr, ... query_dim"], Number]) -> Tuple[NDArray[Shape["query_nr, ... query_dim"], Number], NDArray[Shape["query_nr, ... result_dim"], Number]]:
        raise NotImplementedError
 
    def query_constrain(self) -> QueryConstrain:
        query_ranges = np.asarray(tuple((np.NINF, np.Inf) for i in range(self.query_shape[0])))
        return QueryConstrain(count=None, shape=self.query_shape, ranges=query_ranges)
    
    def result_constrain(self) -> ResultConstrain:
        return ResultConstrain(shape = self.result_shape)
    
    @property
    def exhausted(self):
        return False

@dataclass
class TimeDataSource(DataSource):

    query_shape: Tuple[int,...] = (1,)

    def query(self, times: NDArray[Shape["time_step_nr, [time]"], Number]) -> Tuple[NDArray[Shape["time_step_nr, [time]"], Number], NDArray[Shape["time_step_nr, ... var_shape"], Number]]:
        raise NotImplementedError()
    
    def query_constrain(self) -> QueryConstrain:
        query_ranges = np.asarray(((0.0, np.Inf),))
        return QueryConstrain(count=None, shape=self.query_shape, ranges=query_ranges)

@dataclass
class TimeDataSourceWraper(TimeDataSource):

    query_shape: Tuple[int,...] = (1,)
    data_source: DataSource = init()

    def query(self, times: NDArray[Shape["time_step_nr, [time]"], Number]) -> Tuple[NDArray[Shape["time_step_nr, [time]"], Number], NDArray[Shape["time_step_nr, ... var_shape"], Number]]:
        return self.data_source.query(times)
    
    def query_constrain(self) -> QueryConstrain:
        qc = self.data_source.query_constrain()
        query_ranges = np.asarray(((0.0, qc.ranges[0,1]),))
        return QueryConstrain(count=None, shape=self.query_shape, ranges=query_ranges)