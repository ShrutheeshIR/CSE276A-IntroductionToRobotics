import rospy
import time

import numpy as np
from WayPointReader import *
from Planner import *
from Control import *

if __name__ == '__main__':

    rospy.init_node('ROSRunnerNODE')
    ccsv = CSVReader("waypoints.txt")
    waypoints = ccsv.read_and_parse_file()

    s = SimplePlanner(waypoints)
    cont = MotorControllerConstant()

    s.plan_path()
    time.sleep(5.0)
    cont.move_linear(0.0)
    for idx, command in enumerate(s.commands):
        if idx > 200:
            exit()
        command.display_command()
        if command.movement_type == 'r':
            myangle = command.val

            cont.rotate(myangle)
            time.sleep(2.0)
            #exit()
            '''
            if myangle>math.pi/4:
                no_of_piby4s = int(myangle/(math.pi/4)) 
                for i in range(no_of_piby4s):
                    cont.rotate(math.pi/4)
                    time.sleep(3.0)

                remaining_angle = myangle - no_of_piby4s*math.pi/4
                if remaining_angle > 0.05:
                    print("REM ANGLE : ", remaining_angle)
                    cont.rotate(remaining_angle)
                    time.sleep(3.0)
            '''
        else:
            cont.move_linear(command.val)
            time.sleep(1.0)
            #exit()

        time.sleep(2.0)
    # s.print_plan()
