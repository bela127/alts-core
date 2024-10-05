#Version 1.1 conform as of 05.10.2024
"""
:doc:`Built-In Implementations </module/oracle/augmentation>`
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

from alts.core.oracle.data_source import DataSource
from alts.core.data.constrains import QueryConstrain, ResultConstrain
from alts.core.configuration import init, post_init, NOTSET
from numpy import shape


if TYPE_CHECKING:
    from typing_extensions import Self
    from typing import Tuple
    from nptyping import NDArray, Number, Shape

@dataclass
class Augmentation(DataSource):
    """
    Augmentation(data_source) 
    | **Description**
    |   An Augmentation is a wrapper around a :doc:`Data Source </core/oracle/data_source>` which modifies its in- or outputs depending on the implementation.
    |   One of its uses is to add distortion to a :doc:`Data Source </core/oracle/data_source>`.

    :param query_shape: The expected shape of the queries
    :type query_shape: tuple of ints
    :param result_shape: The expected shape of the results
    :type result_shape: tuple of ints
    """
    data_source: DataSource = init()

    def post_init(self):
        """
        post_init(self) -> None
        | **Description**
        |   Initializes the DataSource.
        """
        super().post_init()
        self.data_source = self.data_source()
        

    @property
    def query_shape(self):
        """
        query_shape(self) -> shape
        | **Description**
        |   Returns the accepted query shape of the :doc:`Data Source </core/oracle/data_source>`.

        :return: Accepted query shape
        :rtype: `Array Shape <https://www.w3schools.com/python/numpy/numpy_array_shape.asp>`_
        """
        return self.data_source.query_shape
    
    @query_shape.setter
    def query_shape(self, value):
        """
        query_shape(self, value) -> None
        | **Description**
        |   Does not allow the query shape to be set.

        :param value: The desired query shape
        :type value: `Array Shape <https://www.w3schools.com/python/numpy/numpy_array_shape.asp>`_
        :raises: AttributeError if query shape is set
        """
        if value is not NOTSET:
            raise AttributeError("Augmentation always uses the query_shape of the data_source")

    @property
    def result_shape(self) -> Tuple[int, ...]:
        """
        result_shape(self) -> shape
        | **Description**
        |   Returns the accepted result shape of the :doc:`Data Source </core/oracle/data_source>`.

        :return: Accepted query shape
        :rtype: `Array Shape <https://www.w3schools.com/python/numpy/numpy_array_shape.asp>`_
        """
        return self.data_source.result_shape
    
    @result_shape.setter
    def result_shape(self, value):
        """
        result_shape(self, value) -> None
        | **Description**
        |   Does not allow the result shape to be set.

        :param value: The desired result shape
        :type value: `Array Shape <https://www.w3schools.com/python/numpy/numpy_array_shape.asp>`_
        :raises: AttributeError if result shape is set
        """
        if value is not NOTSET:
            raise AttributeError("Augmentation always uses the result_shape of the data_source")


    def query(self, queries: NDArray[ Shape["query_nr, ... query_dim"], Number]) -> Tuple[NDArray[Shape["query_nr, ... query_dim"], Number], NDArray[Shape["query_nr, ... result_dim"], Number]]: # type: ignore
        """
        query(self, queries) -> data_points
        | **Description**
        |   Modifies the query before passing it on to :func:`DataSource.query()`.

        :param queries: Requested Query
        :type queries: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :return: Processed Query, Result 
        :rtype: A tuple of two `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_  
        """
        return self.data_source.query(queries)

    def query_constrain(self) -> QueryConstrain:
        """
        query_constrain(self) -> QueryConstrain
        | **Description**
        |   Returns its own query constraints. 

        :return: Constraints around queries
        :rtype: QueryConstrain
        """
        return self.data_source.query_constrain()

    def result_constrain(self) -> ResultConstrain:
        """
        result_constrain(self) -> ResultConstrain
        | **Description**
        |   Returns its own result constraints. 

        :return: Constraints around results
        :rtype: ResultConstrain
        """
        return self.data_source.result_constrain()
    
    @property
    def exhausted(self) -> bool:
        """
        exhausted(self) -> bool
        | **Description**
        |   See :func:`DataSource.exhausted()`.

        :return: Whether the augmented ``DataSource`` has been exhausted
        :rtype: ``boolean``
        """
        return self.data_source.exhausted