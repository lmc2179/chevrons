from pipeline_base import Processor

class Filter(Processor):
    def __init__(self, function):
        self.function = function

    def run(self, input_data):
        return (element for element in input_data if self.function(element))


class Fold(Processor):
    def __init__(self, function):
        self.function = function

    def run(self, input_data):
        input_iter = iter(input_data)
        x = next(input_iter)
        for element in input_iter:
            x = self.function(x, element)
        return x


class Map(Processor):
    def __init__(self, function):
        self.function = function

    def run(self, input_data):
        return (self.function(element) for element in input_data)


