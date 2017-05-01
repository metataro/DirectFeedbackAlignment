import numpy as np

from network.layer import Layer


class Optimizer(object):
    def update(self, layer: Layer, dW: np.ndarray, db: np.ndarray) -> Layer:
        pass

    def decay_learning_rate(self, factor: float) -> None:
        pass


class GDOptimizer(Optimizer):
    def __init__(self, lr: float=0.001) -> None:
        self.lr = lr

    def update(self, layer: Layer, dW: np.ndarray, db: np.ndarray) -> Layer:

        layer.W += -self.lr * dW
        layer.b += -self.lr * db

        return layer

    def decay_learning_rate(self, factor: float) -> None:
        self.lr *= factor


class GDMomentumOptimizer(Optimizer):
    def __init__(self, lr: float=0.001, mu: float=0.9) -> None:
        self.lr = lr
        self.mu = mu

    def update(self, layer: Layer, dW: np.ndarray, db: np.ndarray) -> Layer:

        if not layer.has_param('mv'):
            layer.set_param('mv', (np.zeros(dW.shape), np.zeros(db.shape)))

        v_dW, v_db = layer.get_param('mv')

        v_dW = self.mu * v_dW - self.lr * dW
        v_db = self.mu * v_db - self.lr * db

        layer.W += v_dW
        layer.b += v_db

        layer.set_param('mv', (v_dW, v_db))

        return layer

    def decay_learning_rate(self, factor: float) -> None:
        self.lr *= factor
