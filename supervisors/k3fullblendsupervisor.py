from math import sqrt, sin, cos, pi, atan2
from supervisors.khepera3 import K3Supervisor

class K3BlendingSupervisor(K3Supervisor):
    """K3Blending supervisor creates two controllers: gotogoal and avoidobstacles
       and blends their outputs instead of choosing one.
       
       This module is intended to be demonstration on implementing blending supervisors"""
    def __init__(self, robot_pose, robot_info):
        """Creates an avoid-obstacle controller and go-to-goal controller"""
        K3Supervisor.__init__(self, robot_pose, robot_info)

        #Add controllers ( go to goal is default)
        self.parameters.sensor_poses = robot_info.ir_sensors.poses[:]
        self.avoidobstacles = self.get_controller('avoidobstacles.AvoidObstacles', self.parameters)
        self.gtg = self.get_controller('gotogoal.GoToGoal', self.parameters)

        self.current = self.gtg
        self.old_omega = 0

    def execute(self, robot_info, dt):
        """Blend the behaviour of several controllers"""
        # Copied from Supervisor
        self.robot = robot_info
        self.pose_est = self.estimate_pose()

        # Check if we are in place
        distance_from_goal = sqrt((self.pose_est.x - self.parameters.goal.x)**2 + (self.pose_est.y - self.parameters.goal.y)**2)
        if distance_from_goal < self.robot.wheels.base_length/2:
            return (0,0)

        # Fill parameters for the controllers
        self.parameters.pose = self.pose_est
        self.parameters.sensor_distances = self.get_ir_distances()

        # now instead of choosing one controller, blend results
        distmin = min(self.parameters.sensor_distances)
        distmax = self.robot.ir_sensors.rmax
        
        distance_ratio = distmin/distmax     
        if distance_ratio > 1:
            distance_ratio = 1
        # Forget about the goal at 0.2 ratio
        distance_ratio -= 0.2
        distance_ratio /= 0.8

        weight_avo = 0.5*(1 + cos(pi*distance_ratio))

        v_gtg, w_gtg = self.gtg.execute(self.parameters,dt) #execute go-to-goal
        v_avo, w_avo = self.avoidobstacles.execute(self.parameters,dt) #execute go-to-goal

        v = v_gtg*(1-weight_avo) + v_avo*weight_avo
        w = w_gtg*(1-weight_avo) + w_avo*weight_avo
       
        vl, vr = self.uni2diff((v,w))
        return (vl, vr) 

    def draw_foreground(self, renderer):
        K3Supervisor.draw_foreground(self,renderer)
        renderer.set_pose(self.pose_est)

        # Draw direction from obstacles
        renderer.set_pen(0xFF0000)
        arrow_length = self.robot_size*5
        renderer.draw_arrow(0,0,
            arrow_length*cos(self.avoidobstacles.away_angle),
            arrow_length*sin(self.avoidobstacles.away_angle))

        # Draw direction to goal
        renderer.set_pen(0x444444)
        goal_angle = atan2(self.parameters.goal.y - self.pose_est.y,
                           self.parameters.goal.x - self.pose_est.x) \
                     - self.pose_est.theta
        renderer.draw_arrow(0,0,
            arrow_length*cos(goal_angle),
            arrow_length*sin(goal_angle))
                           