import unittest
from pipeline import Map, Fold, Processor, MapParallel, SerialBatchProcessor#, ParallelBatchProcessor
import numpy as np

class Square(Processor):
    def run(self, input_data):
        return input_data ** 2

class AddOne(Processor):
    def run(self, input_data):
        return input_data + 1

class SwapInputs(Processor):
    def run(self, input_data):
        a,b = input_data
        return b,a

class AddOneSerialBatch(SerialBatchProcessor):
    def _process_batch(self, input_batch):
        return [add_one(i) for i in input_batch]

def square(x):
        return x ** 2

def add_one(x):
    return x+1

def add_one_batch(batch):
    return [x+1 for x in batch]

def infinite_generator():
    while True:
        yield 1

class SyntaxTest(unittest.TestCase):
    def test_pipe(self):
        assert (2 | Square()) == 4

    def test_shift(self):
        f = Square() >> Square() >> AddOne()
        assert f(2) == 17

    def test_pipe_and_shift(self):
        assert (2 | Square() >> Square() >> AddOne()) == 17

    def test_multiple_input(self):
        assert ((1,2) | SwapInputs()) == (2,1)

class FunctionTest(unittest.TestCase):
    def test_map(self):
        assert list([1,2] | Map(square) >> Map(square)  >> Map(add_one)) == [2,17]

    def test_imap(self):
        assert list([1,2] | MapParallel(square) >> MapParallel(square)  >> MapParallel(add_one)) == [2,17]

    def test_map_infinite(self):
        data = infinite_generator()
        output_stream = data | Map(square) >> MapParallel(square)
        assert next(output_stream) == 1

    def test_batch_process(self):
        import itertools
        data = itertools.islice(infinite_generator(),0,1000)
        output = data | AddOneSerialBatch(100) >> AddOneSerialBatch(100)
        assert len(list(output)) == 1000

    def test_batch_process_infinite(self):
        data = infinite_generator()
        output = data | AddOneSerialBatch(100) >> AddOneSerialBatch(100)
        assert next(output) == 3

    # def test_batch_process_parallel(self):
    #     import itertools
    #     data = itertools.islice(infinite_generator(),0,1000)
    #     output = data | ParallelBatchProcessor(add_one_batch) >> ParallelBatchProcessor(add_one_batch)
    #     assert len(list(output)) == 1000
    #
    # def test_batch_process_parallel_infinite(self):
    #     data = infinite_generator()
    #     output = data | ParallelBatchProcessor(add_one_batch) >> ParallelBatchProcessor(add_one_batch)
    #     assert next(output) == 3

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