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

        self.time_source = bp.time_source()
        self.time_behavior = bp.time_behavior(data_pools=self.data_pools)

        self.process = bp.process(time_source=self.time_source, data_pools=self.data_pools)

        self.oracles = bp.oracles(process=self.process)

        self.experiment_modules = bp.experiment_modules(time_source=self.time_source, data_pools=self.data_pools, oracles=self.oracles)

        self.initial_query_sampler = bp.initial_query_sampler(exp_modules = self.experiment_modules)
        self.stopping_criteria = bp.stopping_criteria(exp = self)

        self.iteration = 0


    def run(self) -> int:
        self.time_dependent_loop(self.iteration)
        queries = self.initial_query_sampler.sample()
        self.oracles.process.add(queries)

        while True:
            self.query_dependent_loop()
            self.iteration += 1

            if not self.stopping_criteria.next: break

            self.time_dependent_loop(self.iteration)
            
        return self.exp_nr

    def time_dependent_loop(self, iteration: int):
        times = self.time_source.step(iteration)
        times, vars = self.time_behavior.query(times)
        self.data_pools.stream.add((times, vars))
        return times, vars

    def query_dependent_loop(self):
        queries = None
        results = None
        delayed_queries = None
        delayed_results = None

        if not self.oracles.process.empty and self.process.ready:
                queries = self.oracles.process.pop()
                queries, results = self.process.query(queries)
                self.data_pools.process.add((queries, results))

        self.process.update()
        
        if self.process.has_new_data:
            delayed_queries, delayed_results = self.process.delayed_results()
            self.data_pools.result.add((delayed_queries, delayed_results))

        self.experiment_modules.run()
        return queries, results, delayed_queries, delayed_results