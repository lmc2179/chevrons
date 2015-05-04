from multiprocessing.pool import Pool
from pipeline_base import ParallelBatchProcessor, Processor


class _FilterFunctionClosure(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        return [element for element in args[0] if self.function(element)]


class FilterParallel(ParallelBatchProcessor):
    def __init__(self, function, batch_size=1, n_process=None):
        filter_function = self._construct_filter_function(function)
        super(FilterParallel, self).__init__(filter_function, batch_size=batch_size, n_process=n_process)

    def _construct_filter_function(self, function):
        return _FilterFunctionClosure(function)


class Filter(Processor):
    def __init__(self, function):
        self.function = function

    def run(self, input_data):
        return (element for element in input_data if self.function(element))


class Fold(Processor):
    def __init__(self, function):
        self.function = function

    def run(self, input_data):
        input_iter = iter(input_data)
        x = next(input_iter)
        for element in input_iter:
            x = self.function(x, element)
        return x

class FoldParallel(ParallelBatchProcessor):
    pass

class Map(Processor):
    def __init__(self, function):
        self.function = function

    def run(self, input_data):
        return (self.function(element) for element in input_data)


class MapParallel(Processor):
    def __init__(self, function, n_processes=None, batch_size=1):
        self.function = function
        self.pool = Pool(processes=n_processes)
        self.batch_size = batch_size

    def run(self, input_data):
        return self.pool.imap(self.function, input_data, chunksize=self.batch_size)