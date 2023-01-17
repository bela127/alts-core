from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import List, Tuple, Callable, Optional

    from alts.core.subscriber import Subscriber

class Subscribable():

    def __init__(self):
        super().__init__()
        self.__subscriber: List[Tuple[Subscriber,Callable[[],None]]] = []
        
    def subscribe(self, subscriber: Subscriber, callable: Optional[Callable[[],None]] = None):
        if callable is None:
            self.__subscriber.append((subscriber, subscriber.update))
        else:
            self.__subscriber.append((subscriber, callable))
    
    def update(self):
        for subscriber, callable in self.__subscriber:
            callable()