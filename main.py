from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense
from keras.utils import plot_model
from testModel import testWithFileName
import pydot
import numpy
numpy.random.seed(1)
import csv

BODY_SPLITS = ["Abs / Core", "Back", "Biceps", "Cardio", "Chest", "Legs", "Olympic", "Shoulders", "Triceps"]
CLASSIFICATIONS = ["Arms", "Chest and Tri", "Chest", "Chest and Back", "Back and Bi", "Legs and Shoulders", "Shoulders and Abs", "Other"]

column1, column2 = [], []

for fileName in ['testData/testData1.csv', 'testData/testData2.csv', 'testData/testData3.csv']:
    data = csv.reader(open(fileName))
    for row in data:
        bodySplit = row[0].split('#')
        intSplit = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for split in bodySplit:
            arr = split.split(' ', 1)
            i = BODY_SPLITS.index(arr[1])
            intSplit[i] = arr[0]
        column1.append(intSplit)
        column2.append(CLASSIFICATIONS.index(row[1])/float((len(CLASSIFICATIONS)-1)))

trainingData = numpy.array(column1)
expectedOutput = numpy.array(column2)

# create model
model = Sequential()
model.add(Dense(12, input_dim = 9, kernel_initializer = 'uniform', activation = 'relu'))
model.add(Dense(12, kernel_initializer = 'uniform', activation = 'relu'))
model.add(Dense(1, kernel_initializer = 'uniform', activation = 'sigmoid'))

# Compile model
model.compile(loss = 'binary_crossentropy', optimizer = 'adam', metrics = ['accuracy'])

# Fit the model
model.fit(trainingData, expectedOutput, epochs = 100, batch_size = 5)

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

testWithFileName('testData/testData1.csv')
testWithFileName('testData/testData2.csv')
testWithFileName('testData/testData3.csv')
