import numpy as np
from math import exp


def approximate_slope(func, x):
    h = 0.0001
    return 10000 * (func(x + h) - func(x))


class Node:
    def __init__(self, parent, size):
        self.parent = parent
        self.weights, self.bias = np.array([1 for _ in range(size)]), 0

    def calculate_value(self, inputs):
        return self.parent.activation_func(np.dot(self.weights, inputs) + self.bias)


class Network:
    def __init__(self, layers):
        # layers is a list of sizes of all layers, including input and output

        self.nodes = []
        for size in layers:
            layer = []
            for i in range(size):
                self.nodes.append(Node(self, len(self.nodes[-1])))

            self.nodes.append(layer)

    def predict(self, values):
        for layer in self.nodes:
            values = [node.calculate_value(values) for node in layer]

        return values

    def fit(self):  # TODO
        pass

    @staticmethod
    def activation_func(x):
        return 1 / (exp(-x) + 1)
