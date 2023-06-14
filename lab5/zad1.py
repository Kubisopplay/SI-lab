import json
from sklearn.neural_network import MLPRegressor
import multiprocessing

file = open("jokes_ratings.json", "r")
data = json.load(file)
file.close()

from sentence_transformers import SentenceTransformer
embeddings_model = SentenceTransformer('bert-base-cased')

embeddings = {}
for i in data:
    embeddings[i] = embeddings_model.encode(data[i]["text"])

values = {}
for i in data:
    values[i] = data[i]["rating"]

default_model = MLPRegressor()

from training import train, plot
if __name__ == '__main__':
    multiprocessing.freeze_support()

large_model = MLPRegressor(hidden_layer_sizes=(1000, 1000, 1000)) #chonky boi
large_model_slow = MLPRegressor(hidden_layer_sizes=(1000, 1000, 1000), learning_rate_init=0.00001)

large_model_fast = MLPRegressor(hidden_layer_sizes=(1000, 1000, 1000),learning_rate_init=0.1)
flat_model = MLPRegressor(hidden_layer_sizes=(2500,2500))
tall_model = MLPRegressor(hidden_layer_sizes=[50 for x in range(25)])
small_model = MLPRegressor(hidden_layer_sizes=(10,10,10,10))
giant_model = MLPRegressor(hidden_layer_sizes=[2000 for x in range(4)]) # There was a point I should have stopped, but lets continue and see what happens

models = [default_model, large_model, large_model_slow, large_model_fast, flat_model, tall_model, small_model, giant_model]

processes = []

def model_tostring(model):
    return "layer size = " +  str(model.hidden_layer_sizes[0])+ " layer num = " + str(model.n_layers_) + " learning_rate = " + str(model.learning_rate_init )

#for model in models:
    model, train_err, val_err = train(model, [x for x in embeddings.values()], [x for x in values.values()], 100)
    print("Training model: " + model_tostring(model))
    plot(train_err, val_err, model_tostring(model))

model, train_err, val_err = train(large_model_slow, [x for x in embeddings.values()], [x for x in values.values()], 1000)
print(model.predict(embeddings_model.encode("What do you call a cow with no legs? Ground beef.").reshape(1, -1)))