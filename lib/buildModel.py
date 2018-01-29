from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense
from keras.utils import plot_model
from keras.utils import to_categorical
import pydot
import csv
import numpy
numpy.random.seed(1)
import globalData
globalData.init()


def buildModelWithTrainingFiles(trainingFiles):
    X, Y = [], []

    for fileName in trainingFiles:
        data = csv.reader(open(fileName))
        for row in data:
            bodySplit = row[0].split('#')
            intSplit = [0] * len(globalData.BODY_SPLITS)
            for split in bodySplit:
                arr = split.split(' ', 1)
                if arr[1] not in 'Cardio': #Ignoring Cardio due to minor role in classification determination
                    i = globalData.BODY_SPLITS.index(arr[1])
                intSplit[i] = arr[0]
            X.append(intSplit)
            hotClassifications = [0] * len(globalData.CLASSIFICATIONS)
            hotClassifications[globalData.CLASSIFICATIONS.index(row[1])] = 1
            Y.append(hotClassifications)

    trainingData = numpy.array(X)
    expectedOutput = numpy.array(Y)

    print 'Training data count:', len(X)

    # create model
    model = Sequential()
    model.add(Dense(12, input_dim = 8, kernel_initializer = 'uniform', activation = 'relu'))
    model.add(Dense(12, kernel_initializer = 'uniform', activation = 'relu'))
    model.add(Dense(10, kernel_initializer = 'uniform', activation = 'sigmoid'))

    # Compile model
    model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

    # Fit the model
    model.fit(trainingData, expectedOutput, epochs = 2500, batch_size = 5)

    # evaluate the model
    scores = model.evaluate(trainingData, expectedOutput)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

    # serialize model to JSON
    model_json = model.to_json()
    with open("src/model.json", "w") as json_file:
        json_file.write(model_json)
    model.save_weights("src/model.h5")
    plot_model(model, to_file='src/model.png', show_shapes = True, show_layer_names = True)
    print("Saved model to disk")
