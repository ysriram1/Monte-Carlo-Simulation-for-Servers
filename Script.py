# -*- coding: utf-8 -*-
"""
Created on Mon May 23 21:45:20 2016

@author: Sriram
"""
import random
import numpy as np
import matplotlib.pyplot as plt
from nlib import MCEngine
#We are simulating for a minute

def sim_once(time = 60, n = 1000): #simulate for a minute
    node_state = [True]*n #Wether or not the nodes are ready to process request
    nodeTimer = [0]*n #If the nodes are processing, how long they are going to process
    timer = 0
    requestTimeLst = []
    while True: #this will create a list of times when a single node is expected recieve a request
        timer += random.expovariate(100)#This is the time intervals between each request 
        if timer > time:
            break
        requestTimeLst.append(timer)
    totalRequests = len(requestTimeLst)
    successes = 0
    drops = 0
    for time in requestTimeLst:
        nodeTimer = [0 if i < time else i for i in nodeTimer] #If any of the nodes with processing time with lower than current time, we set it back to 0
        node_state = [True if i == 0 else False for i in nodeTimer] #for such nodes, we set their state as True again
        try:
            nodeAssigned = node_state.index(True)
            nodeTimer[nodeAssigned] = time + 2/(random.uniform(0,1)**(1/3)) #alpha = 3 and X_m = 2. In absolute terms the time take to process
            node_state[nodeAssigned] = False #set the state of that node to false
            successes += 1
        except:
            drops += 1
            continue
    serverCost = n*float(2000/(30*24*3600))*time
    profit = successes*0.01 - drops*0.1 - serverCost
    return profit, successes, drops, totalRequests
    
def sim_many(number = 100, time = 60, n = 100): #We repeat the above simulation a specified number of times
    profitValues =[sim_once(time = time, n = n)[0] for i in range(number)]
    averageProfit = np.mean(profitValues) #the is the average profit
    errorProfit = np.std(profitValues)/np.sqrt(number) #This is the error in profit
    return n, time, averageProfit, errorProfit
    


##The code below is to visualize how the the profit varies with node count

nodes = list(range(0,1000,10))

results= []
count = 0

for node in nodes:
    count += 1
    #print(node)    
    results.append(sim_once(time = 60, n = node))
    
matrix = np.array(results)
plt.figure()
plt.scatter(matrix[:,0],matrix[:,2])
plt.title('with 60 sec')
#plt.ylim(ymin = 0); plt.xlim(xmin=600, xmax=700)

#from scipy.interpolate import spline
#xnew = np.linspace(matrix[:,0].min(), matrix[:,0].max())
#smoother = spline(matrix[:,0], matrix[:,2],xnew)
#plt.plot(xnew,smoother)
#plt.show()
    
