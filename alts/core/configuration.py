#Version 1.1.1 conform as of 18.12.2024
"""
| *alts.core.configuration*
"""
from __future__ import annotations
from typing import TYPE_CHECKING, TypeVar, Generic, Union
from dataclasses import field, is_dataclass
from functools import wraps

import types

if TYPE_CHECKING:
    from typing import Any, Type, Dict, Tuple
    from typing_extensions import Self #type: ignore



class InitError(AttributeError):
    """
    InitError()
    | **Description**
    |   Is raised when an object hasn't been initialized.
    """
    def __init__(self, *args: object) -> None:
        """
        __init__(self, *args) -> None:
        | **Description**
        |   Passes the argument or the default message to AttributeError.

        :param *args: Gets passed onto the AttributeError constructor (default= "Configurable has not been initialized")
        :type *args: Object
        """
        message = "Configurable has not been initialized"
        if args: super().__init__(*args)
        else: super().__init__(message)

class NotSet():
    """
    NotSet()
    | **Description**
    |   If an attribute is set to ``NotSet()`` or ``NOTSET``, then an AttributeError is raised if the attribute is being read. 
    """
    def __repr__(self) -> str:
        """
        __repr__(self) -> str
        | **Description**
        |   The representation of this class is "NOTSET"
        """
        return "NOTSET"
    
    def __getattribute__(self, __name: str) -> Any:
        """
        __getattribute__(self, __name: str) -> Any:
        | **Description**
        |   Tries to get and return the given attribute from the Object class, otherwise throws an AttributeError.

        :param __name: The name of the accessed attribute
        :type __name: str
        :return: The ``__name``-attribute from the Object class
        :rtype: Any
        :raises AttributeError: If the searched attribute does not exist.
        """
        try:
            attr_result = super().__getattribute__(__name)
        except AttributeError as e:
            raise e
        return attr_result

NOTSET = NotSet()

class ConfAttr():
    """
    ConfAttr()
    | **Description**
    |   A configurable attribute may be only initialized at runtime.
    |   Works with the NotSet() class.
    """
    _value = None
    _initialized = True

    def __init__(self, default = NOTSET) -> None:
        """
        __init__(self, default) -> None
        | **Description**
        |   If a default value is given, initializes itself with it. Otherwise it sets itself to be NOTSET.

        :param default: Default value of attribute (default= NOTSET)
        :type default: Any
        """
        if default is NOTSET:
            self._initialized = False
        self._value = default

    def __get__(self, instance, owner):
        """
        __get__(self) -> Any
        | **Description**
        |   Returns its value if it has been initalized, otherwise returns NOTSET

        :return: Its own value (or NOTSET if not initialized)
        :rtype: Any
        """
        if self._initialized:
            return self._value
        return NOTSET

    def __set__(self, instance, value):
        """
        __set__(self, value) -> None
        | **Description**
        |   Initializes itself with the given value.

        :param value: Value to initialize with
        :type value: Any
        """
        self._value = value
        self._initialized = True
    
    def __set_name__(self, owner, name: str):
        """
        __set_name__(self, name) -> None
        | **Description**
        |   Sets the attributes name to ``name``.

        :param name: New attribute name
        :type name: str
        """
        self.name = name

T = TypeVar('T')
Required = Union[T, None]

def is_set(param):
    """
    is_set(param) -> param
    | **Description**
    |   Returns ``param`` if it is not None, otherwise raises a ValueError as setting ``param`` is required.

    :param param: The parameter to be tested, whether it is set
    :type param: Any
    :return: param
    :rtype: Any
    :raises valueError: If param is None
    """
    if param is not None:
        return param
    else:
        raise ValueError("set a values for all 'Required' params")

def post_init():
    """
    post_init() -> Any
    | **Description**
    |   An initialisor that is run during the experiment.

    :return: A not set default
    :rtype: Any
    """
    return field(init=False, repr=False)

def pre_init(default: Any = NOTSET, default_factory: Any = NOTSET) -> Any:
    """
    pre_init(default, default_factory) -> Any
    | **Description**
    |   An initialisor that is run before the experiment. Sets the defaults of attributes.
    |   Prioritizes ``default_factory`` as default over ``default``.

    :param default: A fixed default value (default= NOTSET)
    :type default: Any
    :param default_factory: A dynamic default factory (default= NOTSET)
    :type default_factory: Any
    :return: A field(init=False, repr=False)
    :rtype: Any
    :raises ValueError: If neither default nor default_factory are set
    """
    if default is NOTSET and not isinstance(default_factory, NotSet):
        return field(init=False, repr=False, default_factory=default_factory)
    if default is not NOTSET and default_factory is NOTSET:
        return field(init=False, repr=False, default=default)
    raise ValueError("one of the arguments 'default' or 'default_factory' needs to be set")

def init(default: Any = NOTSET, default_factory: Any = NOTSET) -> Any:
    """
    init(default, default_factory) -> Any
    | **Description**
    |   An initialisor that is at the start of the experiment.
    |   Prioritizes ``default_factory`` as default over ``default``.

    :param default: A fixed default value (default= NOTSET)
    :type default: Any
    :param default_factory: A dynamic default factory (default= NOTSET)
    :type default_factory: Any
    :return: A static/dynamic default if one is given, otherwise becomes a configurable attribute ``ConfAttr()``
    :rtype: Any
    """
    if default is NOTSET and not isinstance(default_factory, NotSet):
        return field(default_factory=default_factory)
    if default is not NOTSET and default_factory is NOTSET:
        return field(default=default)
    return ConfAttr()

class ConfigurableMeta(type):
    """
    ConfigurableMeta()
    | **Description**
    |   A ConfigurableMeta returns a new Configurable of the given type when called.
    """
    def __call__(cls: Type, *args: Any, **kwargs: Any) -> Any:
        """
        __call__(cls, *args, **kwargs) -> Any
        | **Description**
        |   Returns a new Configurable of the given type with the given arguments.

        :param cls: Type of the Configurable
        :type cls: Type
        :param *args: Position arguments for the new Configurable
        :type *args: Any
        :param **kwargs: Keyword arguments for the new Configurable
        :type **kwargs: Any
        :return: The new Configurable
        :rtype: Configurable (of type ``cls``)
        """
        obj: Configurable = cls.__new__(cls, *args, **kwargs)        # type: ignore
        return obj

class ROOT():
    """
    ROOT()
    | **Description**
    |   ROOT defines basic implementations of the __init__, __post_init__, init and post_init methods.
    """
    __post_init_called = False

    def __init__(self) -> None:
        """
        __init__(self) -> None
        | **Description**
        |   Does nothing.
        """
        pass

    def __post_init__(self):
        """
        __post_init__(self) -> None
        | **Description**
        |   Only does anything the first time it is called.
        |   Initializes all non-dataclass objects in method resolution order, then runs post_init().
        """
        if not self.__post_init_called:
            self.__post_init_called = True
            mro = self.__class__.mro()
            for parent in mro[1:]:
                if not is_dataclass(parent):
                    parent.__init__(self)
                    break
            if hasattr(self, 'post_init'):
                self.post_init()

    def post_init(self):
        """
        post_init(self) -> None
        | **Description**
        |   Runs after __post_init__, does nothing here.
        """
        pass

    def init(self, cls):
        """
        init(self, cls) -> None
        | **Description**
        |   Initializes all non-dataclass objects after ``cls`` in method resolution order.

        :param cls: Starting point of initialization.
        :type cls: Type
        """
        mro = self.__class__.mro()
        index = mro.index(cls)
        for parent in mro[index+1:]:
            if not is_dataclass(parent):
                parent.__init__(self)
                break

class Configurable(ROOT, metaclass = ConfigurableMeta):
    """
    Configurable(*args, **kwargs)
    | **Description**
    |   Remembers its parameters and is able to create new instances of itself with the same parameters.

    :param args: Positional arguments for configuration
    :type args: Any
    :param kwargs: Keyword arguments for configuration
    :type kwargs: Any
    """
    __initialized: bool = False
    __cls: Type
    __args: Tuple
    __kwargs: Dict

    def __getnewargs_ex__(self):
        """
        __getnewargs_ex__(self) -> (Tuple, Dict)
        | **Description**
        |   Returns current parameters of the Configurable (args, kwargs). 

        :return: Current parameters (args, kwargs)
        :rtype: (Tuple, Dict)
        """
        return (self.__args, self.__kwargs)

    def __init__(self, *args, **kwargs) -> None:
        """
        __init__(self, *args, **kwargs) -> None
        | **Description**
        |   Initializes itself over ROOT.init(Configurable).

        :param *args: Positionary arguments
        :type *args: Any
        :param **kwargs: Keyword arguments
        :type **kwargs: Any
        :raises TypeError: If any arguments were passed (as they are superfluous here)
        """
        if len(args) != 0 or len(kwargs) != 0:
            raise TypeError(f"__init__ was called with {args}, {kwargs}, no arguments should be left over!")
        super().init(Configurable)

    def __new__(cls: Type[Self], *args, **kwargs) -> Self:
        """
        __new__(cls, *args, **kwargs) -> Self
        | **Description**
        |   Creates a new instance of ``cls`` with the same configuration.
        |   Patches the new instance's __call__ method to initialize itself with the given arguments, if not done so already.

        :param cls: Configurable to be copied
        :type cls: Configurable
        :param *args: Positionary arguments
        :type *args: Any
        :param **kwargs: Keyword arguments
        :type **kwargs: Any
        :return: Copy of cls
        :rtype: Configurable
        """
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
                try:
                    new_obj.__init__(*new_obj.__args, **new_obj.__kwargs)
                except TypeError as e:
                    raise TypeError(f"In {new_obj.__cls.__name__}.__init__ following accrued: {str(e)}") from e
                new_obj.__initialized = True
                return new_obj

            cls.__call__ = __call__

        return obj
    
    def __call__(self, **kwargs) -> Self:
        """
        __call__(self, **kwargs) -> Self
        | **Description**
        |   Returns a new instance of itself with the same configuration.

        :param **kwargs: Keyword arguments are ignored
        :type **kwargs: Any
        :return: New instance of itself with the same configuration.
        :rtype: Configurable
        """
        new_obj = self.__new__(self.__cls, *self.__args, **self.__kwargs) # type: ignore
        return new_obj
