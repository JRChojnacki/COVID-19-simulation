# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 19:08:34 2020

@author: Janek
"""

import random as rd
from pylab import *
import networkx as nx
import imageio
def initialize():
    global g, nextg
    p=2*M/(N*(N-1))
    g = nx.barabasi_albert_graph(N,M)
    DisconnectedIndex=[]
    for i in g.nodes:
        if g.degree[i]==0:
            DisconnectedIndex.append(i)
    g.remove_nodes_from(DisconnectedIndex)
    for i in g.nodes:
        if random() < 0.01:
            g.nodes[i]['state'] = 1 
            g.nodes[i]['color'] ='red'
            g.nodes[i]['infection_time']= 0
        else: 
            g.nodes[i]['state'] = 0 
            g.nodes[i]['color'] ='blue'
            g.nodes[i]['infection_time']= 0
    nextg = g.copy()
    
def observe():
    global g, nextg
    cla()
    nx.draw(g, 
    cmap = cm.binary,
    node_color = [g.nodes[i]['color'] for i in g.nodes],
    edgecolors='black',
    edgewidth=0.1,
    pos=dic,
    node_size=40,
    width=0.05,
    alpha=0.9)
    plt.title('Albert-Barabasi network simulation of the population N=2000,\n implementing social distancing and overpopulated\n hospitals',fontsize=10)
def plotting():
    global T,H,I,R,D
    cla()
    plt.plot(T, H,label='susceptible',color='blue') 
    plt.plot(T, I,label='infected',color='red') 
    plt.plot(T, R,label='recovered',color='green') 
    plt.plot(T, D,label='dead',color='black') 
    plt.xlabel('Time', fontsize=20)
    plt.ylabel('Affected part of  the population', fontsize=10)
    plt.ylim(0,1)
    plt.title('Evolution of the number of cases', fontsize=10)
    plt.grid(True)
def update():
    global g, nextg
    for i in g.nodes:
        if g.nodes[i]['state']==1:
            for j in g.neighbors(i):
                   if g.nodes[j]['color'] !='green' and g.nodes[j]['color'] !='black':
                       a=rand()
                       if a<p_i:
                           nextg.nodes[j]['state']=1    #infection of the neighbour
                           nextg.nodes[j]['color'] ='red'
        if g.nodes[i]['state']==1: #choosing infected part of population
            nextg.nodes[i]['infection_time']+=1            
            p=0
            n=1
            for j in g.neighbors(i):
                n+=j
                if g.nodes[j]['state'] ==1:
                    p+=1
            p=p/n
            if g.nodes[i]['infection_time']==t_r:
                nextg.nodes[i]['state']= 0
                nextg.nodes[i]['color'] ='green'
            elif random()<p+p_d and g.nodes[i]['infection_time']>=t_death:
                nextg.nodes[i]['state']=0
                nextg.nodes[i]['color'] ='black'
                cut=[]
                for j in g.neighbors(i):
                    cut.append(j)
                for j in cut:
                    nextg.remove_edge(i,j)
                
            if g.nodes[i]['infection_time']>=t_d:
                severing_neighbors=[]
                for j in g.neighbors(i):
                    if g.nodes[j]['state'] ==0 and random()<p_s:
                        severing_neighbors.append(j)
                for j in severing_neighbors:
                    nextg.remove_edge(i,j)
    g =  nextg
p_i=0.03    # infection probability
p_s=0.4   #social connection severance probability, after the detection
p_d=4512/68128  #Hubei mortality rate
N=2000       #population
M=3       #averge number of attached edges to the new nodes duting the initialization()
t_r=20     #recovery time
t_d=5      #detection time
t_death=14  #minimal time from sympthoms to death
TimeStep=0
H=[]
I=[]
R=[]
T=[]
D=[]
initialize()
ListOfGraphNames=[]
ListOfPlotNames=[]
GraphImages = []
PlotImages=[]
p=nx.random_layout(g)
dic=nx.random_layout(g,)
#for i in p:
#    p[i]=tuple(p[i])

for i in range(5000):
    infected=0
    healthy=0
    dead=0
    for j in g.nodes:
        infected+=g.nodes[j]['state']
        if g.nodes[j]['color']=='blue': healthy+=1 
        if g.nodes[j]['color']=='black': dead+=1 
    recovered=N-infected-healthy-dead
    T.append(TimeStep)
    I.append(infected/N)
    H.append(healthy/N)
    R.append(recovered/N)
    D.append(dead/N)
    plt.subplot(211)
    observe()
    plt.subplot(212)
    plotting()
    plt.legend(loc='center right')
    plt.savefig("graphcombined" + str(i).zfill(3) + ".png")
    plt.close()
    ListOfGraphNames.append(("graphcombined" + str(i).zfill(3) + ".png"))
    if infected==0:
        break
    for j in range(1):
        update()
        TimeStep+=1
    print(TimeStep)
for filename in ListOfGraphNames:
    GraphImages.append(imageio.imread(filename))
imageio.mimsave('C:/Users/Janek/Desktop/ComputerModeling/network/Covid-19/deaths2OverwhelmedHospitals.gif', GraphImages,duration=0.2)
