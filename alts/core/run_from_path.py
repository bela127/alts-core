from __future__ import annotations
from types import ModuleType
from typing import TYPE_CHECKING, List

import sys
import os
import importlib.util
from alts.core.experiment_runner import ExperimentRunner

if TYPE_CHECKING:
    from alts.core.blueprint import Blueprint

def load_modules_from_folder(experiment_path):
    for dirpath, dnames, fnames in os.walk(experiment_path):
        file_name: str
        for file_name in fnames:
            if file_name.endswith(".py"):
                module = load_module(dirpath, file_name)
                yield module

def load_module(dirpath: str, file_name: str):
    file_path = os.path.join(dirpath, file_name)
    module_name = file_name.split(sep=".")[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError()
    else:
        module = importlib.util.module_from_spec(spec)
        if spec.loader is None:
            raise ImportError()
        else:
            spec.loader.exec_module(module)
        return module

def set_exp_path_and_name(module: ModuleType, exp_path: str):
    try:
        blueprint: Blueprint = module.blueprint
        blueprint.exp_path = os.path.join(exp_path, "eval", module.__name__)
        blueprint.exp_name = module.__name__
        return [blueprint]
    except AttributeError:
        try:
            print("loaded file not a blueprint, test for multiple blueprints")
            blueprints: List[Blueprint] = module.blueprints
            for blueprint in blueprints:
                blueprint.exp_path = os.path.join(exp_path, "eval", module.__name__)
            return blueprints
        except AttributeError:
            print("loaded file contains no blueprints, skipping file!")
            return []
    

def run_experiments_from_folder(experiment_path, parallel = False):
    blueprints = []
    for module in load_modules_from_folder(experiment_path):
        blueprints.extend(set_exp_path_and_name(module, experiment_path))
    er = ExperimentRunner(blueprints)
    if parallel:
        er.run_experiments_parallel()
    else:
        er.run_experiments()




