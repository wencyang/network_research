import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import networkx as nx
import math
import matplotlib.pyplot as plt
import random
#import numpy as np

class Blockmodel:

    def __init__(self, graph, K,name): ##K>=2
        self.K=K
        #self.max_communities = len(graph)
        self.graph=graph
        self.cluster={}
        self.modified_cluster={}
        self.L_history=[]
        self.L = 0.0
        self.initial_cluster={}
        self.new_cluster={}
        
        for node_id in graph.nodes_iter():
            if node_id<self.K+1:
                group_before=node_id
            group_before=random.randint(0,K-1)#(node_id+random.randint(1,100))%K #initial group of nodes into K groups '''+random.randint(1,100)'''
            group_after=group_before
            move_number=0
                
            self.cluster.update({node_id:[group_before, group_before,group_after,move_number]})
            self.modify_cluster()
            
        for k, v in self.cluster.items():
            self.initial_cluster.setdefault(v[0], []).append(k)
                
        for r in range(self.K):
            for s in range(self.K):
                self.L+=self.m(r,s)*self.c(self.m(r,s)/(self.chi(r)*self.chi(s)))  #initial L
        self.L_history=[self.L]
        
        self.repeat()
        
######################write out############################
        filename='%s_cluster_blockmodel.txt'%name
        target=open(filename,'w')
        target.write('initial')
        target.write('\n')
        target.write('%s'%self.initial_cluster)
        target.write('\n')
        target.write('after')
        target.write('\n')
        target.write('%s'%self.modified_cluster)
        target.close()

##################################plot############################################
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(range(len(self.L_history)), self.L_history) 
        figurename='%s_cluster_blockmodel.png'%name
        plt.savefig(figurename)
        
#########################calculation delta_L#######################################
    def modify_cluster(self):
        self.modified_cluster={}
        for k, v in self.cluster.items():
            self.modified_cluster.setdefault(v[0], []).append(k)
            
    def m(self,r,s): #total number of edges between community r and s
        m=0.0

        for node_id in self.modified_cluster[r]:
            for node in self.graph[node_id]:
                if self.cluster[node][0]==s:
                    m+=1
                    #m=m+graph.number_of_edges(node,node_id) for multigraph
        return m ##twice the edges when r=s 
        
    def k(self,i,t): #edges from vetex i to vertices in group t
        k=0.0
        for node_id in self.modified_cluster[t]:
            if node_id in self.graph[i].keys():
                k+=1
                #K=K+graph.number_of_edges(i,node_id) for multigraph
        return k
    
    def k_deg(self,node_id): #degree of vertex i
        return float(self.graph.degree(node_id))
        
    def chi(self,r): #sum of m(r,s)
        chi_=0.0
        for s in range(self.K):
            chi_=chi_+self.m(r,s)
        return chi_
        
    def u(self,i): # don't add this to delta_L calculation for now
        self_edge_list=self.graph.selfloop_edges() 
        if (i,i) in self_edge_list:
            return self_edge_list.count((i,i))
                                
    def a(self,x):
        if x==0:
            return 0.0
        if x>0:
            return 2*x*math.log(x)
        if x<0:
            return 'wrong' 
    
    def b(self,x):
        if x==0:
            return 0.0
        if x>0:
            return x*math.log(x)
        if x<0:
            return 'Wrong'
            
    def c(self,x):
        if x==0:
            return 0.0
        if x>0:
            return math.log(x)
        if x<0:
            return 'Wrong'  
                     
    def L_difference(self, i, s):
        r=self.cluster[i][0]
        delta_L=0.0
        delta_L_t_sum=0.0
        if r==s:
            delta_L=0
        else:
            for t in range(self.K):
                if t!=r and t!=s:
                    delta_L_t=self.a(self.m(r,t)-self.k(i,t))-self.a(self.m(r,t))+self.a(self.m(s,t)+self.k(i,t))-self.a(self.m(s,t))
                    delta_L_t_sum=delta_L_t_sum+delta_L_t
                
            delta_L=delta_L_t_sum+self.a(self.m(r,s)+self.k(i,r)-self.k(i,s))\
            -self.a(self.m(r,s))+self.b(self.m(r,r)-2*(self.k(i,r)))-self.b(self.m(r,r))+self.b(self.m(s,s)+2*(self.k(i,s)))-self.b(self.m(s,s))\
            -self.a(self.chi(r)-self.k_deg(i))+self.a(self.chi(r))-self.a(self.chi(s)+self.k_deg(i))+self.a(self.chi(s))
        
        return delta_L
########################iteration#######################################            
    def delta_L_list(self):
        delta_L_list=[]
        for node_id in self.graph.nodes_iter():
            for s in range(self.K):
                    if s!=self.cluster[node_id][0]:
                        delta_L=self.L_difference(node_id,s)
                        delta_L_list.append((delta_L,node_id,s))
        delta_L_list.sort()
        return delta_L_list


    def run(self):
        L_history_temp=[]
        move_count=0
        #L_history_temp.append((self.L, move_count))
        delta_L_list2=self.delta_L_list()
        while 1:
            if delta_L_list2==[]:
                break
            delta_L,node_id,group=delta_L_list2.pop()
            self.cluster[node_id][2]=group
            self.cluster[node_id][3]=move_count
            #self.cluster[node_id][0]=group
            #self.cluster[node_id][4]=move_count
            move_count+=1
            self.L+=delta_L
            L_history_temp.append((self.L, move_count))
        self.L=max(L_history_temp)[0]
        self.L_history.append(self.L)
        move_max=max(L_history_temp)[1]
        
        for node_id in self.graph.nodes_iter():
            if self.cluster[node_id][3]<move_max:#I'm not sure why is < not <=, but it works
                self.cluster[node_id][0]=self.cluster[node_id][2]
            else:
                self.cluster[node_id][0]=self.cluster[node_id][1]
                
        
                
    def reset(self):
        for node_id in self.graph.nodes_iter():
            self.cluster[node_id][1]=self.cluster[node_id][0]
            self.cluster[node_id][2]=self.cluster[node_id][0]
            self.cluster[node_id][3]=0
            #self.cluster[node_id][4]=0
            self.modify_cluster()
    
    def repeat(self):
        n=0
        while n<20:
            self.run()
            self.reset()
            n+=1

        
def main():
    name='karate'
    group_number=2 # here set the group number
    name1='%s.gml'%name
    graph = nx.read_gml(name1)
    #graph=nx.karate_club_graph()
    Blockmodel(graph,group_number,name)


    
if __name__ == '__main__':
    main()
