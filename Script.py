# -*- coding: utf-8 -*-
"""
Created on Mon May 23 21:45:20 2016

@author: Sriram
"""
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#We are simulating for a minute

def sim_once(time = 60, n = 1000): #simulate for a minute
    '''This function takes a time period to simulate for and the number of nodes
    and returns the profit, number of successful requests, number of dropped 
    requests, and total number of requests for that simulation.
    '''
    nodeTimer = [0]*n #If the nodes are processing, how long they are going to process
    timer = 0
    requestTimeLst = []
    while True: #this will create a list of times when a single node is expected recieve a request
        timer += random .expovariate(100)#This is the time intervals between each request 
        if timer > time:
            break
        requestTimeLst.append(timer)
    totalRequests = len(requestTimeLst)
    successes = 0
    drops = 0
    for time_exp in requestTimeLst:
        nodeTimer = [0 if i < time_exp else i for i in nodeTimer] #If any of the nodes with processing time with lower than current time, we set it back to 0
        try:
            nodeAssigned = nodeTimer.index(0)
            nodeTimer[nodeAssigned] = time_exp + 2./(random.uniform(0,1)**(1./3)) #alpha = 3 and X_m = 2. In absolute terms the time take to process
            successes += 1
        except:
            drops += 1
            continue
    serverCost = n*float(2000./(30.*24*3600))*time
    profit = successes*0.01 - drops*0.1 - serverCost
    return profit, successes, drops, totalRequests


#We simulate the process many times and report the 95% CI using bootstraping

def sim_many(number = 100, time = 60, nodes = 100, bootstrapCI = True, CI = 0.95): #We repeat the above simulation a specified number of times
    '''This function repeats the simulate_once() function a specified number of 
    times and returns the 95% CI of the number of successes, profit, and requests
    via bootstrapping.
    '''    
    global allResults    
    allResults =[sim_once(time = time, n = nodes) for i in range(number)]

    def mean(S): return float(sum(x for x in S))/len(S)
    def resample(S): return [random.choice(S) for i in range(len(S))]
        
    profitValues = [x[0] for x in allResults] 
    profitValues_rs = [mean(resample(profitValues)) for i in range(len(profitValues))]
    
    successes = [float(x[1]) for x in allResults]
    requests = [float(x[3]) for x in allResults]
   
    request_success = list(np.array(successes)/np.array(requests))
    request_success_rs = [mean(resample(request_success)) for i in range(len(request_success))]

    meanSuccessRate = np.mean(request_success)
    meanProfit = np.mean(profitValues) #the is the average profit
    left_tail = int(((1.0-CI)/2)*number)
    right_tail = number-1-left_tail  
    
    if bootstrapCI: #95% CI via bootstraping
        profit_left= np.sort(profitValues_rs)[left_tail] 
        profit_right  = np.sort(profitValues_rs)[right_tail]
        request_success_left  = np.sort(request_success_rs)[left_tail] 
        request_success_right = np.sort(request_success_rs)[right_tail]
        
        return profit_left, meanProfit, profit_right, request_success_left, meanSuccessRate, request_success_right

    else:
        return meanProfit, meanSuccessRate 


#The function below is used to visualize how the the profit varies with node count

def plots_profit_success(minN = 10, maxN = 1000, iterations = 1, time = 60):
    '''This function takes values for the minimum number of servers, maximum number of 
    servers, the necessary simulation time, and the number of iterations, and returns 
    a plot showing the variation in the profit with changing number of servers and the 
    variation of the % of requests processed with the increase in the number of servers 
    used.
    '''    
    
    node_count = list(range(minN,maxN,10))
    results= []
    count = 0
    for node in node_count:
        count += 1
        results.append(sim_many(number = iterations, time = time, nodes = node))
    
    results = np.array(results)
    plt.figure()
    plt.scatter(np.array(node_count), results[:,0])
    plt.title('Processing time of %i seconds (profit earned)'%time); plt.xlabel('Number of Servers'); plt.ylabel('Profit($)')
    plt.xlim(0); plt.show()
        
    plt.figure()
    plt.scatter(np.array(node_count),100*(results[:,1]))#NOTE: dividing here or in the sim_many function itself wont make a difference if we are constructing graphs with only one iteration
    plt.title('Processing time of %i seconds (requests processed)'%time); plt.xlabel('Number of Servers'); plt.ylabel('% of requests processed')
    plt.xlim(0); plt.ylim(0);plt.show()




for time in range(10, 250, 40): #This will generate the necessary graphs for different time periods
    plots_profit_success(time = time)


#This will generate the 95% CIs via bootstrapping for a 60 seconds simulation with 345 nodes for max profit
profitMean = []
profit975 = []
profit025 = []
nodeValues = [330, 345, 355, 375, 400, 415, 425]#We will be plotting at these values

for node in nodeValues:
    results = sim_many(number = 100, time = 60, nodes = node, bootstrapCI= True)
    profitMean.append(results[1]); profit975.append(results[2]); profit025.append(results[0])

fig, ax= plt.subplots()
ax.plot(nodeValues, profitMean, color='black', label = 'Mean')
ax.plot(nodeValues, profit025, color='yellow', label = 'lower bound')  
ax.plot(nodeValues, profit975, color='green', label = 'upper bound')   
plt.xlabel('Number of servers'); plt.ylabel('Profit ($)')
plt.title('The variation of profit with nodes using 95% CI for 60s simulation')
plt.legend()

#This will generate the 95% CIs via bootstrapping for a 60 seconds simulation with 345 nodes for breakeven

profitMean = []
profit975 = []
profit025 = []
nodeValues = [250, 260, 285, 290, 300]#We will be plotting at these values

for node in nodeValues:
    results = sim_many(number = 100, time = 60, nodes = node, bootstrapCI= True)
    profitMean.append(results[1]); profit975.append(results[2]); profit025.append(results[0])

fig, ax= plt.subplots()
ax.plot(nodeValues, profitMean, color='black', label = 'Mean')
ax.plot(nodeValues, profit025, color='yellow', label = 'lower bound')  
ax.plot(nodeValues, profit975, color='green', label = 'upper bound')   
plt.xlabel('Number of servers'); plt.ylabel('Profit ($)'); plt.ylim(ymin = -60)
plt.title('The variation of profit with nodes using 95% CI for 60s simulation')
plt.legend()

#This will generate the 95% CIs via bootstrapping for a 60 seconds simulation with 275 nodes for breakeven

successMean = []
success975 = []
success025 = []
nodeValues = [250, 260, 275, 285, 290, 300]#We will be plotting at these values

for node in nodeValues:
    results = sim_many(number = 100, time = 60, nodes = node, bootstrapCI= True)
    successMean.append(results[4]); success975.append(results[5]); success025.append(results[3])

fig, ax= plt.subplots()
ax.plot(nodeValues, successMean, color='black', label = 'Mean')
ax.plot(nodeValues, success025, color='yellow', label = 'lower bound')  
ax.plot(nodeValues, success975, color='green', label = 'upper bound')   
plt.xlabel('Number of servers'); plt.ylabel('Success %')
plt.title('The variation of success rate with nodes using 95% CI for 60s simulation')
plt.legend()



###############################################
def resample(S):
    return [random.choice(S) for i in range(len(S))]

def bootstrap(x, confidence=0.68, nsamples=100):
    """Computes the bootstrap errors of the input list."""
    def mean(S): return float(sum([x for x in S]))/len(S)
    means = [mean(resample(x)) for k in range(nsamples)]
    means.sort()
    left_tail = int(((1.0-confidence)/2)*nsamples)
    right_tail = nsamples-1-left_tail
    return means[left_tail], mean(x), means[right_tail]
    

import os
os.chdir('/Users/Sriram/Desktop/DePaul/Q3/CSC521')

profitMean = []
profit975 = []
profit025 = []
nodeValues = [340, 341, 342, 343, 344, 345, 346, 347,348, 349, 350]#We will be plotting at these values

for node in nodeValues:
    results = sim_many(number = 100, time = 60, nodes = node, bootstrapCI= True)
    profitMean.append(results[1]); profit975.append(results[2]); profit025.append(results[0])

df = pd.DataFrame({'Number of Servers':nodeValues, 'Mean Profit ($)':profitMean})
df.to_csv('./maxProfit.csv')

profitMean = []
profit975 = []
profit025 = []
nodeValues = [280, 381, 382, 383, 384, 385, 386, 387,388, 389, 380]#We will be plotting at these values

for node in nodeValues:
    results = sim_many(number = 100, time = 60, nodes = node, bootstrapCI= True)
    profitMean.append(results[1]); profit975.append(results[2]); profit025.append(results[0])

df = pd.DataFrame({'Number of Servers':nodeValues, 'Mean Profit ($)':profitMean})
df.to_csv('./breakEven.csv')


successMean = []
success975 = []
success025 = []
nodeValues = [270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280]#We will be plotting at these values

for node in nodeValues:
    results = sim_many(number = 100, time = 60, nodes = node, bootstrapCI= True)
    successMean.append(results[4]); success975.append(results[5]); success025.append(results[3])

df = pd.DataFrame({'Number of Servers':nodeValues, 'Mean Profit ($)':successMean})
df.to_csv('./successRate.csv')
