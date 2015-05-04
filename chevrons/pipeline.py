from multiprocessing import Pool
import functools
import itertools

class Processor(object):
    def __ror__(self, other): # Other is used as an input
        return self.run(other)

    def __rshift__(self, other): # This function is composed with other
        inner_fxn = lambda x: other.run(self.run(x))
        F = Processor()
        F.run = inner_fxn
        return F

    def __call__(self, input_data):
        return self.run(input_data)

    def run(self, input_data):
        raise NotImplementedError

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

class Fold(Processor):
    def run(self, input_data):
        x = next(input_data)
        for element in input_data:
            x = self.reduction_function(x, element)
        return x

    def reduction_function(self, input_1, input_2):
        raise NotImplementedError

class Filter(Processor):
    def __init__(self, function):
        self.function = function

    def run(self, input_data):
        return (element for element in input_data if self.function(element))

class AbstractBatchProcessor(Processor):
    def __init__(self, batch_size):
        self.batch_size = batch_size

    def run(self, input_data):
        batches = self._make_batches_from_iter(input_data, self.batch_size)
        processed_batches = self._get_batch_transformation(batches)
        chained_batches = self._flatten_iterator(itertools.chain(processed_batches))
        return chained_batches

    def _get_batch_transformation(self, batches):
        raise NotImplementedError

    def _flatten_iterator(self, iterator):
        for batch in iterator:
            for element in batch:
                yield element

    def _process_batch(self, input_batch):
        raise NotImplementedError

    def _make_batches_from_iter(self, data, batch_size):
        iterator = iter(data)
        while True:
            batch = list(itertools.islice(iterator, batch_size))
            if batch:
                yield batch
            else:
                return

class SerialBatchProcessor(AbstractBatchProcessor):
    def _get_batch_transformation(self, batches):
        return (self._process_batch(b) for b in batches)

class ParallelBatchProcessor(AbstractBatchProcessor):
    def __init__(self, function, batch_size=1, n_process=None):
        super(ParallelBatchProcessor, self).__init__(batch_size)
        self.pool = Pool(processes=n_process)
        self.function = function

    def _get_batch_transformation(self, batches):
        return self.pool.imap(self.function, batches, chunksize=self.batch_size)

class FilterFunction(object):
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        return [element for element in args[0] if self.function(element)]

class FilterParallel(ParallelBatchProcessor):
    def __init__(self, function, batch_size=1, n_process=None):
        filter_function = self._construct_filter_function(function)
        super(FilterParallel, self).__init__(filter_function, batch_size=batch_size, n_process=n_process)

    def _construct_filter_function(self, function):
        return FilterFunction(function)