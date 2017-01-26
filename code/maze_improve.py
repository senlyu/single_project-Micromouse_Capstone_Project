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
    getback = []
    for i in range(V.shape[0]):
        for j in range(V.shape[0]):
            if V[i,j] != 0:
                V_new.append(change_point(i,j))
                if change_point(i,j) == start:
                    start_new = k
                elif change_point(i,j) == end:
                    end_new = k
                getback.append(change_point(i,j))
                k += 1
    E_new = np.ndarray(shape=(len(V_new),len(V_new)),dtype=np.int32)
    E_new.fill(9999)
    for i in range(len(V_new)):
        for j in range(len(V_new)):
            if E[V_new[i],V_new[j]] == 1:
                E_new[i,j] = 1
    return V_new, E_new, start_new, end_new, getback

# Using Dijkstra Algorithm to solve the single_source shortest path
def shortest(V,E,start,end,getback):
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
    
    def printout(start,end,prelist):
        if start == end:
            pass
        else:
            new_end=pre[end]
            prelist = printout(start,new_end,prelist)            
            prelist.append(end)
        return prelist
    
    prelist = []    
    prelist = printout(start, end, prelist)
    prev = []
    for i in range(len(prelist)):
        prev.append(getback[prelist[i]]) 
    return w[end], prev
'''
#code for test shortest
V.fill(1)
start = change_point(0,0)
end = change_point(6,6)
V_new, E_new, start_new, end_new, getback = know_area(V,E,start,end)
distance, prelist = shortest(V_new, E_new, start_new, end_new, getback)
print(distance)
'''




def reachgoal(now):
    return (now == change_point(dim/2,dim/2) or \
            now == change_point(dim/2-1,dim/2) or \
            now == change_point(dim/2,dim/2-1) or \
            now == change_point(dim/2-1,dim/2-1))

def run(E,V,now,prev,time):
    nextp = now
    for i in range(E.shape[1]):
        if E[now,i] == 1:
            x,y = change_back_point(i)
            if V[x,y] == 0:
                V[x,y] = 1
    mindis = 9999    
    newmindis = 9999
    prelistmin = []
    for i in range(dim):
        for j in range(dim):
            if V[i,j] == 1:
                newdis = abs(i + j - dim + 1)
                V_new, E_new, start_new, end_new, getback = know_area(V,E,now,change_point(i,j))
                greydis, prelist = shortest(V_new, E_new, start_new, end_new, getback)                

                if newdis < newmindis:
                    newmindis = newdis
                    mindis = greydis
                    prelistmin = prelist
                    nextp = change_point(i,j)
                    
    #test
    '''
    print('Total time', time)
    print('now',change_back_point(now))
    print('cost time', mindis)
    print('next point',change_back_point(nextp))
    for i in range(len(prelistmin)):
        aa,bb=change_back_point(prelistmin[i])
        print('steps',aa,bb)
    '''

    time += mindis
    if time > 1000:
    	print('error')
    now = nextp
    prev = prev + prelistmin
    now_x, now_y = change_back_point(now)
    V[now_x, now_y] = 2

    return E,V,now,prev,time


# initialize
now = change_point(0,0)
now_x, now_y = change_back_point(now)
V[now_x, now_y] = 2
time1 = 0
prev1 = []
# first time walk
while not reachgoal(now):
    E,V,now,prev1,time1 = run(E,V,now,prev1,time1)


def printpre(prev):
    for i in range(len(prev)):
        aa,bb=change_back_point(prev[i])
        print(aa,bb)

time = time1

#set all the goal to black
V[dim/2,dim/2] = 2
V[dim/2-1,dim/2] = 2
V[dim/2,dim/2-1] = 2
V[dim/2-1,dim/2-1] = 2

def finded(E,V):
    V_all = V[:,:]
    V_all.fill(2)
    V_new, E_new, start_new, end_new, getback = know_area(V_all,E,change_point(0,0),change_point(dim/2,dim/2))
    short2, short2list = shortest(V_new, E_new, start_new, end_new, getback)
    flag = True
    for i in range(len(short2list)):
    	a,b=change_back_point(short2list[i])
    	if V[a,b] != 2:
    		flag = False
    		break
    return flag


    
prev2 = []
time2 = 0
while not finded(E,V):
    E,V,now,prev2,time2 = run(E,V,now,prev2,time2)


prev3 = []
time3 = 0
V_new, E_new, start_new, end_new, getback = know_area(V,E,now,change_point(0,0))
backdis, prev3 = shortest(V_new, E_new, start_new, end_new, getback)
time3 = backdis
now = change_point(0,0)


time4 = 0
V_new, E_new, start_new, end_new, getback = know_area(V,E,change_point(0,0),change_point(dim/2,dim/2))
time4, shortest = shortest(V_new, E_new, start_new, end_new, getback)
time4 *= 2

print('time1',time1)
print('time2',time2)
print('time3',time3)
print('time4',time4)
print('score',(time1+time2+time3)/30.0+time4)


V.fill(2)
V_new, E_new, start_new, end_new, getback = know_area(V,E,change_point(0,0),change_point(dim/2,dim/2))
timeshort, theshortest = shortest(V_new, E_new, start_new, end_new, getback)
print('theroy shortest time', timeshort)
