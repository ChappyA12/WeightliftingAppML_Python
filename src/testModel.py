
from keras.models import model_from_json
import csv
import numpy

BODY_SPLITS = ["Abs / Core", "Back", "Biceps", "Chest", "Legs", "Olympic", "Shoulders", "Triceps"]
CLASSIFICATIONS = ["Arms", "Chest and Tri", "Chest", "Chest and Back", "Back and Bi", "Back", "Shoulders", "Legs", "Other", "Full Body"]

# load json and create model
json_file = open('model/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model/model.h5")
print("Loaded model from disk")

def testWithTestFiles(fileNames, verbose):
    total, numCorrect = 0, 0
    for fileName in fileNames:
        testingData = []
        expectedOutput = []
        for row in csv.reader(open(fileName)):
            bodySplit = row[0].split('#')
            intSplit = [0, 0, 0, 0, 0, 0, 0, 0]
            for split in bodySplit:
                arr = split.split(' ', 1)
                if arr[1] not in 'Cardio':
                    i = BODY_SPLITS.index(arr[1])
                intSplit[i] = arr[0]
            testingData.append(intSplit)
            if (len(row) > 1):
                expectedOutput.append(CLASSIFICATIONS.index(row[1])/float((len(CLASSIFICATIONS)-1)))
        # calculate predictions
        predictions = model.predict(numpy.array(testingData))
        if (len(expectedOutput) > 0):
            for i in range(len(predictions)):
                pred = int(round(predictions[i][0]*(len(CLASSIFICATIONS)-1)))
                actl = int(round(expectedOutput[i]*(len(CLASSIFICATIONS)-1)))
                total += 1
                if pred == actl:
                    numCorrect += 1
                elif verbose:
                    print i+1, CLASSIFICATIONS[pred], '  --should be->  ', CLASSIFICATIONS[actl]
        else:
            i = 0
            for row in csv.reader(open(fileName)):
                if verbose:
                    print i+1, row[0], '  --guess->  ', CLASSIFICATIONS[int(round(predictions[i][0]*(len(CLASSIFICATIONS)-1)))]
            i += 1
    if total:
        print("********************************** %s: Actual accuracy: %.2f%%" % (fileName, float(numCorrect) / total * 100))
