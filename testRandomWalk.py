# This file is a simple test
import random as rd
import matplotlib.pyplot as plt


def RW(t,q):
    S=0;SS=[0];
    for i in range(t):
        if S<SS[rd.randint(0,i)]:
            S=S+1
        else:
            S=S-1
#        if rd.random()<0.5:
#            S=S-1
#        else:
#            S=S+1
        SS.append(S)
    return SS

def M(i,t,q):
    a=[];aa=0;
    for j in range(i):
        a.append(RW(t,q)[-1])
    for j in range(i):
        aa=aa+a[j]*a[j];
    return aa/i


def p(q,x):
    y=[];
    for t in x:
      y.append(M(10000,t,q))  
    return y


x=[10,100,500,1000,2000,3000,10000,25000,50000]
plt.plot(x,p(0.1,x),'r',x,p(0.2,x),'b',x,p(0.3,x),'g')

plt.show()

