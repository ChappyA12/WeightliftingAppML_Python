
from keras.models import model_from_json
import csv
import numpy

BODY_SPLITS = ["Abs / Core", "Back", "Biceps", "Cardio", "Chest", "Legs", "Olympic", "Shoulders", "Triceps"]
CLASSIFICATIONS = ["Arms", "Chest and Tri", "Chest", "Chest and Back", "Back and Bi", "Legs and Shoulders", "Shoulders and Abs", "Other"]

# load json and create model
json_file = open('model/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model/model.h5")
print("Loaded model from disk")

def testWithFileName(fileName):
    data = csv.reader(open(fileName))
    testingData = []
    expectedOutput = []
    for row in data:
        bodySplit = row[0].split('#')
        intSplit = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for split in bodySplit:
            arr = split.split(' ', 1)
            i = BODY_SPLITS.index(arr[1])
            intSplit[i] = arr[0]
        testingData.append(intSplit)
        if (len(row) > 1):
            expectedOutput.append(CLASSIFICATIONS.index(row[1])/float((len(CLASSIFICATIONS)-1)))
    # calculate predictions
    predictions = model.predict(numpy.array(testingData))
    if (len(expectedOutput) > 0):
        numTrue = 0
        for i in range(len(predictions)):
            pred = int(round(predictions[i][0]*(len(CLASSIFICATIONS)-1)))
            actl = int(round(expectedOutput[i]*(len(CLASSIFICATIONS)-1)))
            if pred == actl:
                numTrue = numTrue + 1
            else:
                print i+1, CLASSIFICATIONS[pred], '-->', CLASSIFICATIONS[actl]
        print("********************************** %s: Actual accuracy: %.2f%%" % (fileName, float(numTrue) / len(predictions) * 100))
    else:
        for i in range(len(predictions)):
            print i+1, CLASSIFICATIONS[int(round(predictions[i][0]*(len(CLASSIFICATIONS)-1)))]
