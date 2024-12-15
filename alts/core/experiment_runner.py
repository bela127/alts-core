#Version 1.1.1 conform as of 15.12.2024
"""
| *alts.core.experiment_runner*
"""
from __future__ import annotations
from typing import TYPE_CHECKING

from multiprocessing import Pool
import os

from alts.core.evaluator import Evaluator

from alts.core.experiment import Experiment

if TYPE_CHECKING:
    from typing import Tuple, Union, Iterable, List
    from alts.core.blueprint import Blueprint



class ExperimentRunner():
    """
    ExperimentRunner(blueprints)
    | **Description**
    |   Runs experiments as described by blueprints.

    :param blueprints: Blueprints describing experiments to run
    :type blueprints: Iterable[Blueprint]
    """
    def __init__(self, blueprints: Iterable[Blueprint]) -> None:
        """
        __init__(self, blueprints) -> None
        | **Description**
        |   Saves ``blueprints`` locally and initializes empty lists.

        :param blueprints: The blueprints for the experiments
        :type blueprints: Iterable[Blueprint]
        """
        self.evaluators: List[Evaluator] = []
        self.blueprints = blueprints

    def run_experiment(self, blueprint: Blueprint):
        """
        run_experiment(blueprint) -> None
        | **Description**
        |   Runs the experiment based on ``blueprint`` on a single core.

        :param blueprint: The blueprint for the experiment
        :type blueprint: Blueprint
        """
        self.evaluators = []
        
        for evaluator in blueprint.evaluators:
            self.evaluators.append(evaluator())
        
        for exp_nr in range(blueprint.repeat):
            experiment = Experiment(blueprint, exp_nr)

            self.register_evaluators(experiment)
            
            print("Running:", experiment.exp_name, exp_nr)
            experiment.run()

    def run_repetition(self, exp_config: Tuple[Blueprint, int]):
        """
        run_repetition(self, exp_config) -> None
        | **Description**
        |   Runs the configured experiment once with the given ``exp_nr``, 
            ignoring the configured amount of repetitions.

        :param exp_config: A blueprint and a given experiment number
        :type exp_config: Tuple[Blueprint, int]
        """
        blueprint, exp_nr = exp_config
        evaluators: List[Evaluator] = []
        for evaluator in blueprint.evaluators:
            evaluators.append(evaluator())
        
        experiment = Experiment(blueprint, exp_nr)
        
        for evaluator in evaluators:
            evaluator.register(experiment)
        
        print("Running:", experiment.exp_name, exp_nr)
        experiment.run()
        
    
    def run_experiment_parallel(self, blueprint: Blueprint, nr_processes: int = int(os.cpu_count() / 2)): # type: ignore
        """
        run_experiment_parallel(self, blueprint, nr_processes) -> None
        | **Description**
        |   Runs a single experiment on multiple cores.

        :param blueprint: The blueprint for the experiment
        :type blueprint: Blueprint
        :param nr_processes: How many processes to run in parallel (default= 1/2 CPU count)
        :type nr_processes: int
        """
        exp_configs = []
        for exp_nr in range(blueprint.repeat):
            exp_configs.append((blueprint,exp_nr))
        
        with Pool(nr_processes) as p:
            p.map(self.run_repetition, exp_configs)

    def run_experiments(self, blueprints: Union[Iterable[Blueprint], None] = None):
        """
        run_experiments(self, blueprints) -> None
        | **Description**
        |   Runs multiple experiments on asingle core.

        :param blueprints: Blueprints for experiments (default= None)
        :type blueprints: Iterable[Blueprint]
        """
        if blueprints is None: blueprints = self.blueprints

        for blueprint in blueprints:
            self.run_experiment(blueprint)

    def run_experiments_parallel(self, blueprints: Union[Iterable[Blueprint], None] = None, nr_processes: int = int(os.cpu_count() / 2), parallel_sub_exp=True): # type: ignore
        """
        run_experiment_parallel(self, blueprint, nr_processes) -> None
        | **Description**
        |   Runs a multiple experiments. Runs either each experiment on multiple cores 
            or one experiment per core.

        :param blueprint: The blueprints for the experiments (default= None)
        :type blueprint: Iterbale[Blueprint]
        :param nr_processes: How many processes to run in parallel (default= 1/2 CPU count)
        :type nr_processes: int
        :param parallel_sub_exp: Whether to run a single experiment in parallel (or multiple experiments in parallel) (default= True)
        :type parallel_sub_exp: bool
        """
        if blueprints is None: blueprints = self.blueprints
        if parallel_sub_exp:
            for blueprint in blueprints:
                self.run_experiment_parallel(blueprint)
        else:
            with Pool(nr_processes) as p:
                p.map(self.run_experiment, blueprints)
    


    def register_evaluators(self, experiment):
        """
        register_evaluators(self,experiment) -> None
        | **Description**
        |   Registers the experiment in all own evaluators.

        :param experiment: Experiment to be registered
        :type experiment: Experiment
        """
        for evaluator in self.evaluators:
            evaluator.register(experiment)
