"""
Pipeline objects with built-in parallelism. These classes are not yet stable.
"""
import functools
from multiprocessing.pool import Pool
import threading
import itertools
    
from chevrons.pipeline_base import PipelineBlock, AbstractBatchProcessorBlock

class ParallelBatchProcessorBlock(AbstractBatchProcessorBlock):
    def __init__(self, function, batch_size=1, n_process=None):
        super(ParallelBatchProcessorBlock, self).__init__(batch_size)
        self.pool = Pool(processes=n_process)
        self.function = function

    def _get_batch_transformation(self, batches):
        return self.pool.imap(self.function, batches, chunksize=self.batch_size)


class FilterParallel(PipelineBlock):
    def __init__(self, function, n_process=None):
        self.function = self._construct_filter_function(function)
        self.pool = Pool(processes=n_process)

    def _construct_filter_function(self, function):
        return _FilterFunctionClosure(function)

    def run(self, input_data):
        return self.pool.imap(self.function, input_data, chunksize=1)


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
    def __init__(self, function, n_processes=None):
        self.function = _MapFunctionClosure(function)
        self.pool = Pool(processes=n_processes)

    def run(self, input_data):
        return self.pool.imap(self.function, input_data, chunksize=1)

class _MapFunctionClosure(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        return [self.function(element) for element in args[0]]


def locked_iter(it):
    it = iter(it)
    lock = threading.Lock()
    while 1:
        try:
            with lock:
                value = next(it)
        except StopIteration:
            return
        yield value

class MakeThreadSafeBatches(PipelineBlock):
    def __init__(self, batch_size):
        self.batch_size = batch_size

    def run(self, input_data):
        return locked_iter(self._make_batches_from_iter(input_data, self.batch_size))

    def _make_batches_from_iter(self, data, batch_size):
        iterator = iter(data)
        while True:
            batch = list(itertools.islice(iterator, batch_size))
            if batch:
                yield batch
            else:
                return

class Unbatch(PipelineBlock):
    def run(self, input_data):
        return self._flatten_iterator(input_data)

    def _flatten_iterator(self, iterator):
        for batch in iterator:
            for element in batch:
                yield element

import warnings
warnings.warn('pipeline_parallel.py: These classes are not yet stable. Use at your own risk.')