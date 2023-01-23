from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

import os

if TYPE_CHECKING:
    from typing import Callable, Optional
    from alts.core.experiment import Experiment

from alts.core.configuration import Configurable, post_init



class Evaluator(Configurable):
    experiment: Experiment = post_init()

    def register(self, experiment: Experiment):
        self.experiment = experiment

@dataclass
class LogingEvaluator(Evaluator):
    folder: str = "log"
    root_path: str = "./eval"
    path = "./eval"


    def register(self, experiment: Experiment):
        super().register(experiment)
        self.path = self.root_path
        if not self.experiment.exp_path is None:
            self.path = os.path.join(self.experiment.exp_path, self.path)
        if not self.experiment.exp_name is None:
            self.path = os.path.join(self.path, self.experiment.exp_name)
        self.path = os.path.join(self.path, self.folder)
        self.path = os.path.join(self.path, f'exp_{self.experiment.exp_nr}')

        os.makedirs(self.path, exist_ok=True)


import functools

class Evaluate:

    def __init__(self, func):
        functools.update_wrapper(self, func)
        self._warped_func = func
        self._pre_func: Optional[Callable] = None
        self._warp_func: Optional[Callable] = None
        self._post_func: Optional[Callable] = None

    def __call__(self, *args, **kwargs):
        if not self._pre_func is None:
            self._pre_func(*args, **kwargs)
        if not self._warp_func is None:
            result = self._warp_func(self._warped_func, *args, **kwargs)
        else:
            result = self._warped_func(*args, **kwargs)
        if not self._post_func is None:
            self._post_func(result)
        return result

    
    def pre(self, methode):
        self._pre_func = methode

    def warp(self, methode):
        self._warp_func = methode

    def post(self, methode):
        self._post_func = methode
