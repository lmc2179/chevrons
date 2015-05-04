from multiprocessing import Pool
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
    def __init__(self, function, n_cores=None, batch_size=1):
        self.function = function
        self.pool = Pool(processes=n_cores)
        self.batch_size = batch_size

    def run(self, input_data):
        return self.pool.imap(self.function, input_data, chunksize=self.batch_size)

class Fold(object):
    def run(self, input_data):
        x = next(input_data)
        for element in input_data:
            x = self.reduction_function(x, element)
        return x

    def reduction_function(self, input_1, input_2):
        raise NotImplementedError

class BatchProcessor(Processor):
    def __init__(self, batch_size):
        self.batch_size = batch_size

    def run(self, input_data):
        batches = self._make_batches_from_iter(input_data, self.batch_size)
        processed_batches = (self._process_batch(b) for b in batches)
        chained_batches = self._flatten_iterator(itertools.chain(processed_batches))
        return chained_batches

    def _flatten_iterator(self, iterator):
        for batch in iterator:
            for element in batch:
                yield element

    def _process_batch(self, input_batch):
        raise NotImplementedError

    def _make_batches_from_iter(self, iterator, batch_size):
        while True:
            batch = list(itertools.islice(iterator, batch_size))
            if batch:
                yield batch
            else:
                return