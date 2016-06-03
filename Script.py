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
    for time_exp in requestTimeLst:
        nodeTimer = [0 if i < time_exp else i for i in nodeTimer] #If any of the nodes with processing time with lower than current time, we set it back to 0
        try:
            nodeAssigned = nodeTimer.index(0)
            nodeTimer[nodeAssigned] = time_exp + 2/(random.uniform(0,1)**(1/3)) #alpha = 3 and X_m = 2. In absolute terms the time take to process
            successes += 1
        except:
            drops += 1
            continue
    serverCost = n*float(2000/(30.*24*3600))*time
    profit = successes*0.01 - drops*0.1 - serverCost
    return profit, successes, drops, totalRequests



#We simulate the process many times and report the 95% CI using bootstraping

def sim_many(number = 100, time = 60, n = 100): #We repeat the above simulation a specified number of times
    profitValues =[sim_once(time = time, n = n)[0] for i in range(number)]
    averageProfit = np.mean(profitValues) #the is the average profit
    errorProfit = np.std(profitValues)/np.sqrt(number) #This is the error in profit
    return n, time, averageProfit, errorProfit
    


#The function below is used to visualize how the the profit varies with node count

def profit_nodePlot(minN = 10, maxN = 1000, iterations = 1, time = 60):
    
    nodes = list(range(minN,maxN,10))
    results= []
    count = 0
    
    for node in nodes:
        count += 1
        #print(node)    
        results.append(sim_many(number = iterations, time = time, n = node))
        
    matrix = np.array(results)
    plt.figure()
    plt.scatter(matrix[:,0],matrix[:,2])
    plt.title('with %i sec'%time)

    
