from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alts.core.blueprint import Blueprint
    from nptyping import NDArray, Number, Shape


class Experiment():
    exp_nr: int

    def __init__(self, bp: Blueprint, exp_nr: int) -> None:
        self.exp_nr = exp_nr
        self.exp_path = bp.exp_path
        self.exp_name = bp.exp_name

        self.data_pools = bp.data_pools()

        self.oracles = bp.oracles()

        self.time_source = bp.time_source()

        self.process = bp.process(time_source=self.time_source, oracles = self.oracles, data_pools=self.data_pools)

        self.experiment_modules = bp.experiment_modules(time_source=self.time_source, data_pools=self.data_pools, oracles=self.oracles)

        self.stopping_criteria = bp.stopping_criteria(exp = self)

        self.iteration = 0

    def run(self) -> int:
        self.time_source.step(self.iteration)
        self.process.initialize()
        self.experiment_modules.initialize()

        while True:
            self.oracles.trigger_subscriber()
            self.process.step(self.iteration)

            self.data_pools.trigger_subscriber()
            self.experiment_modules.step(self.iteration)
            self.iteration += 1

            if not self.stopping_criteria.next: break

            self.time_source.step(self.iteration)
            
        return self.exp_nr