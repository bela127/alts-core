from __future__ import annotations
from typing import TYPE_CHECKING

from multiprocessing import Pool

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
        

    def run_experiments(self, blueprints: Union[Iterable[Blueprint], None] = None):
        if blueprints is None: blueprints = self.blueprints

        for blueprint in blueprints:
            self.run_experiment(blueprint)

    def run_experiments_parallel(self, blueprints: Union[Iterable[Blueprint], None] = None):
        if blueprints is None: blueprints = self.blueprints

        with Pool(None) as p:
            p.map(self.run_experiment, blueprints)


    def register_evaluators(self, experiment):
        for evaluator in self.evaluators:
            evaluator.register(experiment)
