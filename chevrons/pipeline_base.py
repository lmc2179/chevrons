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

class Zip(PipelineBlock):
    "Zip the input streams together (similar to builtin zip() function)."
    def run(self, input_data):
        return zip(*input_data)

