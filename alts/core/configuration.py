from __future__ import annotations
from typing import TYPE_CHECKING, TypeVar, Generic, Union
from dataclasses import field
from functools import wraps

import types

if TYPE_CHECKING:
    from typing import Any, Type, Dict, Tuple
    from typing_extensions import Self #type: ignore



class InitError(AttributeError):

    def __init__(self, *args: object) -> None:
        message = "Configurable has not been initialized"
        if args: super().__init__(*args)
        else: super().__init__(message)

class NotSet():
    def __repr__(self) -> str:
        return "NOTSET"

NOTSET = NotSet()

class ConfAttr():
    _value = None
    _initialized = True

    def __init__(self, default = NOTSET) -> None:
        if default is NOTSET:
            self._initialized = False
        self._value = default

    def __get__(self, instance, owner):
        if self._initialized:
            return self._value
        return NOTSET

    def __set__(self, instance, value):
        self._value = value
        self._initialized = True
    
    def __set_name__(self, owner, name):
        self.name = name

T = TypeVar('T')
Required = Union[T, None]

def is_set(param):
    if param is not None:
        return param
    else:
        raise ValueError("set a values for all 'Required' params")

def post_init():
    return field(init=False, repr=False)

def pre_init(default: Any = NOTSET, default_factory: Any = NOTSET) -> Any:
    if default is NOTSET and not isinstance(default_factory, NotSet):
        return field(init=False, repr=False, default_factory=default_factory)
    if default is not NOTSET and default_factory is NOTSET:
        return field(init=False, repr=False, default=default)
    raise ValueError("one of the arguments 'default' or 'default_factory' needs to be set")

def init(default: Any = NOTSET, default_factory: Any = NOTSET) -> Any:
    if default is NOTSET and not isinstance(default_factory, NotSet):
        return field(default_factory=default_factory)
    if default is not NOTSET and default_factory is NOTSET:
        return field(default=default)
    return ConfAttr()

class ConfigurableMeta(type):

    def __call__(cls: Type, *args: Any, **kwargs: Any) -> Any:
        obj: Configurable = cls.__new__(cls, *args, **kwargs)       
        return obj

class Configurable(metaclass = ConfigurableMeta):
    __initialized: bool = False
    __cls: Type
    __args: Tuple
    __kwargs: Dict

    # def __getattribute__(self, __name: str) -> Any:
    #     initialized = super().__getattribute__("_Configurable__initialized")
    #     exept = ['__reduce_ex__','__reduce__','__getstate__','__class__','__setstate__','__dict__']
    #     if not initialized and not __name in exept:
    #         raise InitError()
    #     else:
    #         attr_result = super().__getattribute__(__name)
    #     return attr_result

    def __getnewargs_ex__(self):
        return (self.__args, self.__kwargs)

    def __init__(self, *args, **kwargs) -> None:
        if len(args) != 0 or len(kwargs) != 0:
            raise TypeError(f"__init__ was called with {args}, {kwargs}, no arguments should be left over!")
        super().__init__()
        # just intercept the __init__ calls so they
        # aren't relayed to `object`

    def __post_init__(self):
        super().__init__()
        # just intercept the __post_init__ calls so they
        # aren't relayed to `object`

    def __new__(cls: Type[Self], *args, **kwargs) -> Self:
        obj: Self = super(Configurable, cls).__new__(cls)
        obj.__cls = cls
        obj.__args = args
        obj.__kwargs = kwargs

        if not hasattr(cls, "_Configurable__patched"):
            cls.__patched = True
            old_call = cls.__call__
            
            @wraps(old_call)
            def __call__(self, **kwargs):
                new_obj = old_call(self, **kwargs)
                new_obj.__init__(*new_obj.__args, **new_obj.__kwargs)
                new_obj.__initialized = True
                return new_obj

            cls.__call__ = __call__

        return obj
    
    def __call__(self, **kwargs) -> Self:
        new_obj = self.__new__(self.__cls, *self.__args, **self.__kwargs)
        return new_obj

