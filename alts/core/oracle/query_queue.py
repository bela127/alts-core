#TODO D
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
    | **Description**
    |   A buffer for queries in shape of a query. 
    """
    queries: NDArray[Shape["query_nr, ... query_shape"], Number] = post_init() # type: ignore
    _query_constrain: QueryConstrainedGetter = post_init()

    _latest_add: NDArray[Shape[" ... query_shape"], Number] = post_init() # type: ignore
    _latest_pop: NDArray[Shape[" ... query_shape"], Number] = post_init() # type: ignore


    def post_init(self):
        """
        | **Description**
        |   Initialites an empty query queue.
        """
        super().post_init()
        self.queries = np.empty((0, *self.query_constrain().shape))

    def add(self, queries: NDArray[Shape["query_nr, ... query_shape"], Number]): # type: ignore
        """
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
        | **Description**
        |   Pops all queries up to the given query_nr (default is 1).

        :param query_nr: How many queries to pop.
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
        | **Description**
        |   Returns the last query of the queue.

        :return: Last queue query
        :rtype: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        return self.queries[-1:,...]
    
    @property
    def first(self)-> NDArray[Shape["1, ... query_shape"], Number]: # type: ignore
        """
        | **Description**
        |   Returns the first query of the queue.

        :return: First queue query
        :rtype: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        return self.queries[:1,...]

    @property
    def latest_add(self)-> NDArray[Shape["1, ... query_shape"], Number]: # type: ignore
        """
        | **Description**
        |   Returns the last added query.

        :return: Last added query
        :rtype: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        return self._latest_add
    
    @property
    def latest_pop(self)-> NDArray[Shape["1, ... query_shape"], Number]: # type: ignore
        """
        | **Description**
        |   Returns the last popped query.

        :return: Last popped query
        :rtype: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        """
        return self._latest_pop

    @property
    def empty(self):
        """
        | **Description**
        |   Returns ``True`` only if the queue is empty.

        :return: Is the queue empty?
        :rtype: bool
        """
        return self.queries.shape[0] == 0
    
    @property
    def count(self):
        """
        | **Description**
        |   Returns the size of the queue.

        :return: Size of queue
        :rtype: int
        """
        return self.queries.shape[0]

    def query_constrain(self) -> QueryConstrain:
        """
        | **Description**
        |   Returns its query constraints.

        :return: Own query constraints
        :rtype: :doc:`QueryConstrain </core/data/constrains>`
        """
        return self._query_constrain()
       

    def __call__(self, query_constrain: Required[QueryConstrainedGetter], **kwargs) -> Self:
        obj =  super().__call__(**kwargs)
        obj._query_constrain = is_set(query_constrain)
        return obj
