"""
Pipeline objects with built-in parallelism. These classes are not yet stable.
"""
import functools
from multiprocessing.pool import Pool
import threading
import itertools
    
from pipeline_base import PipelineBlock

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


class FoldParallel(PipelineBlock):
    def __init__(self, function, n_process=None):
        self.function = function
        self.pool = Pool(processes=n_process)

    def _construct_fold_function(self, function):
        return _FoldFunctionClosure(function)

    def run(self, input_data):
        batch_function = self._construct_fold_function(self.function)
        return self._fold_stream(self.pool.imap(batch_function, input_data, chunksize=1))

    def _fold_stream(self, input_data):
        input_iter = iter(input_data)
        x = next(input_iter)
        for element in input_iter:
            x = self.function(x, element)
        return x


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

class BeginParallel(PipelineBlock):
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

class EndParallel(PipelineBlock):
    def run(self, input_data):
        return self._flatten_iterator(input_data)

    def _flatten_iterator(self, iterator):
        for batch in iterator:
            for element in batch:
                yield element

import warnings
warnings.warn('pipeline_parallel.py: These classes are not yet stable. Use at your own risk.')