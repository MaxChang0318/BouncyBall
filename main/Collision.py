# -*- coding: UTF-8 -*-
from visual import*
'''
Algorithm:
1. initialize:
    class wall: generate 1 

2. on update:
    delete balls which are out of range
    add N balls according to flow rate
    
    get balls bounced off by the wall
    get balls bounced by each other
    change their speed
    update position of the ball according to speed

    SOMEHOW calculate pressure??
'''
#something
            


class Wall():
    def __init__(self, wall_list, v):
        self.wall_list = wall_list
        self.visual = curve(pos = wall_list)
        self.v = vector(v)
    def update_pos(self, dt):
        for point in self.wall_list:
            point[0] += self.v[0] *dt
            point[1] += self.v[1] *dt
        self.visual.pos = self.wall_list
    '''
    def after_speed(self, pos, v):
        #input pos & v, return updated velocity (whether bounced or not)
        
        for i in range(len(self.wall_list)-1):
            v_re = v
            w = self.wall_list[i]-self.wall_list[i+1]
            f = vector(-w[1],w[0]) #法向量              vvv Make sure not hit from back vvv
            if checkhit(self.wall_list[i],self.wall_list[i+1],pos) and dot( [v[0],v[1],0] ,f)<0:
                #print("hit: wall %d and %d"%(i,i+1))
                v_re = reflect(w,v) + self.v #<----!!!
                #print(t,abs(v))
            return v_re
     '''       
def dist(x1,y1,x2,y2):
    return sqrt((x1-x2)**2+(y1-y2)**2)
def reflect(w,v):   #ball hit wall
    '''
    w,v must be list/array/vector with 2 numbers
    '''
    w,v = vector(w),vector(v)
    f = vector(-w[1],w[0],0) #法向量
    unit_f=f/abs(f) #法向量的單位向量
    re = v + abs(dot(v,f)/abs(f))*unit_f*2

    if abs(abs(re)-abs(v)) <= 0.001*abs(v):  #0.001 to fix floating point stuff
        if dot(v,f)<0:
            return re
        else:
            #print('!!!wrong side!!!')
            return v
    else:
        #print("back hit")
        w=-w
        f = vector(-w[1],w[0],0) #法向量
        unit_f=f/abs(f) #法向量的單位向量
        if dot(v,f)<0:
            re = v + abs(dot(v,f)/abs(f))*unit_f*2
            return re
        else:
            #print('!!!!!!!!!!!!!!!!false hit!!!!!!!!!!!!!!!')
            return v

      
def checkhit(w1,w2,b,r):
    wx1,wy1 = w1[0],w1[1]
    wx2,wy2 = w2[0],w2[1]
    bx ,by  =  b[0], b[1]
    area = 0.5*abs(wx1*wy2 + wx2*by + bx*wy1 - wy1*wx2 - wy2*bx - by*wx1)
    wall = sqrt((wx1-wx2)**2+(wy1-wy2)**2)
    # (2*area/wall)<=r : distance to wall <= radius
    # (dist(bx,by,wx1,wy1)<=r or dist(bx,by,wx2,wy2)<=r) : hit edge
    # and not(dist(bx,by,wx1,wy1)>wall or dist(bx,by,wx2,wy2)>wall) : make sure hit in the middle, not outside
    if ((2*area/wall)<=r or (dist(bx,by,wx1,wy1)<=r or dist(bx,by,wx2,wy2)<=r)) and not(dist(bx,by,wx1,wy1)>wall or dist(bx,by,wx2,wy2)>wall):
        
        #print(wall)
        #print(dist(bx,by,wx1,wy1))
        #print(dist(bx,by,wx2,wy2))
      
        return True
    else: return False

def vcollision(a1p, a2p, a1v,a2v): #ball hit ball
    v1prime = a1v - (a1p - a2p)  * sum((a1v-a2v)*(a1p-a2p)) / sum((a1p-a2p)**2)
    v2prime = a2v - (a2p - a1p)  * sum((a2v-a1v)*(a2p-a1p)) / sum((a2p-a1p)**2)
    return v1prime, v2prime

def vectorfy(points):
    for i in range(len(points)):
        points[i] = vector(points[i])
    return points
