cooperative multiple inheritance paradigm:

Cooperative multi-inheritance is a technique for implementing classes that inherit multiple super-classes - typically a main super-class and one or more mixin classes that add additional behaviour.  It makes it easy to add new mixins at a later date to further extend the behavior, without needing to change either the implementation of the class or any existing code that creates an instance of the class.

The technique requires that all the super-class’s `__init__` methods follow the same pattern in the way that they handle unrecognised keyword arguments and use `super()` to invoke their own super-class’s `__init__` methods.

See Raymond Hettinger’s [Python’s super() considered super!](http://rhettinger.wordpress.com/2011/05/26/super-considered-super/) blog post for some more background on the subject.

https://medium.com/swlh/cooperative-multiple-inheritance-paradigm-in-python-f048b7ecdb29

-----

OUR Framework:

Implementing custom Modules:

If you use dataclasses for parameter handling and do post initialization, do NOT use the `__post_init__(self)` data classes sadly break cooperative multiple inheritance.
Instead use our custom `post_init(self)` and call `super().post_init()`, to make sure all base classes are initialized.
If you do not use dataclasses then within your `__init__(self, **kwargs)` call our custom `super().init([cls])` where `[cls]`  is the classname of the class you are just writing. Again this makes sure all base classes are initialized (skipping dataclasses).

We advice to always use dataclasses for parameter handling, and non dataclasses for interfaces or bases without any `__init__` arguments.
All parameters should use our field initializers `init()`, `pre_init()` or `post_init()`. Detailed explanation on the field initializers follows.

Using existing modules within your modules:
If you build a custom module and you want to use existing modules the user can configure this is done in two steps:

1. Module initialization: you provide a `init()` field with the module interface type, for which the experimenter can set the actual module during experiment creation.
2. Within your own `post_init(self)` or `__init__(self, **kwargs)` method you call the object and assign it to itself, like `self.module = self.module([**kwargs])`. This is the step where you inject all dependencies the module needs.

Thanks to our dependency injector framework, these injected dependencies will be available inside the called module even before its `post_init(self)` or `__init__(self, **kwargs)` is called.

Module creation process:
For better intuition our internal module creation process works as follows (a lot of magic is happening under the hood):

1. The experimenter creates an Blueprint by calling the modules `__init__(self, **kwargs)` function, BUT the init function is not executed, as we intercept execution.
2. The models are build from parents towards children, (please note we are talking about compositional structure, not inheritance). During initialization of the parent (in its init or post_init function) it can inject dependencies into its children by calling them.
3. The `__call__` function of a child is executed, injecting the dependencies.
4. All the `__init__(self, **kwargs)` function of the child is executed, doing initialization possibly by using the injected dependencies, and calling its own children. Dataclasses only set the fields at this point.
5. The `post_init(self)` is executed for all classes, here dataclasses can perform further initialization, like calling children.
    Normal classes can also use this method to perform actions that requires all initialization to be finished.

From the perspective of a experimenter this looks easy and clean, one can just use the classes like normal classes and the injected dependencies can be used insight the init method like they where always there.
It is also very easy to inject dependencies into new modules.

Field Initializers:

`init()` is used for parameters a experimenter sets at experiment construction time, this could be other subsequent used experiment modules or hyper-parameters. Is is a good practice to provide sensible default values.
`pre_init()` is used for fields the experimenter does not need to set in experiments, but you as a model builder need internally, like buffers custom models and so on.
`post_init()` parameters are used internally by the framework for dependency injection, and are only required if you extend framework capability to new use cases, i.e., use our framework as a meta framework to build new frameworks. Here you can initialize fields via the classes `__call__` function that are then present in an object BEFORE the object is initialized and can be used by an experimenter during initialization. More details on this in the advanced chapter of dependency injection.



Dependency Injection:
TODO

