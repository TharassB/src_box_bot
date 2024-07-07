#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class ApplyTwist(Node):
    def __init__(self):
        super().__init__('apply_twist')
        self.publisher_ = self.create_publisher(Twist, '/my_cube/twist', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.twist = Twist()
        self.twist.angular.y = 100.0  # Apply an angular velocity around the y-axis

    def timer_callback(self):
        self.publisher_.publish(self.twist)

def main(args=None):
    rclpy.init(args=args)
    node = ApplyTwist()
    rclpy.spin(node)
  
    rclpy.shutdown()

if __name__ == '__main__':
    main()
