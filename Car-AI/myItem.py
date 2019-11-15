#coding: utf-8

import math

# 半圆的轨道
class Circle:
    def __init__(self, rc=(0,0,0), rp=(0,0), rr=1):
        # 颜色
        self.rc = rc
        # 位置
        self.rp = rp
        # 半径
        self.rr = rr

class car:
    def __init__(self, x, y, size=(4,8)):
        # 赛车当前位置
        self.x = x
        self.y = y
        # 赛车初始角度
        self.r = -5*math.pi/180
        # 赛车速度
        self.v = 100
        self.xv = self.v*math.cos(self.r)
        self.yv = self.v*math.sin(self.r)
        # 赛车是否存活
        self.alive = True
        # 赛车行驶了多远
        self.distance = 0
        # 是否抵达终点
        self.goal = False
        # 赛车距离墙距离
        self.dis_wall = 0 # 90
        self.ldis_wall = 0 # 135
        self.lldis_wall = 0 # 180
        self.rdis_wall = 0 # 45
        self.rrdis_wall = 0 # 0

        # 与墙交点的坐标，为了计算距离
        self.dis_pos = (0,0)
        self.ldis_pos = (0,0)
        self.lldis_pos = (0,0)
        self.rdis_pos = (0,0)
        self.rrdis_pos = (0,0)

        #赛车大小
        self.size = size

    def left_move(self):
        self.r = self.r + 10*math.pi/180
        self.xv = self.v*math.cos(self.r)
        self.yv = self.v*math.sin(self.r)
    def right_move(self):
        self.r = self.r - 10*math.pi/180
        self.xv = self.v*math.cos(self.r)
        self.yv = self.v*math.sin(self.r)

    def speed_up(self):
        self.v += 5
        if self.v >=200:
            self.v = 200
        self.xv = self.v*math.cos(self.r)
        self.yv = self.v*math.sin(self.r)
    
    def speed_down(self):
        self.v -= 5
        if self.v < 50:
            self.v = 50
        self.xv = self.v*math.cos(self.r)
        self.yv = self.v*math.sin(self.r)

    def postion_move(self, time_passed_seconds):
        self.x = self.x+time_passed_seconds * self.xv
        self.y = self.y+time_passed_seconds * self.yv

    def cal_dis_to_wall(self, p, radius, big = 1, add_r = 0):
        # p为圆的圆心
        # r是园的半径
        # 分成四块计算

        # 直线的bias
        w = math.tan(self.r+add_r)
        bias = self.y - self.x*w
        px = p[0]   #0所以先不计算
        py = p[1]
        a = (w**2+1)
        b = 2*w*(bias - py)
        c = (bias-py)**2-radius**2
        if b**2 < 4*a*c:
            return (-1,-1)
        else:
            x1 = (-b+(b**2-4*a*c)**(1/2))/(2*a)
            x2 = (-b-(b**2-4*a*c)**(1/2))/(2*a)
            #x1>x2
            r = (self.r+add_r)%(2*math.pi)

            if big == 1:
                if r>=0 and r< math.pi/2:
                    y1 = w*x1+bias
                    return (x1,y1)
                elif r>= math.pi/2 and r<math.pi:
                    y2 = w*x2+bias
                    return (x2,y2)
                elif r>=math.pi and r<3*math.pi/2:
                    y2 = w*x2+bias
                    return (x2,y2)
                elif r>= 3*math.pi/2 and r<2*math.pi:
                    y1 = w*x1+bias
                    return (x1,y1)
            else:
                if r >= 0 and r < math.pi / 2:
                    y2 = w*x2+bias
                    if x2 < self.x: return (-1,-1)
                    return (x2,y2)
                elif r >= math.pi / 2 and r < math.pi:
                    y1 = w*x1+bias
                    if x1 >self.x: return (-1,-1)
                    return (x1,y1)
                elif r >= math.pi and r < 3 * math.pi / 2:
                    y1 = w*x1+bias
                    if x1 > self.x:
                        return (-1,-1)
                    return (x1,y1)
                elif r >= 3 * math.pi / 2 and r < 2 * math.pi:
                    y2 = w*x2+bias
                    if x2<self.x:
                        return (-1,1)
                    return (x2,y2)
    # 
    def _get_onepos(self, x1, x2, y1 , y2, r):
        if r >= 0 and r < math.pi / 2:
            if x1 < x2 or x2 == -1:
                return (x1,y1)
            else:
                return (x2,y2)
        elif r >= math.pi / 2 and r < math.pi:
            if x1 > x2 or x2 == -1:
                return (x1,y1)
            else:
                return (x2, y2)
        elif r >= math.pi and r < 3 * math.pi / 2:
            if x1 > x2 or x2 == -1:
                return (x1,y1)
            else:
                return (x2, y2)
        elif r >= 3 * math.pi / 2 and r < 2 * math.pi:
            if x1 < x2 or x2 == -1:
                return (x1,y1)
            else:
                return (x2, y2)
    # 距墙的距离
    def get_dis_to_wall(self, p1, radius1, p0, radius0):
        x1, y1 = self.cal_dis_to_wall(p1, radius1, 1)
        x2, y2 = self.cal_dis_to_wall(p0, radius0, 0)
        r1 = self.r%(2*math.pi)
        self.dis_pos = self._get_onepos(x1,x2,y1,y2,r1)
        self.dis_wall = ((self.x-self.dis_pos[0])**2+(self.x - self.dis_pos[1])**2)**(1/2)

        add_r = 45*math.pi/180
        x1, y1 = self.cal_dis_to_wall(p1, radius1, 1, add_r)
        x2, y2 = self.cal_dis_to_wall(p0, radius0, 0, add_r)
        r2 = (self.r+add_r)%(2*math.pi)
        self.ldis_pos = self._get_onepos(x1,x2,y1,y2,r2)
        self.ldis_wall = ((self.x-self.ldis_pos[0])**2+(self.x - self.ldis_pos[1])**2)**(1/2)
        #
        add_r = 90*math.pi/180
        x1, y1 = self.cal_dis_to_wall(p1, radius1, 1, add_r)
        x2, y2 = self.cal_dis_to_wall(p0, radius0, 0, add_r)
        r3 = (self.r+add_r)%(2*math.pi)
        self.lldis_pos = self._get_onepos(x1,x2,y1,y2,r3)
        self.lldis_wall = ((self.x-self.lldis_pos[0])**2+(self.x - self.lldis_pos[1])**2)**(1/2)
        #
        add_r = -45*math.pi/180
        x1, y1 = self.cal_dis_to_wall(p1, radius1, 1, add_r)
        x2, y2 = self.cal_dis_to_wall(p0, radius0, 0, add_r)
        r4 = (self.r+add_r)%(2*math.pi)
        self.rdis_pos = self._get_onepos(x1,x2,y1,y2,r4)
        self.rdis_wall = ((self.x-self.rdis_pos[0])**2+(self.x - self.rdis_pos[1])**2)**(1/2)
        #
        add_r = -90*math.pi/180
        x1, y1 = self.cal_dis_to_wall(p1, radius1, 1, add_r)
        x2, y2 = self.cal_dis_to_wall(p0, radius0, 0, add_r)
        r5 = (self.r+add_r)%(2*math.pi)
        self.rrdis_pos = self._get_onepos(x1,x2,y1,y2,r5)
        self.rrdis_wall = ((self.x-self.rrdis_pos[0])**2+(self.x - self.rrdis_pos[1])**2)**(1/2)
    
    # 是否存活
    def is_live(self, p1, r1, p2, r2):
        # 与赛道内侧距离
        if ((self.x-p1[0])**2+(self.y-p1[1])**2) <= (r1+3)**2:
            self.v = 0
            self.xv = self.v * math.cos(self.r)
            self.yv = self.v * math.sin(self.r)
            self.alive = False
            return False
        # 与赛道外侧距离
        if ((self.x-p2[0])**2+(self.y-p2[1])**2) >= (r2-4)**2:
            self.v = 0
            self.xv = self.v * math.cos(self.r)
            self.yv = self.v * math.sin(self.r)
            self.alive = False
            return False
        
        if self.x < 0:
            self.v = 0
            self.xv = self.v * math.cos(self.r)
            self.yv = self.v * math.sin(self.r)
            self.alive = False
            return False
        return True
    
    # 是否到达目的地
    def is_goal(self):
        if self.y < 138 and self.x < 20:
            self.goal = True
            self.alive = False
            self.v = 0
            self.xv = self.v * math.cos(self.r)
            self.yv = self.v * math.sin(self.r)
            return True
        return False

if __name__ == '__main__':
    print(math.cos(-30*math.pi/180))
    # (x,y) = cal_dis_to_wall_big((0,1),1,1,0,math.pi*135/180)
    print(-45%180)