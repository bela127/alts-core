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

        self.process = bp.process(time_source = self.time_source, time_behavior = self.time_behavior)

        self.observable_stream = bp.observable_stream(constrained = self.time_behavior)
        self.stream_data_pool = bp.stream_data_pool(observable = self.observable_stream)

        self.observable_process = bp.observable_process(constrained = self.process)
        self.process_data_pool = bp.process_data_pool(observable = self.observable_process)

        self.observable_results = bp.observable_results(constrained = self.process)
        self.result_data_pool = bp.result_data_pool(observable = self.observable_results)

        self.oracle = Oracle(self.process.query_queue)

        self.experiment_modules = bp.experiment_modules(stream_data_pool = self.stream_data_pool, process_data_pool= self.process_data_pool, result_data_pool= self.result_data_pool, oracle= self.oracle)

        self.initial_query_sampler = bp.initial_query_sampler(exp_modules = self.experiment_modules)
        self.stopping_criteria = bp.stopping_criteria(exp = self)

        self.iteration = 0


    def run(self):
        queries = self.initial_query_sampler.sample()
        self.oracle.request(queries)
        while self.stopping_criteria.next:
            self.loop(self.iteration)
            self.iteration += 1
        return self.exp_nr

    def loop(self, iteration: int):
        times = self.time_source.step(iteration)
        times, vars = self.time_behavior.query(times)

        data_points = self.observable_stream.filter((times, vars))
        self.stream_data_pool.add(data_points)

        controls = None
        output = None
        if self.process.queried:
            controls, output = self.process.run(times, vars)
            data_points = self.observable_process.filter((controls, output))
            self.process_data_pool.add(data_points)
        
        results = None
        if self.process.finished:
            controls, results = self.process.results
            data_points = self.observable_results.filter((controls, results))
            self.result_data_pool.add(data_points)

        self.experiment_modules.run()
        return times, vars, controls, output, results