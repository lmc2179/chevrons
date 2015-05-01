import unittest
import pipeline
import numpy as np
import functools

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

class ConvertToVector(pipeline.IteratorFunction):
    def _process_element(self, element):
        return np.array([int(element['COL_1']), int(element['COL_2'])])

class SumVectors(pipeline.ReduceFunction):
    def reduction_function(self, input_1, input_2):
        return input_1 + input_2

class UseCaseTest(unittest.TestCase):
    def test_end_to_end(self):
        import csv
        input_file = csv.DictReader(open('test_data.csv'))
        run_data_pipeline = ConvertToVector() >> SumVectors()
        run_data_pipeline(input_file) == [4, 6]