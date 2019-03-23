import pygame
from pygame.locals import *
from sys import exit
import numpy as np
import copy

import myItem
import myCarAI

def mapPaint(pygame, screen, BigCircle, smallCircle):
    screen.fill((255, 255, 255))
    # 绘制地图
    pygame.draw.circle(screen, BigCircle.rc, BigCircle.rp, BigCircle.rr)
    pygame.draw.circle(screen, smallCircle.rc, smallCircle.rp, smallCircle.rr)
    pygame.draw.rect(screen, (0, 0, 255), Rect((0, 1), (30, 158)))

def carPaint(pygame, screen, cars):
    # 绘制小车
    for i in range(len(cars)):
        car = cars[i]
        pygame.draw.rect(screen, (0, 255, 0), Rect((car.x, car.y), (car.size)))
        pygame.draw.line(screen, (255, 255, 0), (car.x + car.size[0] / 2, car.y + car.size[1] / 2),
                         (car.dis_pos[0], car.dis_pos[1]))
        # pygame.draw.line(screen, (0, 255, 0), (car.x + car.size[0] / 2, car.y + car.size[1] / 2),
        #                  (car.ldis_pos[0], car.ldis_pos[1]))
        # pygame.draw.line(screen, (0, 255, 0), (car.x + car.size[0] / 2, car.y + car.size[1] / 2),
        #                  (car.lldis_pos[0], car.lldis_pos[1]))
        # pygame.draw.line(screen, (0, 255, 0), (car.x + car.size[0] / 2, car.y + car.size[1] / 2),
        #                  (car.rdis_pos[0], car.rdis_pos[1]))
        # pygame.draw.line(screen, (0, 255, 0), (car.x + car.size[0] / 2, car.y + car.size[1] / 2),
        #                  (car.rrdis_pos[0], car.rrdis_pos[1]))

#这需要很多功夫啊
def pick_best_AI(cars, carAis):
    bestindex = 0
    farDistance = 1000
    for i in range(len(cars)):
        if cars[i].distance < farDistance:
            farDistance = cars[i].distance
            bestindex = i
        if cars[i].goal == True:
            bestindex = i
            break
    print(cars[bestindex].distance)
    bestAI = myCarAI.carAI()
    w, b = carAis[bestindex].get_weights()
    bestAI.assign_weights(copy.deepcopy(w), copy.deepcopy(b))
    return bestAI

def gameStart():
    pygame.init()
    bigCircle = myItem.Circle((0,0,0), (0,320), 320)
    smallCircle = myItem.Circle((255, 255, 255), (0,320), 160)
    #生成200辆car和200个AI
    cars = []
    carAis = []
    carnum = 100
    for i in range(carnum):
        cars.append(myItem.car(2, 560, (15,15)))
        carAis.append(myCarAI.carAI())

    screen = pygame.display.set_mode((480, 640), 0, 32)
    # Clock对象
    clock = pygame.time.Clock()
    for k in range(60):
        print("第%d次--------------------"%k)
        for i in range(1000):
            #手动操作
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            #AI
            #input car.r  car.v car.dis-s 7 output speed, direction
            #根据speed和direction控制小车
            #计算移动距离
            time_passed = clock.tick(); time_passed_seconds = time_passed / 1000.
            for i in range(len(cars)):
                car = cars[i]
                if car.alive == False:
                    continue
                car.get_dis_to_wall((0, 320), 320, (0, 320), 160)
                car.postion_move(time_passed_seconds)
                carAi = carAis[i]
                data = np.array([car.r*3, car.v/100, car.dis_wall/300, car.ldis_wall/300,
                                 car.lldis_wall/300, car.rdis_wall/300, car.rrdis_wall/300])
                # print(data)
                data = data.T
                #控制方向
                v,dir = carAi.forward(data)
                if v == -1:
                    car.speed_down()
                elif v == 1:
                    car.speed_up()
                if dir == -1:
                    car.left_move()
                elif dir == 1:
                    car.right_move()
                if car.is_goal() == True:
                    print("goal!")
                    # filename = "goal"+str(i)
                    # carAi.save(filename)
                if car.is_live(smallCircle.rp, smallCircle.rr, bigCircle.rp, bigCircle.rr)==False:
                    pass

                car.distance = car.y

            mapPaint(pygame, screen, bigCircle, smallCircle)
            carPaint(pygame, screen,cars)
            pygame.display.update()

            #是否结束
            flag = 0
            for i in range(len(cars)):
                car = cars[i]
                if car.alive == True:
                    flag = 1
            if flag == 0: break

        #选出最好的一个AI
        bestAI = pick_best_AI(cars, carAis)
        cars.clear(); carAis.clear()
        for i in range(carnum):
            cars.append(myItem.car(2, 560, (15, 15)))
        carAis = myCarAI.gene_algo(bestAI, carnum)

def testAI(filename):
    pygame.init()
    bigCircle = myItem.Circle((0, 0, 0), (0, 320), 320)
    smallCircle = myItem.Circle((255, 255, 255), (0, 320), 160)

    car = myItem.car(2, 560, (15, 15))
    carAi = myCarAI.carAI()
    #load训练好的神经网络
    carAi.load(filename)
    screen = pygame.display.set_mode((480, 640), 0, 32)
    # Clock对象
    clock = pygame.time.Clock()
    for i in range(5000):
        # 手动操作
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        # AI
        # input car.r  car.v car.dis-s 7 output speed, direction
        # 根据speed和direction控制小车
        # 计算移动距离
        time_passed = clock.tick()
        time_passed_seconds = time_passed / 1000.
        car.postion_move(time_passed_seconds)
        car.get_dis_to_wall((0, 320), 320, (0, 320), 160)

        data = np.array([car.r * 3, car.v / 100, car.dis_wall / 300, car.ldis_wall / 300,
                         car.lldis_wall / 300, car.rdis_wall / 300, car.rrdis_wall / 300])
        data = data.T
        v, dir = carAi.forward(data)
        if v == -1:
            car.speed_down()
        elif v == 1:
            car.speed_up()
        if dir == -1:
            car.left_move()
        elif dir == 1:
            car.right_move()
        if car.is_goal() == True:
            print("goal!")
            break
        if car.is_live(smallCircle.rp, smallCircle.rr, bigCircle.rp, bigCircle.rr) == False:
            print("error")
            break

        mapPaint(pygame, screen, bigCircle, smallCircle)
        pygame.draw.rect(screen, (0, 255, 0), Rect((car.x, car.y), (car.size)))
        pygame.draw.line(screen, (255, 255, 0), (car.x + car.size[0] / 2, car.y + car.size[1] / 2),
                         (car.dis_pos[0], car.dis_pos[1]))
        pygame.draw.line(screen, (0, 255, 0), (car.x + car.size[0] / 2, car.y + car.size[1] / 2),
                         (car.ldis_pos[0], car.ldis_pos[1]))
        pygame.draw.line(screen, (0, 255, 0), (car.x + car.size[0] / 2, car.y + car.size[1] / 2),
                         (car.lldis_pos[0], car.lldis_pos[1]))
        pygame.draw.line(screen, (0, 255, 0), (car.x + car.size[0] / 2, car.y + car.size[1] / 2),
                         (car.rdis_pos[0], car.rdis_pos[1]))
        pygame.draw.line(screen, (0, 255, 0), (car.x + car.size[0] / 2, car.y + car.size[1] / 2),
                         (car.rrdis_pos[0], car.rrdis_pos[1]))

        pygame.display.update()


if __name__ == '__main__':
    # gameStart()
    filename = "goal_para/goal17.npz"
    testAI(filename)


