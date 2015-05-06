# Example: Training a Scikit learn model on synthetic data
import random
from pipeline_base import Zip
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

generate_synthetic_output = Map(calculate_true_value) >> Map(add_noise)
y = X | generate_synthetic_output
(X,y) | Zip() >> TrainScikitModel(model, batch_size=100)
print(model.coef_)