from multiprocessing import Pool
import functools

class PipelineFunction(object):
    def __ror__(self, other): # Other is used as an input
        return self.run(other)

    def __rshift__(self, other): # This function is composed with other
        inner_fxn = lambda x: other.run(self.run(x))
        F = PipelineFunction()
        F.run = inner_fxn
        return F

    def __call__(self, input_data):
        return self.run(input_data)

    def run(self, input_data):
        raise NotImplementedError

class IteratorFunction(PipelineFunction):
    def run(self, input_data):
        return (self._process_element(element) for element in input_data)

    def _process_element(self, element):
        raise NotImplementedError

class ReduceFunction(object):
    def run(self, input_data):
        x = next(input_data)
        for element in input_data:
            x = self.reduction_function(x, element)
        return x

    def reduction_function(self, input_1, input_2):
        raise NotImplementedError