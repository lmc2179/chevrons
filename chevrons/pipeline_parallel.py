"""
Pipeline objects with built-in parallelism. These classes are not yet stable.
"""
import functools
from multiprocessing.pool import Pool
from chevrons.pipeline_base import PipelineBlock, AbstractBatchProcessorBlock

class ParallelBatchProcessorBlock(AbstractBatchProcessorBlock):
    def __init__(self, function, batch_size=1, n_process=None):
        super(ParallelBatchProcessorBlock, self).__init__(batch_size)
        self.pool = Pool(processes=n_process)
        self.function = function

    def _get_batch_transformation(self, batches):
        return self.pool.imap(self.function, batches, chunksize=self.batch_size)


class FilterParallel(ParallelBatchProcessorBlock):
    def __init__(self, function, batch_size=1, n_process=None):
        filter_function = self._construct_filter_function(function)
        super(FilterParallel, self).__init__(filter_function, batch_size=batch_size, n_process=n_process)

    def _construct_filter_function(self, function):
        return _FilterFunctionClosure(function)


class _FoldFunctionClosure(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        return functools.reduce(self.function, args[0])


class FoldParallel(ParallelBatchProcessorBlock):
    def __init__(self, function, batch_size=1, n_process=None):
        fold_function = self._construct_fold_function(function)
        super(FoldParallel, self).__init__(fold_function,batch_size=batch_size, n_process=n_process)

    def _construct_fold_function(self, function):
        return _FoldFunctionClosure(function)


class _FilterFunctionClosure(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        return [element for element in args[0] if self.function(element)]


class MapParallel(PipelineBlock):
    def __init__(self, function, n_processes=None, batch_size=1):
        self.function = function
        self.pool = Pool(processes=n_processes)
        self.batch_size = batch_size

    def run(self, input_data):
        return self.pool.imap(self.function, input_data, chunksize=self.batch_size)

import warnings
warnings.warn('pipeline_parallel.py: These classes are not yet stable. Use at your own risk.')