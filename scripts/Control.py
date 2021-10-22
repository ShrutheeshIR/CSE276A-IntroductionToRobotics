#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import Float32MultiArray
import math
# from WayPointReader import *

class MotorControllerConstant:

    def __init__(self):

        self.pub = rospy.Publisher('/ctrl_cmd', Float32MultiArray, queue_size=1)
        time.sleep(5.0) 
        self.timestep = 0.02

        self.linear_speed = 0.80

        self.veh_lin_speed = 0.35 #m/s was 0.35
        self.veh_ang_speed = 4.3 #rad/s was 3.6

        self.left_to_right_linear_ratio = 0.96

        self.angular_speed = 0.75
        self.left_to_right_angular_ratio = 0.975

    
    def move_linear(self, distance):

        move = 0.0
        stop = 1.0

        duration = distance / self.veh_lin_speed
        print("LINEAR DURATION : ", duration)
        steps = int(duration / self.timestep)

        for i in range(steps):
            msg = Float32MultiArray()

            msg.data = [move, self.linear_speed, self.linear_speed * self.left_to_right_linear_ratio]
            self.pub.publish(msg)
            time.sleep(self.timestep)

        zero_speed = 0.0
        msg = Float32MultiArray()
        msg.data = [stop, 0.0, 0.0]
        self.pub.publish(msg)
        time.sleep(2.0)



    def rotate(self, angle):

        move = 0.0
        stop = 1.0
        print(angle)
        if abs(angle) < 0.01:
            duration = 0.0
            return
        
        duration = 0.07 + abs(angle) / self.veh_ang_speed
        dir = angle/abs(angle)
        print("ANGULAR DURATION ", duration)


        steps = int(duration / self.timestep)
        print(steps)

        for i in range(steps):
            msg = Float32MultiArray()

            msg.data = [move, self.angular_speed * dir, self.angular_speed * -dir * self.left_to_right_angular_ratio]
            self.pub.publish(msg)
            time.sleep(self.timestep)

        zero_speed = 0.0
        msg = Float32MultiArray()
        msg.data = [stop, zero_speed, zero_speed]
        self.pub.publish(msg)
        time.sleep(2.0)


# if __name__ == '__main__':
#     rospy.init_node('CONTROLNODE')
#     c = MotorControllerConstant()
#     c.move_linear(1)
#     time.sleep(3.0)
#     for i in range(4):
#         c.rotate(math.pi/4)
#         time.sleep(2.0)


class MotorController:
    def __init__(self):

        self.pub = rospy.Publisher('/ctrl_cmd', Float32MultiArray, queue_size=1)
        self.veh_params = {'R' : 0.031, 'L' : 0.150, 'wheel_pos' : {'slope' : 0.410013*100, 'intercept' : -0.215093*100}, 'wheel_neg' : {'slope' : 0.410013*100, 'intercept' : 0.215000*100}}
        self.left_to_right_ratio = 1.02

        self.move = 0.0
        self.stop = 1.0

        self.timestep = 0.02

        print("INITIALIZED")


    def map_phi_to_m(self, phi):
        dir = 0
        if phi > 0.5:
            dir = 1
            return (phi - self.veh_params['wheel_pos']['intercept'])/self.veh_params['wheel_pos']['slope']
        if phi < -0.5:
            dir = -1
            return (phi - self.veh_params['wheel_neg']['intercept'])/self.veh_params['wheel_neg']['slope']
        else:
            return 0


    def move_vw(self, v, w, delT):
        phi_r = w * self.veh_params['L'] / (2 * self.veh_params['R']) + v/self.veh_params['R']
        phi_l = -w * self.veh_params['L'] / (2 * self.veh_params['R']) + v/self.veh_params['R']
        motor_left, motor_right = self.map_phi_to_m(phi_l), self.map_phi_to_m(phi_r)
        steps = int(delT / self.timestep)

        print(motor_left, motor_right, phi_l, phi_r)

        print(steps, delT, self.timestep, delT/self.timestep)

        total_time = 0.0
        while total_time <= delT:
            msg = Float32MultiArray()
            msg.data = [self.move, -motor_left, -motor_right * self.left_to_right_ratio]
            self.pub.publish(msg)
            time.sleep(self.timestep)
            total_time += self.timestep

        msg = Float32MultiArray()
        msg.data = [self.stop, 0,0]
        self.pub.publish(msg)
        time.sleep(1.0)

if __name__ == '__main__':
    rospy.init_node('CONTROLNODE')

    m = MotorController()
    time.sleep(2)
    m.move_vw(0.25, 0, 2+0.06)
    time.sleep(5)
    # m.move_vw(0.0, math.pi*2, 0.25*3 + 0.06)
    time.sleep(3.0)
