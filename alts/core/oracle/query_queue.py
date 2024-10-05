#Version 1.1 conform as of 05.10.2024
"""
:doc:`Built-In Implementations </modules/oracle/query_queue>`
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import numpy as np

from alts.core.configuration import Configurable, Required, is_set, pre_init, post_init, init
from alts.core.data.constrains import QueryConstrained
from alts.core.subscribable import DelayedPublisher

if TYPE_CHECKING:
    from typing_extensions import Self
    from nptyping import NDArray, Shape, Number
    from typing import  Tuple
    from alts.core.data.constrains import QueryConstrainedGetter, QueryConstrain

@dataclass
class QueryQueue(DelayedPublisher, QueryConstrained):
    """
    QueryQueue()
    | **Description**
    |   A buffer for queries in shape of a query. 
    """
    queries: NDArray[Shape["query_nr, ... query_shape"], Number] = post_init() # type: ignore
    _query_constrain: QueryConstrainedGetter = post_init()

    _latest_add: NDArray[Shape[" ... query_shape"], Number] = post_init() # type: ignore
    _latest_pop: NDArray[Shape[" ... query_shape"], Number] = post_init() # type: ignore


    def post_init(self):
        """
        post_init(self) -> None
        | **Description**
        |   Initialites an empty query queue.
        """
        super().post_init()
        self.queries = np.empty((0, *self.query_constrain().shape))

    def add(self, queries: NDArray[Shape["query_nr, ... query_shape"], Number]): # type: ignore
        """
        add(self, queries) -> None
        | **Description**
        |   Adds the queries to the queue.

        :param queries: The queries to be added to the queue
        :type queries: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        self.queries = np.concatenate((self.queries, queries))
        self._latest_add = queries[-1:]
        self.request_update()
    
    def pop(self, query_nr = 1) -> NDArray[Shape["query_nr, ... query_shape"], Number]: # type: ignore
        """
        pop(self, query_nr) -> queries
        | **Description**
        |   Pops all queries up to the given query_nr.

        :param query_nr: How many queries to pop (default = 1).
        :type query_nr: int
        :return: Array of popped queries
        :rtype: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        poped = self.queries[:query_nr,...]
        self.queries = self.queries[query_nr:,...]
        self._latest_pop = poped
        return poped

    @property
    def last(self)-> NDArray[Shape["1, ... query_shape"], Number]: # type: ignore
        """
        last(self) -> query
        | **Description**
        |   Returns the last query of the queue.

        :return: Last queue query
        :rtype: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        return self.queries[-1:,...]
    
    @property
    def first(self)-> NDArray[Shape["1, ... query_shape"], Number]: # type: ignore
        """
        first(self) -> query
        | **Description**
        |   Returns the first query of the queue.

        :return: First queue query
        :rtype: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        return self.queries[:1,...]

    @property
    def latest_add(self)-> NDArray[Shape["1, ... query_shape"], Number]: # type: ignore
        """
        latest_add(self) -> query
        | **Description**
        |   Returns the last added query.

        :return: Last added query
        :rtype: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        return self._latest_add
    
    @property
    def latest_pop(self)-> NDArray[Shape["1, ... query_shape"], Number]: # type: ignore
        """
        latest_pop(self) -> query
        | **Description**
        |   Returns the last popped query.

        :return: Last popped query
        :rtype: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        return self._latest_pop

    @property
    def empty(self):
        """
        empty(self) -> None
        | **Description**
        |   Returns ``True`` only if the queue is empty.

        :return: Is the queue empty?
        :rtype: bool
        """
        return self.queries.shape[0] == 0
    
    @property
    def count(self) -> int:
        """
        count(self) -> int
        | **Description**
        |   Returns the size of the queue.

        :return: Size of queue
        :rtype: int
        """
        return self.queries.shape[0]

    def query_constrain(self) -> QueryConstrain:
        """
        query_constrain(self) -> QueryConstrain
        | **Description**
        |   Returns its query constraints.

        :return: Own query constraints
        :rtype: :doc:`QueryConstrain </core/data/constrains>`
        """
        return self._query_constrain()
       

    def __call__(self, query_constrain: Required[QueryConstrainedGetter], **kwargs) -> Self:
        """
        __call__(self, query_constrain, **kwargs) -> Self
        | **Description**
        |   Returns a QueryQueue with the given query constraint.

        :param query_constrain: Constraints of the queries the queue holds.
        :type query_constrains: :doc:`QueryConstrain </core/data/constrains>`
        :return: Configured QueryQueue
        :rtype: QueryQueue
        """
        obj =  super().__call__(**kwargs)
        obj._query_constrain = is_set(query_constrain)
        return obj
