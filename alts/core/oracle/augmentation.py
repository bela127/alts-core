from __future__ import annotations
from typing import TYPE_CHECKING

from alts.core.configuration import Configurable

if TYPE_CHECKING:
    from typing import Tuple, List, Union
    from nptyping import NDArray, Number, Shape


class Augmentation(Configurable):
    def apply(self, data_point: Tuple[NDArray[Shape["query_nr, ... query_dim"], Number], NDArray[Shape["query_nr, ... result_dim"], Number]]) -> Tuple[NDArray[Shape["query_nr, ... query_dim"], Number], NDArray[Shape["query_nr, ... result_dim"], Number]]:
        return data_point

class NoAugmentation(Augmentation):
    ...