#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
from dynamic_reconfigure.server import Server
from motor_control.cfg import PIDConfig
from Controller_PID import PIDController
from motor_model import MotorSystem
import numpy as np


class MotorControlNode:
    def __init__(self):
        rospy.init_node('motor_control_node', anonymous=True)

        # Initialize MotorSystem with default PID parameters
        self.motor_system = MotorSystem(Kp=1.0, Ki=0.1, Kd=0.05)

        # ROS Subscribers
        self.speed_subscriber = rospy.Subscriber('/motor_speed', Float32, self.speed_callback)
        self.position_subscriber = rospy.Subscriber('/motor_position', Float32, self.position_callback)

        # ROS Publishers
        self.speed_publisher = rospy.Publisher('/motor_speed_feedback', Float32, queue_size=10)
        self.position_publisher = rospy.Publisher('/motor_position_feedback', Float32, queue_size=10)

        # ROS Service to reset the PID controller
        self.reset_service = rospy.Service('/reset_pid', Empty, self.reset_pid)

        # Dynamic reconfigure server
        self.srv = Server(PIDConfig, self.reconfigure_callback)

    def speed_callback(self, msg):
        setpoint = msg.data
        rospy.loginfo(f"Setting motor speed to: {setpoint}")
        times, motor_speeds, gear_speeds, pwms = self.motor_system.control_motor(setpoint, dt=0.01, time_end=2.0)
        for speed in motor_speeds:
            self.speed_publisher.publish(speed)
            rospy.sleep(0.01)  # simulate real-time publishing

    def position_callback(self, msg):
        setpoint = msg.data
        rospy.loginfo(f"Setting motor position to: {setpoint}")
        times, motor_speeds, gear_speeds, pwms = self.motor_system.control_motor(setpoint, dt=0.01, time_end=2.0)
        for position in gear_speeds:
            self.position_publisher.publish(position)
            rospy.sleep(0.01)  # simulate real-time publishing

    def reconfigure_callback(self, config, level):
        rospy.loginfo(f"Reconfigure request: {config}")
        self.motor_system.pid.Kp = config['Kp']
        self.motor_system.pid.Ki = config['Ki']
        self.motor_system.pid.Kd = config['Kd']
        return config

    def reset_pid(self, req):
        rospy.loginfo("Resetting PID controller")
        self.motor_system.pid.reset()
        return EmptyResponse()

    def run(self):
        rospy.spin()


if __name__ == '__main__':
    try:
        node = MotorControlNode()
        node.run()
    except rospy.ROSInterruptException:
        pass
