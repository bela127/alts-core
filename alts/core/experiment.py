from __future__ import annotations
from typing import TYPE_CHECKING
from alts.core.oracle.oracle import Oracle

from alts.core.queryable import QueryableWrapper

if TYPE_CHECKING:
    from alts.core.blueprint import Blueprint
    from nptyping import NDArray, Number, Shape


class Experiment():
    exp_nr: int

    def __init__(self, bp: Blueprint, exp_nr: int) -> None:
        self.exp_nr = exp_nr
        self.exp_path = bp.exp_path
        self.exp_name = bp.exp_name

        self.time_source = bp.time_source()
        self.time_behavior = bp.time_behavior()

        self.stream_data_pool = bp.stream_data_pool(constrained = self.time_behavior)

        self.process = bp.process(time_source=self.time_source, stream_data_pool=self.stream_data_pool)

        self.query_queue = bp.query_queue(query_constrain = self.process.query_constrain)

        self.process_data_pool = bp.process_data_pool(constrained = self.process)

        self.result_data_pool = bp.result_data_pool(constrained = self.process)

        self.oracle = Oracle(self.query_queue)

        self.experiment_modules = bp.experiment_modules(stream_data_pool = self.stream_data_pool, process_data_pool= self.process_data_pool, result_data_pool= self.result_data_pool, oracle= self.oracle)

        self.initial_query_sampler = bp.initial_query_sampler(exp_modules = self.experiment_modules)
        self.stopping_criteria = bp.stopping_criteria(exp = self)

        self.iteration = 0


    def run(self):
        self.time_dependent_loop(self.iteration)
        queries = self.initial_query_sampler.sample()
        self.oracle.request(queries)

        while True:
            self.query_dependent_loop()
            self.iteration += 1

            if not self.stopping_criteria.next: break

            self.time_dependent_loop(self.iteration)
            
        return self.exp_nr

    def time_dependent_loop(self, iteration: int):
        times = self.time_source.step(iteration)
        times, vars = self.time_behavior.query(times)
        self.stream_data_pool.add((times, vars))
        return times, vars

    def query_dependent_loop(self):
        queries = None
        results = None
        delayed_queries = None
        delayed_results = None

        if not self.query_queue.empty and self.process.ready:
                queries = self.query_queue.pop()
                queries, results = self.process.query(queries)
                self.process_data_pool.add((queries, results))

        self.process.update()
        
        if self.process.has_new_data:
            delayed_queries, delayed_results = self.process.delayed_results()
            self.result_data_pool.add((delayed_queries, delayed_results))

        self.experiment_modules.run()
        return queries, results, delayed_queries, delayed_results