#Fully documented as of 30.06.2024
from __future__ import annotations
from typing import TYPE_CHECKING, Self
from alts.core.data.data_sampler import DataSampler

from alts.core.configuration import Configurable, post_init, Required, is_set

from alts.core.data.constrains import QueryConstrain, QueryConstrained

if TYPE_CHECKING:
    from typing import Tuple, List, Dict
    from nptyping import NDArray, Number, Shape

class InterpolationStrategy(Configurable, QueryConstrained):
    """
    | **Description**
    |   An ``InterpolatingStrategy`` is an **ambivalent** source of data depending on the :doc:`DataSampler <core/data/data_sampler>` it interpolates within.
    |   This is a base class not intended for direct use.

    :param data_sampler: A sample of the data which contains the to be interpolated data points
    :type data_sampler: :doc:`DataSampler <core/data/data_sampler>`
    """
    data_sampler: DataSampler = post_init()

    def interpolate(self, data_points: Tuple[NDArray[Shape["query_nr, sample_nr, ... query_dim"], Number], NDArray[Shape["query_nr, sample_nr, ... result_dim"], Number]]) -> Tuple[NDArray[Shape["query_nr, ... query_dim"], Number], NDArray[Shape["query_nr, ... result_dim"], Number]]: # type: ignore
        """
        | **Description**
        |   Interpolates a twople of data points and returns the interpolated twople.
        |   This implementation of ``interpolate`` returns the twople as is. If this is the result you wish to achieve, please use :class:`NoInterpolation` instead.

        :param data_points: A twople of data_points to be interpolated
        :type data_points: Tuple(`NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_, `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_)
        :return: The interpolated twople
        :rtype: Tuple(`NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_, `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_)
        """
        return data_points

    def query_constrain(self) -> QueryConstrain:
        """
        | **Description**
        |   See :func:`DataSource.query()`

        :param queries: Requested Query
        :type queries: `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_
        :return: Processed Query, Result 
        :rtype: A tuple of two `NDArray <https://numpy.org/doc/stable/reference/arrays.ndarray.html>`_  
        """
        return self.data_sampler.query_constrain()

    def __call__(self, data_sampler: Required[DataSampler] = None, **kwargs) -> Self:
        """
        | **Description**
        |   Returns an ``InterpolatingDataSource`` constrained to the given :doc:`DataSampler <core/data/data_sampler>`.

        :param data_sampler: A sample of the data which contains the to-be interpolated data points
        :type data_sampler: :doc:`DataSampler <core/data/data_sampler>`
        :return: Instance of ``InterpolatingDataSource`` constrained to ``data_sampler``
        :rtype: ``InterpolatingDataSource``
        """
        obj = super().__call__(**kwargs)
        obj.data_sampler = is_set(data_sampler)
        return obj

class NoInterpolation(InterpolationStrategy):
    """
    | **Description**
    |   A ``NoInterpolation`` is an interpolator that does nothing to the given data. 

    :param data_sampler: A sample of the data which contains the to-be interpolated data points
    :type data_sampler: :doc:`DataSampler <core/data/data_sampler>`
    """
    ...
