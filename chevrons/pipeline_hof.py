from pipeline_base import PipelineBlock

class Filter(PipelineBlock):
    def __init__(self, function):
        self.function = function

    def run(self, input_data):
        return (element for element in input_data if self.function(element))


class Fold(PipelineBlock):
    def __init__(self, function):
        self.function = function

    def run(self, input_data):
        input_iter = iter(input_data)
        x = next(input_iter)
        for element in input_iter:
            x = self.function(x, element)
        return x


class Map(PipelineBlock):
    def __init__(self, function):
        self.function = function

    def run(self, input_data):
        return (self.function(element) for element in input_data)


