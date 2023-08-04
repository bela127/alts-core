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
    def __init__(self, blueprints: Iterable[Blueprint]) -> None:
        self.evaluators: List[Evaluator] = []
        self.blueprints = blueprints

    def run_experiment(self, blueprint: Blueprint):
        self.evaluators = []
        
        for evaluator in blueprint.evaluators:
            self.evaluators.append(evaluator())
        
        for exp_nr in range(blueprint.repeat):
            experiment = Experiment(blueprint, exp_nr)

            self.register_evaluators(experiment)
            
            print("Running:", experiment.exp_name, exp_nr)
            experiment.run()

    def run_repetition(self, exp_config: Tuple[Blueprint, int]):
        blueprint, exp_nr = exp_config
        evaluators: List[Evaluator] = []
        for evaluator in blueprint.evaluators:
            evaluators.append(evaluator())
        
        experiment = Experiment(blueprint, exp_nr)
        
        for evaluator in evaluators:
            evaluator.register(experiment)
        
        print("Running:", experiment.exp_name, exp_nr)
        experiment.run()
        
    
    def run_experiment_parallel(self, blueprint: Blueprint, nr_processes: int = int(os.cpu_count() / 2)):
        exp_configs = []
        for exp_nr in range(blueprint.repeat):
            exp_configs.append((blueprint,exp_nr))
        
        with Pool(nr_processes) as p:
            p.map(self.run_repetition, exp_configs)

    def run_experiments(self, blueprints: Union[Iterable[Blueprint], None] = None):
        if blueprints is None: blueprints = self.blueprints

        for blueprint in blueprints:
            self.run_experiment(blueprint)

    def run_experiments_parallel(self, blueprints: Union[Iterable[Blueprint], None] = None, nr_processes: int = int(os.cpu_count() / 2), parallel_sub_exp=True):
        if blueprints is None: blueprints = self.blueprints
        if parallel_sub_exp:
            for blueprint in blueprints:
                self.run_experiment_parallel(blueprint)
        else:
            with Pool(nr_processes) as p:
                p.map(self.run_experiment, blueprints)
    


    def register_evaluators(self, experiment):
        for evaluator in self.evaluators:
            evaluator.register(experiment)
