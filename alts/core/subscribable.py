#Version 1.1.1 conform as of 16.12.2024
"""
| *alts.core.subscribable*
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass
from abc import abstractmethod

from alts.core.configuration import Configurable, pre_init

if TYPE_CHECKING:
    from typing import List, Tuple, Callable, Optional
    from alts.core.subscriber import Subscriber

class Subscribable():
    """
    Subscribable()
    | **Description**
    |   A Subscribable can have subscribers. When the Subscribable is updated, it calls the given Callable for each subscriber.
    """
    @abstractmethod
    def subscribe(self, subscriber: Subscriber, callable: Optional[Callable[[Subscribable],None]] = None) -> None:
        """
        subscribe(self, subscriber, callable) -> None
        | **Description**
        |   Remembers ``subscriber`` and calls the given ``callable`` if one is given.

        :param subscriber: The new subscriber
        :type subscriber: Subscriber
        :param callable: This gets called when the Subscribable updates (default= None)
        :type callable: Callable
        :raises NotImplementedError: Method is abstract
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self) -> None:
        """
        updae(self) -> None
        | **Description**
        |   Updates all subscribers given their callables.

        :raises NotImplementedError: Method is abstract
        """
        raise NotImplementedError()

class Publisher(Configurable, Subscribable):
    """
    Publisher()
    | **Description**
    |   A Publisher is a simple Subscribable which just calls the subscribers' callables when updated.
    """
    def __init__(self):
        """
        __init__(self) -> None
        | **Description**
        |   Initializes its values to default values.
        """
        super().init(Publisher)
        self.__subscriber: List[Tuple[Subscriber,Callable[[Subscribable],None]]] = []
        
    def subscribe(self, subscriber: Subscriber, callable: Optional[Callable[[Subscribable],None]] = None):
        """
        subscribe(self, subscriber, callable) -> None
        | **Description**
        |   Adds the ``(subscriber, callable)`` tuple to its record.
        |   If no callable is passed, defaults to ``subscriber.update``.

        :param subscriber: The new subscriber
        :type subscriber: Subscriber
        :param callable: Gets called on update (default= ``subscriber.update``)
        :type callable: Callable
        """
        if callable is None:
            self.__subscriber.append((subscriber, subscriber.update)) # type: ignore
        else:
            self.__subscriber.append((subscriber, callable))
    
    def update(self):
        """ 
        update(self) -> None
        | **Description**
        |   Calls the associated callable of each subscriber.

        :raises TypeError: ``callable`` is not a Callable
        """
        for subscriber, callable in self.__subscriber:
            try:
                callable(self)
            except TypeError as e:
                raise TypeError(f"The subscriber '{subscriber.__class__.__name__}' with callable {str(e)}. Provide an 'subscription' argument.") from e

class DelayedPublisher(Publisher):
    """
    DelayedPublisher()
    | **Description**
    |   A DelayedPublisher, as opposed to a Publisher, updates through the ``update()`` method only if it has been requested
        by executing the ``request_update()`` method after the last successful update.   
    """
    __new_data: bool = False

    def request_update(self):
        """
        requeste_update(self) -> None
        | **Description**
        |   Ensures an update on the next ``update()`` call.
        """
        self.__new_data = True

    def update(self):
        """
        update(self) -> None
        | **Description**
        |   Updates its subscribers only there has been a ``request_update()`` since the last update.
        """
        if self.__new_data:
            self.__new_data = False
            return super().update()
