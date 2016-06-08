# -*- coding: utf-8 -*-
"""
Created on Mon May 23 21:45:20 2016

@author: Sriram
"""
import random
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
            nodeTimer[nodeAssigned] = time_exp + 2./(random.uniform(0,1)**(1./3)) #alpha = 3 and X_m = 2. In absolute terms the time take to process
            successes += 1
        except:
            drops += 1
            continue
    serverCost = n*float(2000./(30.*24*3600))*time
    profit = successes*0.01 - drops*0.1 - serverCost
    return profit, successes, drops, totalRequests



#We simulate the process many times and report the 95% CI using bootstraping

def sim_many(number = 100, time = 60, nodes = 100, bootstrapCI = False): #We repeat the above simulation a specified number of times
    '''This function repeats the simulate_once() function a specified number of 
    times and returns the 95% CI of the number of successes, profit, and requests
    via bootstrapping.
    '''    
    allResults =[sim_once(time = time, n = nodes) for i in range(number)]

    def mean(S): return float(sum(x for x in S))/len(S)
    def resample(S): return [random.choice(S) for i in xrange(len(S))]
        
    profitValues = [x[0] for x in allResults] 
    profitValues_rs = [mean(resample(profitValues)) for i in range(len(profitValues))]
    
    successes = [float(x[1]) for x in allResults]
    requests = [float(x[3]) for x in allResults]
   
    request_success = list(np.array(successes)/np.array(requests))
    request_success_rs = [mean(resample(request_success)) for i in range(len(request_success))]

    meanSuccessRate = np.mean(request_success)
    meanProfit = np.mean(profitValues) #the is the average profit
    
    if bootstrapCI: #95% CI via bootstraping
        profit_025= np.sort(profitValues_rs)[int(0.025*len(profitValues_rs))] 
        profit_975  = np.sort(profitValues_rs)[int(0.975*len(profitValues_rs))]
        request_success_025  = np.sort(request_success_rs)[int(0.025*len(request_success_rs))] 
        request_success_975 = np.sort(request_success_rs)[int(0.975*len(request_success_rs))]
        
        return profit_025, meanProfit, profit_975, request_success_025, meanSuccessRate, request_success_975

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


#This will generate the 95% CIs via bootstrapping for a 60 seconds simulation with 340 nodes. For max profit
profitMean = []
profit975 = []
profit025 = []
nodeValues = [330, 345, 380, 425, 490]#We will be plotting at these values


for node in nodeValues:
    results = sim_many(number = 100, time = 60, nodes = node, bootstrapCI= True)
    profitMean.append(results[1]); profit975.append(results[2]); profit025.append(results[0])

fig, ax= plt.subplots()
#ax.plot(nodeValues, profitMean, color='black')
ax.plot(nodeValues, profit025, color='yellow')  
ax.plot(nodeValues, profit025, color='green')   

#This will generate the 95% CIs via bootstrapping for a 60 seconds simulation with 286 nodes. For breakeven 
sim_many(number = 100, time = 60, nodes = 286, bootstrapCI = True)

#This will generate the 95% CIs via bootstrapping for a 60 seconds simulation with 275 nodes. For 90% success  
sim_many(number = 100, time = 60, nodes = 275, bootstrapCI = True)


