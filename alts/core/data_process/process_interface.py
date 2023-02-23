
class Environment():

    def update():
        pass

    def set_state(time, state):
        pass

    def get_unobservables():
        pass

    def get_observables():
        pass

    def get_queriables():
        pass

class Process():

    def run():
        pass

#controlled
    def set_controllables():
        pass

    def set_constants():
        pass

#environmeltal:
    def set_unobservable_env():
        pass

    def set_observable_env():
        pass

    def get_observable_env():
        pass

    def env_querieables():
        pass

    def query_env():
        pass

    def env_query_result():
        pass

    def get_unobservable_env():
        pass

# intermediate:
    def get_observable_inter():
        pass

    def inter_querieables():
        pass

    def query_inter():
        pass

    def inter_query_result():
        pass

    def get_unobservable_inter():
        pass

# output:
    def get_observable_out():
        pass

    def out_querieables():
        pass

    def query_out():
        pass

    def out_query_result():
        pass

    def get_unobservable_out():
        pass

class Oracle():
    #environmeltal:
    def set_observable_env():
        pass

    def get_observable_env():
        pass

    def env_querieables():
        pass

    # intermediate:
    def inter_querieables():
        pass

    def query_inter():
        pass

    def inter_query_result():
        pass

    # output:
    def out_querieables():
        pass

    def query_out():
        pass

    def out_query_result():
        pass

class Variable():

    def precition():
        pass

class Querieable():

    def cost():
        pass #constant or known input dependent or unknown

    def time():
        pass #constant or known input dependent or unknown

class QueryResult(Variable):

    def cost():
        pass #actual cost

    def time():
        pass #actual time

class Baseline():

#environmeltal:

    def get_observable_env():
        pass

    def get_env_querieables():
        pass

    def get_unobservable_env():
        pass

# intermediate:
    def get_observable_inter():
        pass

    def get_inter_querieables():
        pass

    def get_unobservable_inter():
        pass

# output:
    def get_observable_out():
        pass

    def get_out_querieables():
        pass

    def get_unobservable_out():
        pass
