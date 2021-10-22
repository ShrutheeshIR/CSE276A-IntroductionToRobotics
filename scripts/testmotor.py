#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import Float32MultiArray

rospy.init_node('mynode')

mypub = rospy.Publisher('/ctrl_cmd', Float32MultiArray, queue_size = 1)

t1 = time.time()
print("ABOUT TO ENTER" , t1)
for i in range(50):
    msg = Float32MultiArray()
    msg.data = [0.0, 0.6, 0.6]
    mypub.publish(msg)
    time.sleep(0.1)
#time.sleep(5)
print("DONE LOOP ", time.time() - t1)
msg.data = [1.0, 0.0, 0.0]
mypub.publish(msg)
time.sleep(2)
