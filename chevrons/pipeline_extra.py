from chevrons.pipeline_base import SerialBatchProcessorBlock

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