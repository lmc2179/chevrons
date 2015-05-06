from chevrons.pipeline_base import PipelineBlock

class Filter(PipelineBlock):
    """
    Filter out data through this block by checking the truth of the given function.
    """
    def __init__(self, function):
        self.function = function

    def run(self, input_data):
        return (element for element in input_data if self.function(element))


class Fold(PipelineBlock):
    """
    Successively reduce inputs with the given binary function.
    """
    def __init__(self, function):
        self.function = function

    def run(self, input_data):
        input_iter = iter(input_data)
        x = next(input_iter)
        for element in input_iter:
            x = self.function(x, element)
        return x


class Map(PipelineBlock):
    """
    Map each item passing through this block using the given function.
    """
    def __init__(self, function):
        self.function = function

    def run(self, input_data):
        return (self.function(element) for element in input_data)


