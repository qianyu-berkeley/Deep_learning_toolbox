import numpy as np
from deep_NN.NN_model_blocks import NN_model_blocks


class deep_NN_model(object):

    def __init__(self):

        # model parameters default values
        self.learning_rate = 0.01
        self.num_iterations = 2500
        self._config = {}
        self._seed = 1

        # object function cost tracker
        self._costs = []

        # NN model block definition
        self._nn_model_blocks = None

    def set_hyper_params(self, num_iterations, learning_rate, layer_dims):
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self._config = {"layer_dims": layer_dims,
                        "seed": self._seed}
        # "lambd": lambd,
        # "keep_prob": keep_prob}

    def L_layer_model(self, train_X, train_Y, print_cost=False):
        """
        Construct a L-layer neural network: [LINEAR->RELU]*(L-1)->LINEAR->SIGMOID.
        and train the model with given hyper-parameters

        Returns:
        parameters -- parameters learnt by the model.
        """

        # Define NN model blocks
        self._nn_model_blocks = NN_model_blocks(self._config)

        # Parameters initialization
        self._nn_model_blocks.initialize_parameters_deep()

        # Loop (gradient descent)
        for i in range(0, self.num_iterations):

            AL, caches = self._nn_model_blocks.L_model_forward(train_X)
            # Forward propagation: [LINEAR -> RELU]*(L-1) -> LINEAR -> SIGMOID.
            # if keep_prob == 1:
            #    AL, caches = self._nn_model_blocks.L_model_forward(train_X)
            # elif keep_prob < 1:
            #    AL, caches = self._nn_model_blocks.L_model_forward(train_X,
            #                                                       keep_prob)

            cost = self._nn_model_blocks.compute_cost(AL, train_Y)
            # Compute cost
            # if lambd == 0:
            #    cost = self._nn_model_blocks.compute_cost(AL, train_Y)
            # else:
            #    cost = self._nn_model_blocks.compute_cost(AL, train_Y, lambd)

            # Either user L2 or dropout not both
            #assert(lambd == 0 or keep_prob == 1)

            grads = self._nn_model_blocks.L_model_backward(AL,
                                                           train_Y,
                                                           caches)

            # Backward propagation.
            # if lambd == 0 and keep_prob == 1:
            #    grads = self._nn_model_blocks.L_model_backward(AL,
            #                                                  train_Y,
            #                                                   caches)
            # elif lambd != 0:
            #    grads = self._nn_model_blocks.L_model_backward(AL,
            #                                                   train_Y,
            #                                                   caches,
            #                                                   lambd)
            # elif keep_prob < 1:
            #    grads = self._nn_model_blocks.L_model_backward(AL,
            #                                                   train_Y,
            #                                                   caches,
            #                                                   keep_prob)

            # Update parameters.
            self._nn_model_blocks.update_parameters(grads,
                                                    self.learning_rate)

            # Print the cost every 100 training example
            if print_cost and i % 100 == 0:
                print("Cost after iteration {:d}: {:f}".format(i, cost))
            if print_cost and i % 100 == 0:
                self._costs.append(cost)

    def training_report(self):
        pass

    def predict(self, X, Y):
        """
        This function is used to predict the results of a L-layer neural network.

        Arguments:
        ----------
        X -- data set of examples you would like to label
        parameters -- parameters of the trained model

        Returns:
        ----------
        p -- predictions for the given dataset X
        """
        m = X.shape[1]
        p = np.zeros((1, m))

        # Forward propagation
        probas, caches = self._nn_model_blocks.L_model_forward(X)

        # convert probas to 0/1 predictions
        for i in range(0, probas.shape[1]):
            if probas[0, i] > 0.5:
                p[0, i] = 1
            else:
                p[0, i] = 0

        # print results
        print("Accuracy: {}".format(str(np.sum((p == Y)/m))))

        return p

    def save(self):
        # Return nn model parameter dict object
        return self._nn_model_blocks._parameters