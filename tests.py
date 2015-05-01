import unittest
import pipeline
import numpy as np

class Square(pipeline.PipelineFunction):
    def run(self, input_data):
        print('Square', input_data)
        return input_data ** 2

class AddOne(pipeline.PipelineFunction):
    def run(self, input_data):
        print('AddOne', input_data)
        return input_data + 1

class SquareElements(pipeline.IteratorFunction):
    def _process_element(self, element):
        return element ** 2

class AddOneToElements(pipeline.IteratorFunction):
    def _process_element(self, element):
        return element + 1


class SyntaxTest(unittest.TestCase):
    def test_pipe(self):
        assert (2 | Square()) == 4

    def test_shift(self):
        f = Square() >> Square() >> AddOne()
        assert f(2) == 17

    def test_pipe_and_shift(self):
        assert (2 | Square() >> Square() >> AddOne()) == 17

    def test_iterator_function(self):
        assert list([1,2] | SquareElements() >> SquareElements()  >> AddOneToElements()) == [2,17]