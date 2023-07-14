from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass

from alts.core.configuration import Configurable, pre_init

if TYPE_CHECKING:
    from typing import List, Tuple, Callable, Optional
    from alts.core.subscriber import Subscriber

class Subscribable(Configurable):

    def __init__(self):
        self.__post_init__()

    def __post_init__(self):
        super().__post_init__()
        self.__subscriber: List[Tuple[Subscriber,Callable[[],None]]] = []
        
    def subscribe(self, subscriber: Subscriber, callable: Optional[Callable[[],None]] = None):
        if callable is None:
            self.__subscriber.append((subscriber, subscriber.update))
        else:
            self.__subscriber.append((subscriber, callable))
    
    def update(self):
        for subscriber, callable in self.__subscriber:
            try:
                callable(self)
            except TypeError as e:
                raise TypeError(f"The subscriber '{subscriber.__class__.__name__}' with callable {str(e)}. Provide an 'subscription' argument.") from e

@dataclass
class DelayedSubscribable(Subscribable):
    _new_data: bool = pre_init(default=False)

    def request_update(self):
        self._new_data = True

    def update(self):
        if self._new_data:
            self._new_data = False
            return super().update()
