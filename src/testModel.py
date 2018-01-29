
from keras.models import model_from_json
import csv
import numpy

BODY_SPLITS = ["Abs / Core", "Back", "Biceps", "Chest", "Legs", "Olympic", "Shoulders", "Triceps"]
CLASSIFICATIONS = ["Arms", "Chest and Tri", "Chest", "Chest and Back", "Back and Bi", "Back", "Shoulders", "Legs", "Other", "Full Body"]

def testWithTestFiles(fileNames, verbose):
    # load json and create model
    json_file = open('model/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights("model/model.h5")
    print("Loaded model from disk")

    total, numCorrect = 0, 0

    for fileName in fileNames:
        testingData, expectedOutput = [], []

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
                hotClassifications = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                hotClassifications[CLASSIFICATIONS.index(row[1])] = 1
                expectedOutput.append(hotClassifications)
        # calculate predictions
        predictions = model.predict(numpy.array(testingData))
        if (len(expectedOutput) > 0):
            for i in range(len(predictions)):
                pred = predictions[i].argmax(axis = 0)
                actl = expectedOutput[i].index(1)
                total += 1
                if pred == actl:
                    numCorrect += 1
                elif verbose:
                    print fileName, i+1, CLASSIFICATIONS[pred], '  --should be->  ', CLASSIFICATIONS[actl], '   certainty:', predictions[i][pred] * 100
        else:
            i = 0
            for row in csv.reader(open(fileName)):
                if verbose:
                    pred = predictions[i].argmax(axis = 0)
                    print i+1, row[0], '  --guess->  ', CLASSIFICATIONS[pred], '   certainty:', predictions[i][pred] * 100
                i += 1
    if total:
        print("*********************************************** Actual accuracy: %.2f%%" % (float(numCorrect) / total * 100))
