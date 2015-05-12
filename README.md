# chevrons `>>`

Rapidly build pipelines for out-of-core data processing using higher order functions.

**More documentation to come! This is still a very new project.**

## Table of Contents
* [What is this?](#what-is-this)
* [Building Pipelines with Chevrons](#building-pipelines-with-chevrons)
* [Higher order Functions](#higher-order-functions)
* [Parallelism](#parallelism)

#What is this?

`chevrons` is a collection of tools for building memory-efficient pipelines on iterators by composing functions. It introduces a clean syntax for passing data between functions which are composed.

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

#Building Pipelines with Chevrons

#Higher order Functions

#Parallelism

#Example: Training a Scikit learn model on synthetic data
```
import random
from chevrons.pipeline_base import Zip
from chevrons.pipeline_hof import Map
from chevrons.pipeline_extra import TrainScikitModel
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

###Future updates planned:
* Seamless paralellization of higher order function blocks
* More blocks for Machine Learning and Data processing

#Contact

I'd love to hear any feedback you have, or ideas for features you think would be interesting! Send me an email at louiscialdella@gmail.com if you'd like to let me know of your happiness/displeasure/exuberance/vexation.
