
import random
import StringIO
import globalData
globalData.init()

def generateTestData(fileName, num):
    with open(fileName, 'w') as f:
        for i in range(num):
            result = []
            for i in range(random.choice([1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5])):
                split = random.choice(globalData.BODY_SPLITS)
                if not contains(result, split):
                    result.append(str(random.choice([1, 1, 2, 2, 2, 3, 3, 4])) + ' ' + split)
            f.write('#'.join(result)+'\n')

def contains(list, string):
    for i in list:
        if string in i:
            return True
    return False
