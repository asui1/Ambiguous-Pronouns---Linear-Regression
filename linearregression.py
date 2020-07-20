import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import csv
from sklearn.preprocessing import StandardScaler

def cost_function(X, Y, B):
    m = len(Y)
    J = np.sum((X.dot(B) - Y) ** 2)/(2 * m)
    return J
def batch_gradient_descent(X, Y, B, alpha, iterations):
    cost_history = [0] * iterations
    m = len(Y)
 
    for iteration in range(iterations):
    #print(iteration)
    # Hypothesis Values
        h = X.dot(B)
    # Difference b/w Hypothesis and Actual Y
        loss = h - Y
    # Gradient Calculation
        gradient = X.T.dot(loss) / m
    # Changing Values of B using Gradient
        B = B - alpha * gradient
    # New Cost Value
        cost = cost_function(X, Y, B)
        cost_history[iteration] = cost
    return B, cost_history

def mergex(data):
    ret = []
    for i in range(0, len(data), 2):
        cur = data[i]
        cur.extend(data[i+1])
        ret.append(cur)
    return ret
def mergey(data):
    ret = []
    for i in range(0, len(data), 2):
        first = data[i]
        second = data[i+1]
        if first==0 and second == 0:
            ret.append(1)
        if first == 1 and second == 0:
            ret.append(0)
        else:
            ret.append(-1)
    return ret


data = []
y = []
names = []
g = open('snippet.csv', 'r', newline = '')
read = csv.reader(g)

for row in read:
    nums = row[:-1]
    temp_data = [int(x) for x in nums]
    data.append(temp_data[0:5])
    y.append(temp_data[5])
    names.append(row[6])

g.close()


data = mergex(data)
y = mergey(y)
print(data[0])
print(y[:5])
sc = StandardScaler()
X = sc.fit_transform(data)
print(X)
m = 2000
f = 10
X_train = X[:m,:f]
X_train = np.c_[np.ones(len(X_train),dtype='int64'),X_train]
y_train = y[:m]
X_test = X[m:,:f]
X_test = np.c_[np.ones(len(X_test),dtype='int64'),X_test]
y_test = np.array(y[m:])
B = np.zeros(X_train.shape[1])
alpha = 0.0001
iter_ = 10000
newB, cost_history = batch_gradient_descent(X_train, y_train, B, alpha, iter_)
print("new B is ")

print(newB)

        

def find_match(newB, testX, Y):
    print(len(testX))
    print(len(Y))
    match = 0
    mismatch = 0
    tt = 0
    tf = 0
    ff = 0
    ran = 0.1
    for i in range(len(testX)):
        val = 0
        for j in range(len(testX[i])):
            val += newB[j]*testX[i][j]
        if val > ran and Y[i] == 1:
            match += 1
            tt += 1
        elif val < -ran and Y[i] == -1:
            match += 1
            tf += 1
        elif val >= -ran and val <= ran and Y[i] == 0:
            match += 1
            ff += 1
        else:
            mismatch += 1
            
    return match, mismatch, tt, tf, ff


print(find_match(newB, X[:m], y[:m]))

print(find_match(newB, X[m:4000], y[m:4000]))

print(find_match(newB, X[4000:], y[4000:]))
