import itertools

class PipelineBlock(object):
    "Most basic block which allows chevron syntax. Subclasses must implement run method."
    def __ror__(self, other): # Other is used as an input
        return self.run(other)

    def __rshift__(self, other): # This function is composed with other
        inner_fxn = lambda x: other.run(self.run(x))
        F = PipelineBlock()
        F.run = inner_fxn
        return F

    def __call__(self, input_data):
        return self.run(input_data)

    def run(self, input_data):
        raise NotImplementedError

class Merge(PipelineBlock):
    def __init__(self, iterator):
        self.iterator = iterator

    def run(self, input_data):
        return zip(self.iterator, input_data)

class Zip(PipelineBlock):
    "Zip the input streams together (similar to builtin zip() function)."
    def run(self, input_data):
        return zip(*input_data)

class AbstractBatchProcessorBlock(PipelineBlock):
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

class SerialBatchProcessorBlock(AbstractBatchProcessorBlock):
    def _get_batch_transformation(self, batches):
        return (self._process_batch(b) for b in batches)


