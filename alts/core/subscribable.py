from __future__ import annotations
from typing import TYPE_CHECKING

from alts.core.configuration import Configurable

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
                callable()
            except TypeError as e:
                raise TypeError(f"The subscriber '{subscriber.__class__}' should implement a callable {str(callable)} with an 'subscription' argument. Results in {str(e)}") from e
