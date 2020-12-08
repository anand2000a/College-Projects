from abc import ABCMeta, abstractmethod
import numpy as np
import cv2


class Model:
    __metaclass__ = ABCMeta

    nParams = 0

    # returns the residual vector with the given model parameters, input vector and expected output vector
    def residual(self, params, x, y):
        r = y - self.fun(x, params)
        r = r.flatten()

        return r

    # returns the values ​​returned by the model with the given parameters and the input vector
    @abstractmethod
    def fun(self, x, params):
        pass

    # Jacobian returns
    @abstractmethod
    def jacobian(self, params, x, y):
        pass

    # returns a set of sample model parameters
    @abstractmethod
    def getExampleParameters(self):
        pass

    # returns another set of sample parameters
    @abstractmethod
    def getInitialParameters(self):
        pass


class OrthographicProjectionBlendshapes(Model):
    nParams = 6

    def __init__(self, nBlendshapes):
        self.nBlendshapes = nBlendshapes
        self.nParams += nBlendshapes

    def fun(self, x, params):
        # scaling
        s = params[0]
        # rotation
        r = params[1:4]
        #displacement (translation)
        t = params[4:6]
        w = params[6:]

        mean3DShape = x[0]
        blendshapes = x[1]

        # rotation matrix from rotation vector, Rodrigues formula
        R = cv2.Rodrigues(r)[0]
        P = R[:2]
        shape3D = mean3DShape + \
            np.sum(w[:, np.newaxis, np.newaxis] * blendshapes, axis=0)

        projected = s * np.dot(P, shape3D) + t[:, np.newaxis]

        return projected

    def jacobian(self, params, x, y):
        s = params[0]
        r = params[1:4]
        t = params[4:6]
        w = params[6:]

        mean3DShape = x[0]
        blendshapes = x[1]

        R = cv2.Rodrigues(r)[0]
        P = R[:2]
        shape3D = mean3DShape + \
            np.sum(w[:, np.newaxis, np.newaxis] * blendshapes, axis=0)

        nPoints = mean3DShape.shape[1]

        # nSamples * 2 because each point has two dimensions (x and y)
        jacobian = np.zeros((nPoints * 2, self.nParams))

        jacobian[:, 0] = np.dot(P, shape3D).flatten()

        stepSize = 10e-4
        step = np.zeros(self.nParams)
        step[1] = stepSize
        jacobian[:, 1] = ((self.fun(x, params + step) -
                           self.fun(x, params)) / stepSize).flatten()
        step = np.zeros(self.nParams)
        step[2] = stepSize
        jacobian[:, 2] = ((self.fun(x, params + step) -
                           self.fun(x, params)) / stepSize).flatten()
        step = np.zeros(self.nParams)
        step[3] = stepSize
        jacobian[:, 3] = ((self.fun(x, params + step) -
                           self.fun(x, params)) / stepSize).flatten()

        jacobian[:nPoints, 4] = 1
        jacobian[nPoints:, 5] = 1

        startIdx = self.nParams - self.nBlendshapes
        for i in range(self.nBlendshapes):
            jacobian[:, i + startIdx] = s * np.dot(P, blendshapes[i]).flatten()

        return jacobian

    # unused
    def getExampleParameters(self):
        params = np.zeros(self.nParams)
        params[0] = 1

        return params

    def getInitialParameters(self, x, y):
        mean3DShape = x.T
        shape2D = y.T

        shape3DCentered = mean3DShape - np.mean(mean3DShape, axis=0)
        shape2DCentered = shape2D - np.mean(shape2D, axis=0)

        scale = np.linalg.norm(shape2DCentered) / \
            np.linalg.norm(shape3DCentered[:, :2])
        t = np.mean(shape2D, axis=0) - np.mean(mean3DShape[:, :2], axis=0)

        params = np.zeros(self.nParams)
        params[0] = scale
        params[4] = t[0]
        params[5] = t[1]

        return params
