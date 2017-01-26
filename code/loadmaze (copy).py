import numpy as np
import sys


def change_point(a,b):
    point = a * dim + b
    return point

def change_back_point(point):
    a = point / dim
    b = point % dim
    return a,b


filename=str(sys.argv[1])
with open(filename, 'rb') as f_in:
    global dim
    dim = int(f_in.next())
    map_info = []
    for line in f_in:
        map_info.append(map(int,line.split(',')))
    map_info = np.array(map_info)

total_point = dim * dim    

# All the points
V = np.zeros((dim,dim),dtype=np.int32)
# All the edges, 0 for connected, 1 for wall
E = np.ndarray(shape=(total_point,total_point),dtype=np.int32)

E.fill(9999)
# get the wall done
for i in range(dim):
    for j in range(dim):
        x = map_info[i,j]
        up, right, botton, left = False, False, False, False   
        if x >= 8:
            left = True
            x -= 8
        if x >= 4:
            botton = True
            x -= 4
        if x >= 2:
            right = True
            x -= 2
        if x >= 1:
            up = True
        if (up and j+1 < dim):
            E[change_point(i,j),change_point(i,j+1)] = 1
            E[change_point(i,j+1),change_point(i,j)] = 1
        if (right and i+1 < dim):
            E[change_point(i,j),change_point(i+1,j)] = 1
            E[change_point(i+1,j),change_point(i,j)] = 1
        if (botton and j-1 >= 0):
            E[change_point(i,j),change_point(i,j-1)] = 1
            E[change_point(i,j-1),change_point(i,j)] = 1
        if (left and i-1 >= 0):
            E[change_point(i,j),change_point(i-1,j)] = 1
            E[change_point(i-1,j),change_point(i,j)] = 1

# before find the shortest, first to load the V and E correctly
def know_area(V,E,start,end):
    k = 0
    V_new = []
    for i in range(V.shape[0]):
        for j in range(V.shape[0]):
            if V[i,j] != 0:
                V_new.append(change_point(i,j))
                if change_point(i,j) == start:
                    start_new = k
                elif change_point(i,j) == end:
                    end_new = k
                k += 1
    E_new = np.ndarray(shape=(len(V_new),len(V_new)),dtype=np.int32)
    E_new.fill(9999)
    for i in range(len(V_new)):
        for j in range(len(V_new)):
            if E[V_new[i],V_new[j]] == 1:
                E_new[i,j] = 1
    return V_new, E_new, start_new, end_new

# Using Dijkstra Algorithm to solve the single_source shortest path
def shortest(V,E,start,end):
    w = [ 999 for i in range(len(V))]
    w[start] = 0
    pre = [ 0 for i in range(len(V))]
    Q = set( i for i in range(len(V)))

    while len(Q) >0:
        minn = 9999
        for element in Q:
            if w[element] < minn:
                minn = w[element]
                u = element
        Q.remove(u)
        for i in range(E.shape[0]):
            if E[u,i] == 1:
                alt = w[u]+1
                if alt < w[i]:
                    w[i] = alt
                    pre[i] = u
    #for test
    
    def printout(x,y,a,b,prelist):
        if a == x and b == y:
            pass
        else:
            a_,b_=change_back_point(pre[change_point(a,b)])
            prelist = printout(x,y,a_,b_,prelist)
            
            prelist.append(change_point(a,b))

        return prelist
    
    prelist = []
    start_x, start_y = change_back_point(start)
    end_x, end_y = change_back_point(end)
    prelist = printout(start_x, start_y, end_x, end_y, prelist)
    return w[end], prelist
'''
#code for test shortest
V.fill(1)
start = change_point(0,0)
end = change_point(11,11)
V_new, E_new, start_new, end_new = know_area(V,E,start,end)
distance, prelist = shortest(V_new, E_new, start_new, end_new)
print(distance)
for i in range(len(prelist)):
	aa,bb=change_back_point(prelist[i])
	print(aa,bb)
'''

# initialize
now = change_point(0,0)
now_x, now_y = change_back_point(now)
V[now_x, now_y] = 2
time1 = 0
nextp = now
# walk first time

def reachgoal(now):
    return (now == change_point(dim/2,dim/2) or \
            now == change_point(dim/2-1,dim/2) or \
            now == change_point(dim/2,dim/2-1) or \
            now == change_point(dim/2-1,dim/2-1))
 

prev = []
# first time
while not reachgoal(now):

    for i in range(E.shape[1]):
        if E[now,i] == 1:
            x,y = change_back_point(i)
            if V[x,y] == 0:
                V[x,y] = 1


    mindis = 9999
    
    for i in range(dim):
        for j in range(dim):
            if V[i,j] == 1:                
                V_new, E_new, start_new, end_new = know_area(V,E,now,change_point(i,j))
                greydis, prelist = shortest(V_new, E_new, start_new, end_new)
                if greydis < mindis:
                    mindis = greydis
                    prelistmin = prelist
                    nextp = change_point(i,j)


    time1 += mindis
    print('Total time', time1)
    print('now',change_back_point(now))
    print('cost time', mindis)
    now = nextp
    prev = prev + prelistmin
    #
    print('next point',change_back_point(now))
    for i in range(len(prelistmin)):
	    aa,bb=change_back_point(prelistmin[i])
	    print('steps',aa,bb)

    now_x, now_y = change_back_point(now)
    V[now_x, now_y] = 2
print(time1)
#for i in range(len(prev)):
#	aa,bb=change_back_point(prev[i])
#	print(aa,bb)

time = time1






