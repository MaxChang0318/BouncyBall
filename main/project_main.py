# -*- coding: UTF-8 -*-
'''
  A_____A
 /  = . =  - Developed by CKB, do not steal plz
/     w   \
current version: 1.2

update log:
ver 1.0 - initial release
ver 1.1 - fix weird acceleration
ver 1.2 - fix "ball stuck in wall" problem

ver 2.0 -  MOAR BALLS

'''
from visual import *
from visual.graph import *
from Collision import *

## variables
r = 0.1 #radius of ball
#N = 50


## visual stuff
scene = display(x=0,y=0,width=600,height=600,background=(0,0,0),center = vector(0,0) #!vis
                ,autoscale = False,)  #!vis
gd = gdisplay(x=600,y=0,width=300,height=300,xtitle='t',title = 'velocity',
              foreground=color.black,background=color.white)
gd2= gdisplay(x=600,y=300,width=300,height=300,xtitle='t',title = 'Ball Amount',
              foreground=color.black,background=color.white)

f1 = gcurve(color=color.blue, gdisplay=gd)
f2 = gcurve(color=color.red , gdisplay=gd)
f3 = gcurve(color=color.green,gdisplay=gd2)

random.seed(1)


#main code
t = 0
dt =0.001
dts = 0

#initialization ends

class Container():
    def __init__(self, parts):
        global r
        self.parts = parts #list sections of container
        ## balls
        self.N = 3 #initial number of ball
        
        self.v = random.uniform(-30,30,[self.N,3]) #velocity of balls
        for i in range(len(self.v)):
            self.v[i][0] = 0
            self.v[i][1] = 0 #random.random(size = None)*10 - 5
            self.v[i][2] = 0
        
        
        #pos_arr = random.uniform(-3,3,(N,3))
        self.pos_arr = zeros((self.N,3)) #pos of ball
            
        for i in range(len(self.pos_arr)):
            self.pos_arr[i][2] = 0
            self.pos_arr[i][1] = random.random(size = None)*6 - 3
            self.pos_arr[i][0] = random.random(size = None)*6 - 3
        
        self.ball = [sphere(radius = r,make_trail=False,       #!vis
                    color=color.yellow) for i in range(self.N)]#!vis
        
        self.ball[0].color = color.red  #!vis
        #self.ball[0].make_trail = True  #!vis
        for i in range(self.N):  #!vis
            self.ball[i].pos = vector(self.pos_arr[i])  #!vis
        
    def OnUpdate(self):
        '''
        The main update function.
        '''
        for j in range(self.N):
            for k in range(2):
                self.pos_arr[j][k] += self.v[j][k]*dt  # update ball position array

            self.ball[j].pos = vector(self.pos_arr[j])  # update visual ball position #!vis
            #'''  ball hit detection
            r_array = self.pos_arr - self.pos_arr[:,newaxis]   # all pairs of atom-to-atom vectors
            rmag = sum(square(r_array),-1)                     # atom-to-atom distance squared
            hit = nonzero((rmag < 4*r**2) - identity(self.N))
            hitlist = zip(hit[0], hit[1])     
            for p,q in hitlist:
                if sum((self.pos_arr[p]-self.pos_arr[q])*(self.v[p]-self.v[q])) < 0 :       # check if approaching
                    self.v[p], self.v[q] = vcollision(self.pos_arr[p], self.pos_arr[q], self.v[p], self.v[q])
                    #print('ball hit')
            #'''
            
            for part in self.parts:

                wall = part.wall_list
                for i in range(len(wall)-1):
                    w = wall[i]-wall[i+1]
                    f = vector(-w[1],w[0]) #法向量
                    if checkhit(wall[i],wall[i+1],self.pos_arr[j],r) and dot([self.v[j][0]-part.v[0],self.v[j][1]-part.v[1],0], f) <= 0:
                        #print("hit: wall %d and %d"%(i,i+1))
                        self.v[j] = reflect(w,self.v[j] - part.v) + part.v
                        print(dot([self.v[j][0]-part.v[0],self.v[j][1]-part.v[1],0], f))
                        print(self.v[j])
                        print(reflect(w,self.v[j] - part.v) + part.v -reflect(w,self.v[j]))
                        print('---')
                
                part.update_pos(dt)  # update wall position
                

    def add_ball(self,pos,vel):
        '''
        pos,v should be list with 3 variables
        '''
        
        self.ball.append(sphere(radius=r,make_trail=False,color=color.yellow)) #!vis
        self.pos_arr = append(self.pos_arr,[pos], axis = 0)
        self.v = append(self.v,[vel], axis = 0)
        self.N += 1
        #print('NOW N = %d'%self.N)
    
    def del_ball(self,index):
        #print('del ball %d' % index)
        
        self.ball[index].visible = False    #!vis
        del self.ball[index]                #!vis
        self.pos_arr = delete(self.pos_arr, index, 0)
        self.v = delete(self.v, index, 0)
        self.N -= 1

wall1 = [[3,3],[3,-3],[-3,-3],[-3,3]]
wall2 = [[-3,3],[3,3]] 
#wall1 = [[0,3],[22,3],[22,-3],[0,-3]]  #pipe
#wall1 = [[17,1],[15,1],[15,0],[17,0],[17,1]]   #square
#wall2 = [[17,1],[15,1],[15,-1],[17,-1],[17,1]]   #square
#wall = [[1,1],[1,0],[-1,-1],[-1,0],[1,2],[1,3]]
#wall = [[780,0],[1150,-140],[1180,-130],[1170,-90],[970,0],[780,0]]
'''
wall = [[0,60],[300,60],[850,240],[900,250],[940,220],[950,170],[940,130],[900,100],[730,60],[1170,40],
        [1400,60],
        [1400,0],[1070,0],[1200,-60],[1230,-90],[1240,-130],[1230,-170],[1180,-190],[1130,-180],[610,0],[300,20],
        [0,0],[0,60]]
#'''

wall1,wall2 = vectorfy(wall1), vectorfy(wall2)
flow = Container(parts = [Wall(wall1, v = vector(0,0) ),Wall(wall2, v = vector(0, -5) )])  #!vis    

while True:
    rate(100)
    t += dt
    dts += 1
    if flow.parts[1].wall_list[0][1] <= -2 : 
        flow.parts[1].v = vector(0, 5) 
    if flow.parts[1].wall_list[0][1] >= 3 :
        flow.parts[1].v = vector(0, -5) 
    '''
    if dts%10 == 0:
        rd = random.uniform(9,11)
        rdv= random.uniform(-1,1)
        rd2 =random.uniform(-3,3)
        summon_ball((0,rd2,0),(rd,rdv,0))
    #'''
    #average vel
    tmp, tmp2 = 0, 0
    avg, avg2 = 0, 0
    n1, n2= 0 ,0
    for i in range(len(flow.v)):
        ab = abs(vector(flow.v[i]))**2
        tmp += ab
        n1 += 1
    if n1 != 0:
        avg = tmp/n1
    
    for i in range(len(flow.v)):
        if flow.v[i][0] > 15:
            ab = abs(vector(flow.v[i]))**2
            tmp2 += ab
            n2 += 1
    if n2 != 0:
        avg2 = tmp/n2

    if n1 != 0:
        f1.plot(pos = (t,avg))
    if n2 != 0:
        f2.plot(pos = (t,avg2))
        
    flow.OnUpdate()  
           
    if dts % 10 == 0 :
        #print('add ball')
        pass
        #flow.add_ball(pos = [0,random.random(size = None)*6 - 3,0],vel = [random.random(size = None)*10 +30,random.random(size = None)*10 -5,0])
        #flow.add_ball(pos = [0,random.random(size = None)*6 - 3,0],vel = [50,0,0])
    if dts % 100 == 0:
        pass
        #flow.ball[0].make_trail = True

    '''
    m = -1  ##trying to delete a ball without problem
    while True:
        m += 1
        if m == flow.N:
            break
        
        if flow.pos_arr[m][0] > 21 or flow.pos_arr[m][0] < 0 or abs(flow.pos_arr[m][1]) > 3:
            #print('prev N = %d' % N)
            flow.del_ball(m)  #delete ball out of range
            #print('after N = %d' % N)
            m -= 1
    '''

    f3.plot(pos=(t,flow.N))
        