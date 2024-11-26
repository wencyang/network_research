# About the repo 
This is a collection of codes and documents, mainly focus on community detection.

1. Python code about P609 computational physics at Indiana University. The topic is cellular automata spring-block model of earthquakes

2. stochastic_block_model.py is an implementation of Newman's stochastic block model with some .gml files to test. package networkx is used.

3. newmangreedy.py is an implementation of Newman's fast greedy algorithm, which can also be tested by .gml files. package networkx is used.

4. stochastic block model test.pdf is a summary of experiment results for the stochastic block model.

5. Data files

   karate.gml: classical network for a karate club

   lesmis.gml: network graph for Les Miserables
   
   netscience.gml: network graph for netscience
   
   power.gml: network graph for power grids
   

# About stochastic block model
   stochastic block model is a model for network communities (or blocks) detection.

1. You need to know the number of communities first, unlike Newman's fast greedy algorithm. You can run Newman's fast greedy algorithm several times and calculate the average value as the number of communities.

2. Once you have the number of communities, you can start the K-means-like process to move the nodes to different blocks. The idea is to maximize the
   liklihood L(G|g) = sum_over_rs{m_rs * log(m_rs/k_r*k_s)} where g is the graph(network) and G is the assignment of communities. m_rs is the number of links between block r and s and k_r and k_s is the degree of r and s
   
   References:
   
   [1] Fast algorithm for detecting community structure in networks
   
   https://journals.aps.org/pre/abstract/10.1103/PhysRevE.69.066133
   
   [2] Stochastic blockmodels and community structure in networks
   
   https://journals.aps.org/pre/abstract/10.1103/PhysRevE.83.016107

   
# About usage of the files

Free to use for any purposes. 

The .gml files are free for academic use as far as I know.
