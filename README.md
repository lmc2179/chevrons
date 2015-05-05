# chevrons `>>`

[![travis](https://travis-ci.org/lmc2179/chevrons.svg?branch=master)](https://travis-ci.org/lmc2179/chevrons)



Rapidly build pipelines for out-of-core data processing using higher order functions.

`chevrons` is a collection of tools for building memory-efficient pipelines on iterators by composing functions. It introduces a clean syntax for passing data between functions which are composed.

More documentation to come! This is still a very new project.

Please note that at the moment, `chevrons` only supports Python 3 and later.

```
# Example: Training a Scikit learn model on synthetic data
import random
from pipeline_base import Merge
from pipeline_hof import Map
from pipeline_extra import TrainScikitModel
from sklearn.linear_model import LinearRegression

def add_noise(data_point):
    return random.gauss(data_point, 1)

def calculate_true_value(X):
    true_slope = 0.4
    true_intercept = 1
    return true_slope*X[0] + true_intercept

X = [[i] for i in range(1000)]
model = LinearRegression()

generate_synthetic_data = Map(calculate_true_value) >> Map(add_noise) >> Merge(X)
X | generate_synthetic_data >> TrainScikitModel(model, batch_size=100)
```
