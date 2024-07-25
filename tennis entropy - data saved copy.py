import math

text = open("play_tennis.csv").read()

lines = text.split("\n")

labels = lines[0].split(",")
data = []
for i in range(1, len(lines)):
    data.append(lines[i].split(","))



def possible_vals(d):
    vals = {}
    for i in d:
        if(i[-1] in vals):
            vals[i[-1]] += 1
        else:
            vals[i[-1]] = 1
    return vals
def entropy(d):
    values = possible_vals(d)
    e = 0
    for i in values:
        e += values[i]/len(d) *(-math.log2(values[i]/len(d)))
    return e

def expected_entropy(d, c):
    newSets = {}
    for r in d:
        if(r[c] in newSets):
            newSets[r[c]].append(r)
        else:
            newSets[r[c]] = []
            newSets[r[c]].append(r)
    avg = 0
    for i in newSets:
        avg+= entropy(newSets[i]) * (len(newSets[i])/len(d))
    return avg
def filter_data(d, feature, featureIndex):
    newList = []
    for point in d:
        if(point[featureIndex] == feature):
            newList.append(point)
    return newList

def entropize_or_whatever(d):
    if(entropy(d) == 0):
        return (d[0][-1],)
    highest_avg = -1
    featureCol = 0
    for f in range(len(d[0])-1):
        if(entropy(d)-expected_entropy(d, f) >highest_avg):
            highest_avg = entropy(d)-expected_entropy(d, f)
            featureCol = f
    pos_values = set()
    for row in d:
        pos_values.add(row[featureCol]) 
    newDict = {}
    for val in pos_values:    
        newDict[val] = entropize_or_whatever(filter_data(d, val, featureCol))
    return (featureCol, newDict)

print("Starting entropy: " +  str(entropy(data)))
print(entropize_or_whatever(data))
