import unittest
import pipeline

class Square(pipeline.PipelineFunction):
    def run(self, *args, **kwargs):
        print('Square', args[0])
        return args[0] ** 2

class AddOne(pipeline.PipelineFunction):
    def run(self, *args, **kwargs):
        print('AddOne', args[0])
        return args[0] + 1

class SyntaxTest(unittest.TestCase):
    def test_pipe(self):
        assert (2 | Square()) == 4

    def test_shift(self):
        f = Square() >> Square() >> AddOne()
        assert f(2) == 17

    def test_pipe_and_shift(self):
        assert (2 | Square() >> Square()  >> AddOne()) == 17