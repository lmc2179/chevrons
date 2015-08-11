# chevrons `>>`

Rapidly build pipelines for out-of-core data processing using higher order functions.

## Table of Contents
* [What is this?](#what-is-this)
* [Higher order Functions](#higher-order-functions)
* [Parallelism](#parallelism)
* [Implementing Your Own Pipeline Pieces](#implementing-your-own-pipeline-pieces)
* [Example: Training a Scikit learn model on synthetic data](#example-training-a-scikit-learn-model-on-synthetic-data)

#What is this?

`chevrons` is a collection of tools for building memory-efficient pipelines on iterators by composing functions. It introduces a clean syntax for passing data between functions which are composed. Data passing through each part of the pipeline is evaluated lazily, making it easy to work with very large (or infinite) streams of data in settings with limited resources.

`chevrons` is perfect for situations where you have a lot of data that you want to process out-of-core, but not enough to warrant a "big data" solution. It lets you build pipeline components that can be composed, reordered, and reused easily. The name of the package comes from the syntax of these pipelines, which looks like this:

```
output = input_data | function_1 >> function_2 >> function_3
```

This syntax makes pipelines readable and easy to understand. Similarly, subsections of the pipeline can be named and reused:

```
preprocess = function_1 >> function_2
output1 = input_data1 | preprocess >> function_3
output2 = input_data2 | preprocess >> function_4
```

The objects passed between functions are all generators/iterators, so output1 and output2 will be turned into generators which can be evaluated one element at a time (for example, written to a file or used to train a machine learning model).

You can construct your own pieces of the pipeline by writing a subclass of one of the classes in `pipeline_base`, or perform `Map`, `Fold`, and `Reduce` by importing those blocks from `pipeline_hof`.

Please note that at the moment, `chevrons` only supports Python 3 and later.

#Higher order Functions

Currently, the `Map`, `Fold` and `Reduce` functions are included as pipeline components. For a quick introduction to these functions and how they work, check out [this page](http://www.cse.unsw.edu.au/~en1000/haskell/hof.html).

Each one takes a helper function which is user defined. For example, take the following (contrived) pipeline, which sums up the square roots of all inputs which are multiples of three:

```
from chevrons.pipeline_hof import Map, Filter, Fold
import math

def is_multiple_of_three(x):
    return x % 3 == 0
    
def add(x1,x2):
    return x1+x2
    
data = range(0,10)

sum_sqrt_threes = data | Filter(is_multiple_of_three) >> Map(math.sqrt) >> Fold(add)
```

#Parallelism

*Note: Parallel processing is still in beta - while these classes are stable enough for most use cases, please report any bugs that you find.*

One advantage of structuring computation as higher-order functions is that they are extremely easy to parallelize effectively. It's easy to make pipeline elements parallel using `chevrons`! The `pipeline_parallel` module defines pipeline pieces for running things in parallel. Note that all consecutive parallel elements should begin with a `BeginParallel` block and end with an `EndParallel` block or a `FoldParallel` block. The `BeginParallel` will take a batch size, which will be used throughout the pipeline. We can rewrite the above pipeline example to utilize parallelization very easily:

```
from chevrons.pipeline_parallel import MapParallel, FilterParallel, FoldParallel, BeginParallel, EndParallel

data = range(0,10)

data | BeginParallel(5) >> FilterParallel(is_multiple_of_three) >> MapParallel(math.sqrt) >> FoldParallel(add)
```

For pipelines where the individual functions are very computationally intensive, this can lead to very significant speedups when the correct batch size is chosen.

#Implementing Your Own Pipeline Pieces

#Example: Training a Scikit learn model on synthetic data
```
import random
from chevrons.pipeline_base import Zip
from chevrons.pipeline_hof import Map
from chevrons.pipe line_extra import TrainScikitModel
from sklearn.linear_model import LinearRegression

def add_noise(data_point):
    return random.gauss(data_point, 1)

def calculate_true_value(X):
    true_slope = 0.4
    true_intercept = 1
    return true_slope*X[0] + true_intercept

X = [[i] for i in range(1000)]
model = LinearRegression()

generate_synthetic_output = Map(calculate_true_value) >> Map(add_noise)
y = X | generate_synthetic_output
(X,y) | Zip() >> TrainScikitModel(model, batch_size=100)
print(model.coef_)
```

#Contact

I'd love to hear any feedback you have, or ideas for features you think would be interesting! Send me an email at louiscialdella@gmail.com if you'd like to let me know of your happiness/displeasure/exuberance/vexation.
