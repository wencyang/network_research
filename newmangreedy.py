import networkx as nx
import heapq
from collections import namedtuple
import matplotlib.pyplot as plt

class greedyAlgorithm:

    RenameMapping = namedtuple('RenameMapping', ['integer', 'original'])

    def __init__(self, graph):

        self.rename_map = self.remap(graph)
        self.orig = graph.copy()
        self.super_graph = graph.copy()
        self.max_communities = len(graph)
        self.dendrogram = nx.Graph()
        self.pair_Q_diff_heap = []
        self.Q_history = []
        self.den_num = self.super_graph.number_of_nodes()
        num_edges=2*graph.number_of_edges()
        Q = 0.0

        for cluster_id in graph.nodes_iter():
            node_degree = graph.degree(cluster_id)
            ai = float(node_degree) / num_edges
            self.super_graph.node[cluster_id] = ai# assign ai 
            self.dendrogram.add_node(cluster_id)
            Q -= float(node_degree * node_degree) / (num_edges * num_edges) # initial Q=sum(eii-ai*ai), eii=0

        for (community_id1, community_id2) in graph.edges_iter():
            eij = 1.0 / num_edges
            self.super_graph[community_id1][community_id2] = eij
            self.super_graph[community_id2][community_id1] = eij
            
        self.reheap()
        self.run_greedy(Q)
                
        communities = self.get_communities()
        
    def remap(self, graph):
        mapping_to_int = {} #dict
        mapping_to_orig = {}
        for node_index, node in enumerate(graph.nodes_iter()):
            mapping_to_int[node]= node_index
            mapping_to_orig[node_index] = node
        return self.RenameMapping(mapping_to_int, mapping_to_orig)

    def reheap(self):#recalculate Q difference and store in heap
        del self.pair_Q_diff_heap
        self.pair_Q_diff_heap = []
        for (id1, id2) in self.super_graph.edges_iter():
            self.add_pair_to_Q_diff_heap(id1, id2)
        
    def add_pair_to_Q_diff_heap(self, id1, id2):#calculate Q difference and store in heap
        qd = self.Q_difference(id1, id2)
        if id2 < id1:
            id1, id2 = id2, id1
        heapq.heappush(self.pair_Q_diff_heap, (-qd, id1, id2))# push -qd into heap since heappop pop the smallest first
      
    def Q_difference(self, community_id1, community_id2):
        ai = float(self.super_graph.node[community_id1])
        aj = float(self.super_graph.node[community_id2])
        eij = float(self.super_graph[community_id1][community_id2])
        return 2.0*(eij - ai*aj)
        
############################################################################            
    def run_greedy(self, Q):
        self.Q_history = [Q]
        while len(self.super_graph) > 1:
            while True:
                if self.pair_Q_diff_heap:
                    qd, id1, id2 = heapq.heappop(self.pair_Q_diff_heap)
                if(self.super_graph.has_node(id1) and self.super_graph.has_node(id2)):
                    Q_diff = -qd
                    break
            if self.super_graph.number_of_edges() > 0:
                Q += Q_diff
                self.combine_communities(id1, id2)
                self.Q_history.append(Q)

    def combine_communities(self, community_id1, community_id2):
        combine_id = self.den_num+1
        self.den_num += 1
        c1_con = self.super_graph[community_id1]
        c2_con = self.super_graph[community_id2]
        c12_nodes = set(c1_con.keys()).union(set(c2_con.keys()))
        
        self.super_graph.add_node(combine_id)
        combined_degree = self.super_graph.node[community_id1] + self.super_graph.node[community_id2]
        self.super_graph.node[combine_id] = combined_degree
        for outer_node in c12_nodes:
            total = 0.0
            if(outer_node in c1_con):
                if(outer_node!=community_id2):
                   total += c1_con[outer_node]
            if(outer_node in c2_con):
                if(outer_node!=community_id1):
                   total += c2_con[outer_node]
            self.super_graph[combine_id][outer_node] = total
            self.super_graph[outer_node][combine_id] = total
            self.add_pair_to_Q_diff_heap(combine_id, outer_node)
        
        self.super_graph.remove_node(community_id1)# Remove old nodes
        self.super_graph.remove_node(community_id2)

        self.dendrogram.add_node(combine_id)# Update dendrogram
        self.dendrogram.add_edge(combine_id, community_id1)
        self.dendrogram.add_edge(combine_id, community_id2)

    def dendrogram_crawl(self, start, priors=None, max_fringe_size=None):
        if priors == None:
            priors = set()
        fringe = []

        priors.add(start)
        heapq.heappush(fringe, -start)

        while len(fringe) > 0 and (max_fringe_size == None or len(fringe) < max_fringe_size):
            node = -heapq.heappop(fringe)
            priors.add(node)
            for inode in self.dendrogram[node]:
                if inode not in priors:
                    heapq.heappush(fringe,-inode)
        return priors, fringe

    def get_communities(self, num_communities=None):
        if num_communities == None:
            index, value = max(enumerate(self.Q_history), key=lambda x: x[1])
            num_communities = len(self.Q_history) - index
        
        communities=[]
        
        nx.relabel_nodes(self.dendrogram, self.rename_map.integer, copy=False)
        start_node = max(self.dendrogram)
        priors, fringe = self.dendrogram_crawl(start=start_node, max_fringe_size=num_communities)

        for neg_clust_start in fringe:
            clust_start = -neg_clust_start
            cprior, cfringe = self.dendrogram_crawl(start=clust_start, priors=priors.copy())
            cluster_set = set(self.rename_map.original[n] for n in cprior
                                  if n <= clust_start and self.orig.has_node(n+1))
            if cluster_set:
                communities.append(cluster_set)
        nx.relabel_nodes(self.dendrogram, self.rename_map.original, copy=False)
        return sorted(communities, key=lambda c: -len(c))

#######################################################################
    def plot_Q_history(self, plot_name, out_file_name):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(range(len(self.Q_history), 0, -1), self.Q_history)
        plt.title('Number of communities vs. Modularity for %s' % plot_name)
        ax.set_xlabel('Number of communities')
        ax.set_ylabel('Modularity Score')
        plt.savefig(out_file_name)
        plt.show()

def main():
    graph = nx.read_gml('karate.gml')
    #graph=nx.karate_club_graph()
    nx.draw_networkx(graph)

    newman = greedyAlgorithm(graph)
    print newman.Q_history
    print newman.get_communities()
    newman.plot_Q_history('karate','karate')
    
if __name__ == '__main__':
    main()