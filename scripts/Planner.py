#!/home/oloin/home/base_py/bin/env python
# import rospy
import time
import math

class Command:
    def __init__(self, op, val, direction):
        self.movement_type = op
        self.val = val
        self.dir = direction

    def get_val(self):
        return self.val
    
    def get_op(self):
        if self.movement_type == 'r':
            return 'rotate-in-place'
        else:
            return 'linear-movement-in-place'
    
    def display_command(self):
        if self.movement_type == 'r':
            print("Rotating In Place by {angle} radians in {dir} direction".format(angle=self.val, dir = "clockwise" if self.dir > 0 else "anticlockwise"))
        else:
            print("Moving linearly for {dist} metres in {dir} direction".format(dist=self.val, dir = "forward" if self.dir > 0 else "backward"))
        

class SimplePlanner:

    def __init__(self, waypoints):
        self.waypoints = waypoints

        self.commands = []
        

        self.cur_pos = (0.0, 0.0)
        self.cur_ori = 0.0

    
    def plan_path(self):

        for wp in self.waypoints[1:]:

            ori = wp[-1]
            pos = (wp[0], wp[1])


            rel_heading = math.atan2(pos[1] - self.cur_pos[1], pos[0] - self.cur_pos[0]) - self.cur_ori

            print(rel_heading, pos[1] - self.cur_pos[1], pos[0] - self.cur_pos[0])

            if abs(rel_heading) > 3.14:
                rel_heading *= 0.9
            
            if abs(rel_heading) > math.pi:
                rel_heading = 2 * math.pi - rel_heading

            self.cur_ori = rel_heading + self.cur_ori

            if rel_heading == 0:
                self.commands.append(Command('r', 0, 1))
            else:
                self.commands.append(Command('r', rel_heading, rel_heading / abs(rel_heading)))


            dist = math.sqrt((pos[1] - self.cur_pos[1])**2 + (pos[0] - self.cur_pos[0])**2)
            self.cur_pos = pos
            self.commands.append(Command('l', dist, 1))

            rel_angle = ori - self.cur_ori

            if abs(rel_angle) > 3.1415:
                rel_angle *= 0.9

            if abs(rel_angle) > math.pi:

                mydir = rel_angle/abs(rel_angle)
                rel_angle = 2 * math.pi - abs(rel_angle) * -mydir


            self.cur_ori = ori

            if rel_angle == 0:
                self.commands.append(Command('r', 0, 1))
            else:
                self.commands.append(Command('r', rel_angle, rel_angle / abs(rel_angle)))

    def print_plan(self):
        for cmd in self.commands:
            cmd.display_command()

