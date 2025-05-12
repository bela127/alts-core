#Version 1.1.1 conform as of 01.04.2025
"""
| *alts.core.evaluator*
| :doc:`Built-In Implementations </modules/evaluator>`
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

import os

if TYPE_CHECKING:
    from typing import Callable, Optional
    from alts.core.experiment import Experiment

from alts.core.configuration import Configurable, post_init



class Evaluator(Configurable):
    """
    Evaluator()
    | **Description**
    |   The Evaluator evaluates the results of an experiment. An evaluation can take any shape and may wrap any function of the experiment.
    """
    experiment: Experiment = post_init()

    def register(self, experiment: Experiment):
        """
        register(self, experiment) -> None
        | **Description**
        |   Registers a new experiment as the one to be evaluated.

        :param experiment: The experiment to be evaluated
        :type experiment: Experiment
        """
        self.experiment = experiment

@dataclass
class LogingEvaluator(Evaluator):
    """
    LogingEvaluator(experiment)
    | **Description**
    |   Logs the evaluation of the experiment into a ```./eval/log``` folder.

    :param experiment: The experiment to be evaluated
    :type experiment: Experiment
    """
    folder: str = "log"
    root_path: str = "./eval"
    path = "./eval"

    @property
    def iteration(self):
        """
        iteration(self) -> int
        | **Description**
        |   Returns the current iteration of the experiment.

        :return: Current iteration of the experiment
        :rtype: int
        """
        return self.experiment.iteration

    def register(self, experiment: Experiment):
        """
        register(self, experiment) -> None
        | **Description**
        |   Registers the experiment to be evaluated and creates the appropiate logging folders.

        :param experiment: The experiment to be evaluated
        :type experiment: Experiment
        """
        super().register(experiment)
        self.path = self.root_path
        if self.experiment.exp_path is not None:
            self.path = os.path.join(self.experiment.exp_path, self.path)
        if self.experiment.exp_name is not None:
            self.path = os.path.join(self.path, self.experiment.exp_name)
        self.path = os.path.join(self.path, self.folder)
        self.path = os.path.join(self.path, f'exp_{self.experiment.exp_nr}')

        os.makedirs(self.path, exist_ok=True)


import functools

class Evaluate():
    """
    Evaluate(func)
    | **Description**
    |   Evaluate is a modifiable function decorator/wrapper . You may set a function that runs beforehand, afterwards, or receives the original function as an argument.
    |   Call the currently wrapped function with Evaluate().

    :param func: Function to be wrapped
    :type func: function
    """
    def __init__(self, func):
        """
        __init__(self, func) -> None
        | **Description**
        |   Sets ```func``` as its original function and initiates the ```pre```, ```wrap```, and ```post``` functions to do nothing (i.e. calling ```Evaluate(*args, **kwargs)``` now would yield ```original_func(*args, **kwargs)```).

        :param func: Function to be wrapped
        :type func: function
        """
        functools.update_wrapper(self, func)
        self._original_func = func
        self._pre_func: Optional[Callable] = None
        self._wrap_func: Optional[Callable] = None
        self._post_func: Optional[Callable] = None

    def __call__(self, *args, **kwargs):
        """
        __call__(self, *args, **kwargs)
        | **Description**
        |   Calls the wrapped function with the given arguments.
        |   Running order: pre(*args, **kwargs), wrap(original_func, *args, **kwargs), post(*args, **kwargs)

        :return: The result of wrap(original_func, *args, **kwargs)
        :rtype: any
        """
        if not self._pre_func is None:
            self._pre_func(*args, **kwargs)
        if not self._wrap_func is None:
            result = self._wrap_func(self._original_func, *args, **kwargs)
        else:
            result = self._original_func(*args, **kwargs)
        if not self._post_func is None:
            self._post_func(result)
        return result

    
    def pre(self, func):
        """
        pre(self, func) -> None
        | **Description**
        |   Sets the function to run before the wrapped function. 

        :param func: Function to run before the wrapped function
        :type func: function
        """
        self._pre_func = func

    def warp(self, func):
        """
        wrap(self, func) -> None
        | **Description**
        |   Sets the function to wrap the original function (takes the original function as an argument). 

        :param func: Function to wrap the original function
        :type func: function
        """
        self._warp_func = func

    def post(self, func):
        """
        pre(self, func) -> None
        | **Description**
        |   Sets the function to run after the wrapped function.

        :param func: Function to run after the wrapped function
        :type func: function
        """
        self._post_func = func
