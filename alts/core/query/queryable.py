#Fully documented as of 25.09.2024
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
    """
    | **Description**
    |   A Queryable module can be queried for results.
    """
    @abstractmethod
    def query(self, queries: NDArray[Shape["query_nr, ... query_shape"], Number]) -> Tuple[NDArray[Shape["query_nr, ... query_shape"], Number], NDArray[Shape["query_nr, ... result_shape"], Number]]: # type: ignore
        """
        | **Description**
        |   For a list of queries it returns a list of queries with associated results.

        :param queries: A list of queries
        :type queries: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :return: A tuple of queries and their results
        :rtype: Tuple[`NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_,`NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_]
        """
        raise NotImplementedError()