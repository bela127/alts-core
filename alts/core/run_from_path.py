#Version 1.1.1 conform as of 14.12.2024
"""
| *alts.core.run_from_path*
"""
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
    """
    load_modules_from_folder(experiment_path) -> modules
    | **Description**
    |   Loads and returns all modules from the ``experiment_path`` folder.
    |   It does so by loading all .py files in the folder. Subfolders are ignored.

    :param experiment_path: Path to folder with modules
    :type experiment_path: Dir path
    :return: The modules inside the ``experiment_path`` folder
    :rtype: List[ModuleType]
    """
    for dirpath, dnames, fnames in os.walk(experiment_path):
        file_name: str
        for file_name in fnames:
            if file_name.endswith(".py"):
                module = load_module(dirpath, file_name)
                yield module

def load_module(dirpath: str, file_name: str):
    """
    load_module(dirpath, file_name) -> module
    | **Description**
    |   Loads and returns the contents of the specified file as a module using the importlib library. 

    :param dirpath: Path to folder containing module
    :type dirpath: Dir path
    :param file_name: The module in the folder to be loaded
    :param file_name: File name
    :return: Loaded, interactable module from the file
    :rtype: ModuleType

    :raises ImportError: If importlib fails to find a  module spec or fails to create spec.loader
    """
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
    """
    set_exp_path_and_name(module, exp_path) -> blueprints
    | **Description**
    |   Returns all blueprints from a module and sets their experiment path to ``exp_name``.
    |   It first tries to load a blueprint from ``module.blueprint``. If that fails, it tries
        to load a list of blueprints from ``module.blueprints``. If that fails, too, it returns 
        an empty list.

    :param module: Module to be laoded from
    :type module: ModuleType
    :param exp_path: The desired experiment output path. A new output folder "eval" will be created in there.
    :type exp_path: Dir path
    :return: All prepared blueprints
    :rtype: list[Blueprint]
    """
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
    """
    run_experiments_from_folder(experiment_path, parallel) -> None
    | **Description**
    |   Loads all blueprint found in modules in ``experiment_path`` and runs an experiment with each configuration.
    |   The output folder ("eval") with its output files will be created in ``experiment_path``.

    :param experiment_path: Folder with modules containing blueprints
    :type experiment_path: Dir path
    :param parallel: If True, runs experiments in parallel (default= False)
    :type parallel: bool
    """
    blueprints = []
    for module in load_modules_from_folder(experiment_path):
        blueprints.extend(set_exp_path_and_name(module, experiment_path))
    er = ExperimentRunner(blueprints)
    if parallel:
        er.run_experiments_parallel()
    else:
        er.run_experiments()




