#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import Float32MultiArray
# Calib eqn : if min = m0 => y = (1-m0)x + m0

class CalibMotors:
    
    def __init__(self):
        self.pub = rospy.Publisher('/ctrl_cmd', Float32MultiArray, queue_size=1)


        self.wheel1_radius = 0.3
        self.wheel2_radius = 0.3


        self.timestep = 0.02
        self.left_to_right_line_ratio = 0.987

        self.start_vel = 0.0
        

    def starting_velocity(self):

        start_vel = 0.3
        move = 0.0
        stop = 1.0


        while(start_vel < 0.65):
            print(start_vel)
            for i in range(50):
                msg = Float32MultiArray()
                msg.data = [move, start_vel, start_vel]
                self.pub.publish(msg)
                time.sleep(0.1)

            speed = 0.0
            msg = Float32MultiArray()
            msg.data = [stop, speed, speed]
            self.pub.publish(msg)
            time.sleep(1.0)
            start_vel += 0.05

    def straight_forward_calib(self, speed, duration):

        move = 0.0
        stop = 1.0

        steps = int(duration // self.timestep)
        print(steps)
        t1 = time.time()
        for i in range(steps):
            msg = Float32MultiArray()

            msg.data = [move, -speed, -speed * self.left_to_right_line_ratio]
            self.pub.publish(msg)
            time.sleep(self.timestep)
        print("Actual duration : ", time.time() - t1)
        speed = 0.0
        msg = Float32MultiArray()
        msg.data = [stop, speed, speed]
        self.pub.publish(msg)
        time.sleep(2.0)

    
    def in_place_rotate_calib(self, speed, duration):

        move = 0.0
        stop = 1.0

        steps = int(duration // self.timestep)
        print(steps)
        for i in range(steps):
            msg = Float32MultiArray()

            msg.data = [move, speed, -speed * self.left_to_right_line_ratio]
            self.pub.publish(msg)
            time.sleep(self.timestep)

        speed= 0.0
        msg = Float32MultiArray()
        msg.data = [stop, speed, speed]
        self.pub.publish(msg)
        time.sleep(2.0)


    def issue_command(self):

        # self.starting_velocity()
        # vel_val = 0.80
        # self.straight_forward_calib(vel_val, 3)
        vel_st = 0.65
        for i in range(7):
            for i in range(2):
                print(vel_st*100)
                self.straight_forward_calib(vel_st, 3)
                time.sleep(10.0)
            vel_st += 0.05

        # for i in range(1):
        # vel_val = 0.80
        # self.in_place_rotate_calib(vel_val, (0.637365293696689+ (1.0-vel_val)*0)*2)
            #time.sleep(3.0)


if __name__ == '__main__':
    rospy.init_node('CalibTestNode')
    c = CalibMotors()
    c.issue_command()
