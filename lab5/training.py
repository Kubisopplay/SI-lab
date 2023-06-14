from sklearn.neural_network import MLPRegressor
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def train(model, embeddings, data, epochs):
    train_em,  val_em, train_data, val_data = train_test_split(embeddings, data, test_size=0.2, random_state=2137)
    train_err = []
    val_err = []
    for i in range(epochs):
        model.partial_fit(train_em, train_data)

        train_err.append(mean_squared_error(model.predict(train_em), train_data))
        val_err.append(mean_squared_error(model.predict(val_em), val_data))

    #plot(train_err, val_err, "layer size = " +  str(model.hidden_layer_sizes[0])+ " layer num = " + str(model.n_layers_) + " learning_rate = " + str(model.learning_rate_init ))
    return model, train_err, val_err

def plot(train_err, val_err, name=""):

    plt.plot(train_err, label="train")
    plt.plot(val_err, label="validation")
    plt.ylabel("mean squared error")
    plt.xlabel("epoch")
    plt.legend()
    plt.title(name)
    plt.savefig(name+".png")
    #plt.show()
    plt.clf()