# some small projects
1. Here I put some python code about my P609 computational physics class assignment.

2. stochastic_block_model.py is an implementation of Newman's stochastic block model with some .gml files to test. Code needs refactoring.

3. newmangreedy.py is an implementation of Newman's fast greedy algorithm, which can also be tested by .gml files.

4. The rest are some homeworks of computational physics.

# about stochastic block model
stochastic block model is a model for network communities (or call it blocks) detection. And it's also developed by MJ Newman. 

You need to know the number of communities first, unlike other methods. After that, you can start the K-means-like process to 

move the node to different block. The idea is to maximize the liklihood L(G|g) = sum_over_rs{m_rs * log(m_rs/k_r*k_s)} where 

g is the graph(network) and G is the assignment of communities. m_rs is the number of links between block r and s and k_r and 

k_s is the degree of r and s
