from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense
from keras.utils import plot_model
from keras.utils import to_categorical
import pydot
import numpy
import csv
numpy.random.seed(1)

BODY_SPLITS = ["Abs / Core", "Back", "Biceps", "Chest", "Legs", "Olympic", "Shoulders", "Triceps"]
CLASSIFICATIONS = ["Arms", "Chest and Tri", "Chest", "Chest and Back", "Back and Bi", "Back", "Shoulders", "Legs", "Other", "Full Body"]
CLASSIFICATIONS_INT = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

def buildModelWithTrainingFiles(trainingFiles):
    encoded = to_categorical(numpy.array(CLASSIFICATIONS_INT))
    X, Y = [], []

    for fileName in trainingFiles:
        data = csv.reader(open(fileName))
        for row in data:
            bodySplit = row[0].split('#')
            intSplit = [0, 0, 0, 0, 0, 0, 0, 0]
            for split in bodySplit:
                arr = split.split(' ', 1)
                if arr[1] not in 'Cardio': #Ignoring Cardio due to minor role in classification determination
                    i = BODY_SPLITS.index(arr[1])
                intSplit[i] = arr[0]
            X.append(intSplit)
            hotClassifications = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            hotClassifications[CLASSIFICATIONS.index(row[1])] = 1
            Y.append(hotClassifications)

    trainingData = numpy.array(X)
    expectedOutput = numpy.array(Y)

    # create model
    model = Sequential()
    model.add(Dense(12, input_dim = 8, kernel_initializer = 'uniform', activation = 'relu'))
    model.add(Dense(12, kernel_initializer = 'uniform', activation = 'relu'))
    model.add(Dense(10, kernel_initializer = 'uniform', activation = 'sigmoid'))

    # Compile model
    model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

    # Fit the model
    model.fit(trainingData, expectedOutput, epochs = 500, batch_size = 5)

    # evaluate the model
    scores = model.evaluate(trainingData, expectedOutput)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

    # serialize model to JSON
    model_json = model.to_json()
    with open("model/model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("model/model.h5")
    plot_model(model, to_file='model/model.png', show_shapes = True, show_layer_names = True)
    print("Saved model to disk")
