import unittest
import datetime
from pipeline_base import MapParallel
from pipeline_hof import Map
from pipeline_parallel import MapParallel


def time_consuming_function(x):
    "A costly function which takes a float and returns the same float. Used for testing efficiency of parallelism."
    return float(str(float(str(float(str(float(str(x))))))))

class PerformanceTest(unittest.TestCase):
    def test_map_parallel_speed(self):
        test_data_size = 1000000
        data1,data2 = range(test_data_size),range(test_data_size)
        begin = datetime.datetime.now()
        output = data1 | Map(time_consuming_function)
        list(output)
        single_thread_time = datetime.datetime.now() - begin
        begin = datetime.datetime.now()
        output = data1 | MapParallel(time_consuming_function, n_processes=None, batch_size=10000)
        list(output)
        multi_thread_time = datetime.datetime.now() - begin
        print(multi_thread_time, single_thread_time)
        assert multi_thread_time < single_thread_time
