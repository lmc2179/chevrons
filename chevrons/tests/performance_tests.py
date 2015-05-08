import unittest
import datetime
from pipeline_parallel import MapParallel, BeginParallel, FilterParallel, EndParallel, FoldParallel
from pipeline_hof import Map, Filter, Fold

def time_consuming_function(x):
    "A costly function which takes a float and returns the same float. Used for testing efficiency of parallelism."
    return float(str(float(str(float(str(float(str(float(str(float(str(float(str(float(str(x))))))))))))))))

def add_slow(x1,x2):
    return time_consuming_function(x1) + time_consuming_function(x2)

def is_even_slow(x):
    return time_consuming_function(x) % 2 == 0

def is_multiple_three_slow(x):
    return time_consuming_function(x) % 3 == 0

class PerformanceTest(unittest.TestCase):
    def eval_parallel_speed(self, data1,data2,pipeline_single, pipeline_multi, final_type=list):
        begin = datetime.datetime.now()
        output = data1 | pipeline_single
        final_type(output)
        single_thread_time = datetime.datetime.now() - begin
        begin = datetime.datetime.now()
        output = data2 | pipeline_multi
        final_type(output)
        multi_thread_time = datetime.datetime.now() - begin
        print('MULTITHREAD, SINGLETHREAD')
        print(multi_thread_time, single_thread_time)
        assert multi_thread_time < single_thread_time

    def test_map_parallel_speed(self):
        print('MAP TEST: ')
        test_data_size = 1000000
        data1,data2 = range(test_data_size),range(test_data_size)
        pipeline_single = Map(time_consuming_function) >> Map(time_consuming_function)
        pipeline_multi = BeginParallel(5000) >> MapParallel(time_consuming_function) >> MapParallel(time_consuming_function) >> EndParallel()
        self.eval_parallel_speed(data1, data2, pipeline_single, pipeline_multi)

    def test_filter_parallel_speed(self):
        print('FILTER TEST: ')
        test_data_size = 1000000
        data1,data2 = range(test_data_size),range(test_data_size)
        pipeline_single = Filter(is_even_slow) >>  Filter(is_multiple_three_slow)
        pipeline_multi = BeginParallel(5000) >> FilterParallel(is_even_slow) >>  FilterParallel(is_multiple_three_slow) >> EndParallel()
        self.eval_parallel_speed(data1, data2, pipeline_single, pipeline_multi)

    def test_combined_parallel_speed(self):
        print('COMBINED TEST: ')
        test_data_size = 1000000
        data1,data2 = range(test_data_size),range(test_data_size)
        pipeline_single = Filter(is_even_slow) >>  Filter(is_multiple_three_slow) >> Fold(add_slow)
        pipeline_multi = BeginParallel(5000) >> FilterParallel(is_even_slow) >>  \
                         FilterParallel(is_multiple_three_slow) >> FoldParallel(add_slow) >> EndParallel()
        self.eval_parallel_speed(data1, data2, pipeline_single, pipeline_multi, lambda x:x)

