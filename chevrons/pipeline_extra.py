from pipeline_base import PipelineBlock
import itertools

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

class SideEffectBlock(SerialBatchProcessorBlock):
    def __init__(self, return_data=True, batch_size=1):
        self.return_data=return_data
        super(SideEffectBlock, self).__init__(batch_size=batch_size)

    def _get_batch_transformation(self, batches):
        if self.return_data:
            return (self._process_batch(b) for b in batches)
        else:
            for b in batches:
                self._side_effect(b)
            return []

    def _process_batch(self, input_batch):
        self._side_effect(input_batch)
        return input_batch

    def _side_effect(self, input_batch):
        raise NotImplementedError

class TrainScikitModel(SideEffectBlock):
    def __init__(self, model, batch_size=1):
        self.model = model
        super(TrainScikitModel, self).__init__(return_data=False, batch_size=batch_size)

    def _side_effect(self, input_batch):
        X,y = list(zip(*list(input_batch)))
        self.model.fit(X,y)