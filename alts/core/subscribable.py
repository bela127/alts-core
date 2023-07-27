from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass
from abc import abstractmethod

from alts.core.configuration import Configurable, pre_init

if TYPE_CHECKING:
    from typing import List, Tuple, Callable, Optional
    from alts.core.subscriber import Subscriber

class Subscribable():
    @abstractmethod
    def subscribe(self, subscriber: Subscriber, callable: Optional[Callable[[Subscribable],None]] = None) -> None:
        raise NotImplementedError()

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError()

class Publisher(Configurable, Subscribable):

    def __init__(self):
        super().init(Publisher)
        self.__subscriber: List[Tuple[Subscriber,Callable[[Subscribable],None]]] = []
        
    def subscribe(self, subscriber: Subscriber, callable: Optional[Callable[[Subscribable],None]] = None):
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

class DelayedPublisher(Publisher):
    __new_data: bool = False

    def request_update(self):
        self.__new_data = True

    def update(self):
        if self.__new_data:
            self.__new_data = False
            return super().update()
