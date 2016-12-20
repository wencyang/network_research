import networkx as nx
import math
import matplotlib.pyplot as plt
import random

class Blockmodel:

    def __init__(self, graph, K): ##K>=2
        self.K=K
        self.max_communities = len(graph)
        self.graph=graph
        self.cluster={}
        self.L_history=[]
        self.L = 0.0
        self.initial_cluster={}
        
        for node_id in graph.nodes_iter():
            group_before=(node_id+random.randint(1,100))%K #initial group of nodes into K groups '''+random.randint(1,100)'''
            group_after=group_before
            move=False
            move_number=0
            
            def group_current(group_before,group_after,move):
                if move==True:
                    return group_after
                if move==False:
                    return group_before
                
            self.cluster.update({node_id:[group_current(group_before,group_after,move), group_before,group_after,move,move_number]})
        for k, v in self.cluster.items():
            self.initial_cluster.setdefault(v[0], []).append(k)
                
        for r in range(self.K):
            for s in range(self.K):
                self.L+=self.m(r,s)*math.log(self.m(r,s)/(self.chi(r)*self.chi(s)))
        self.L_history=[self.L]
        
        print self.initial_cluster
        print self.repeat()

################plot###############
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(range(len(self.L_history)), self.L_history) 
        plt.show()
        
#########################calculation delta_L#######################################
    def m(self,r,s): #total number of edges between community r and s
        m=0.0
        for node_id in self.graph.nodes_iter():
            if self.cluster[node_id][0]==r:
                for node in self.graph[node_id]:
                    if self.cluster[node][0]==s:
                        m+=1
        return m ##twice the edges when r=s 
        
    def k(self,i,t): #edges from vetex i to vertices in group t
        k=0.0
        for node_id,group in self.cluster.items():
            if group[0]==t and node_id!=i:
                if node_id in self.graph[i].keys():
                    k+=1
        return k
    
    def k_deg(self,node_id): #degree of vertex i
        return float(self.graph.degree(node_id))
        
    def chi(self,r): #sum of m(r,s)
        chi_=0.0
        for s in range(self.K):
            chi_=chi_+self.m(r,s)
        return chi_
        
    #def u(i):
      #no self edge considered for now     
                                
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
    def max_delta_L(self):
        delta_L_list=[]
        for node_id in self.graph.nodes_iter():
            if self.cluster[node_id][3]==False:
                for s in range(self.K):
                    if s!=self.cluster[node_id][0]:
                        delta_L=self.L_difference(node_id,s)
                        delta_L_list.append((delta_L,node_id,s))
        if delta_L_list==[]:
            return []
        else:
            return max(delta_L_list)


    def run(self):
        L_history_temp=[]
        move_count=0
        #L_history_temp.append((self.L, move_count))
        while 1:
            if self.max_delta_L()==[]:
                break
            delta_L,node_id,group=self.max_delta_L()
            self.cluster[node_id][2]=group
            self.cluster[node_id][3]=True
            #self.cluster[node_id][0]=group
            self.cluster[node_id][4]=move_count
            move_count+=1
            self.L+=delta_L
            L_history_temp.append((self.L, move_count))
        self.L=max(L_history_temp)[0]
        self.L_history.append(self.L)
        move_max=max(L_history_temp)[1]
        
        for node_id in self.graph.nodes_iter():
            if self.cluster[node_id][4]<move_max:#I'm not sure why is < not <=
                self.cluster[node_id][0]=self.cluster[node_id][2]
            else:
                self.cluster[node_id][0]=self.cluster[node_id][1]
                
                
                
    def reset(self):
        for node_id in self.graph.nodes_iter():
            self.cluster[node_id][1]=self.cluster[node_id][0]
            self.cluster[node_id][2]=self.cluster[node_id][0]
            self.cluster[node_id][3]=False
            self.cluster[node_id][4]=0
    
    def repeat(self):
        new_cluster={}
        n=0
        while n<1000:
            self.run()
            self.reset()
            n+=1
        for k, v in self.cluster.items():#show the result
            new_cluster.setdefault(v[0], []).append(k)
           
        return new_cluster
#########################main##################################

        
def main():
    graph = nx.read_gml('karate.gml')
    #graph=nx.karate_club_graph()
    Blockmodel(graph,2)


    
if __name__ == '__main__':
    main()