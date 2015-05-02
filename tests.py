import unittest
from pipeline import Map, Fold, Processor, MapParallel
import numpy as np
import functools

class Square(Processor):
    def run(self, input_data):
        return input_data ** 2

class AddOne(Processor):
    def run(self, input_data):
        return input_data + 1

def square(x):
        return x ** 2

def add_one(x):
    return x+1

class SyntaxTest(unittest.TestCase):
    def test_pipe(self):
        assert (2 | Square()) == 4

    def test_shift(self):
        f = Square() >> Square() >> AddOne()
        assert f(2) == 17

    def test_pipe_and_shift(self):
        assert (2 | Square() >> Square() >> AddOne()) == 17

    def test_map(self):
        assert list([1,2] | Map(square) >> Map(square)  >> Map(add_one)) == [2,17]

    def test_imap(self):
        assert list([1,2] | MapParallel(square) >> MapParallel(square)  >> MapParallel(add_one)) == [2,17]

def parse_row( element):
        return np.array([int(element['COL_1']), int(element['COL_2'])])

def sum_vectors(input_1, input_2):
        return input_1 + input_2

class UseCaseTest(unittest.TestCase):
    def test_end_to_end(self):
        import csv
        input_file = csv.DictReader(open('test_data.csv'))
        run_data_pipeline = Map(parse_row) >> Map(sum_vectors)
        run_data_pipeline(input_file) == [4, 6]