import math

text = open("mushroom.csv").read()
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


def entropize_or_whatever(d, calls):
    highest_avg = -1
    featureCol = 0
    for f in range(len(d[0])-1):
        if(entropy(d)-expected_entropy(d, f) >highest_avg):
            highest_avg = entropy(d)-expected_entropy(d, f)
            featureCol = f
    newSets = {}
    for row in d:
        if(row[featureCol] in newSets):
            feature = row[featureCol]
            del row[featureCol]
            newSets[feature].append(row)
        else:
            newSets[row[featureCol]] = []
            feature = row[featureCol]
            del row[featureCol]
            newSets[feature].append(row)
    print(calls +"* "+ labels[featureCol]+ "? (information gain: " + str(highest_avg) + ")")
    del labels[featureCol]
    calls += " "
    for set in newSets:
        if(entropy(newSets[set]) < 0.1):
            print(calls+"* " + set + " --> " + newSets[set][0][-1])
        elif(len(newSets[set][0]) > 1):
            print(calls +"* " + set + " (current entropy: " + str(entropy(newSets[set])) + ")")
            entropize_or_whatever(newSets[set], calls + "     ")


print("Starting entropy: " +  str(entropy(data)))
entropize_or_whatever(data, "")
