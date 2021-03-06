import numpy as np


class Loss(object):
    def calculate(self, x: np.ndarray, y: np.ndarray) -> tuple:
        pass


class SoftmaxCrossEntropyLoss(Loss):
    def calculate(self, x: np.ndarray, y: np.ndarray) -> tuple:
        n = x.shape[0]

        # threshold = 30
        # abs_x = np.abs(x)
        # larget_than_threshold = (abs_x > threshold)
        # x *= (np.abs(larget_than_threshold - 1)) + (larget_than_threshold * threshold / abs_x)

        # print("min: {}, max: {}".format(np.min(x), np.max(x)))

        exp = np.exp(x)
        probs = exp / np.sum(exp, axis=1, keepdims=True)
        correct_logprobs = -np.log(probs[range(n), y])
        loss = np.sum(correct_logprobs) / n
        delta = probs
        delta[range(n), y] -= 1
        delta /= float(n)
        return loss, delta