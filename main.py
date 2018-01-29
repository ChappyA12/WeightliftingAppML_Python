import sys
sys.path.append('./src')
from buildModel import buildModelWithTrainingFiles
from testModel import testWithTestFiles
from testDataGenerator import generateTestData

buildModelWithTrainingFiles(['testData/testData1.csv', 'testData/testData2.csv', 'testData/testData3.csv', 'testData/testData4.csv'])

testWithTestFiles(['testData/testData1.csv', 'testData/testData2.csv', 'testData/testData3.csv', 'testData/testData4.csv'], True)

generateTestData('testData/tempTestData.csv', 10)
testWithTestFiles(['testData/tempTestData.csv'], True)
