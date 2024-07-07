#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Wrench, Vector3
import sys
import select
import termios
import tty

def getKey(settings):
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class WrenchController(Node):
    def __init__(self):
        super().__init__('wrench_controller')
        self.publisher_ = self.create_publisher(Wrench, '/my_cube/wrench', 10)
        self.get_logger().info("Press 'k' to topple front, 'l' to topple back, 'q' to quit")

    def apply_wrench(self, direction):
        wrench_msg = Wrench()
        torque = Vector3()

        if direction == 'front':
            torque.y = 25000000000.0  # Adjust this value to control the torque magnitude
        elif direction == 'back':
            torque.y = -2500000000.0  # Adjust this value to control the torque magnitude

        wrench_msg.torque = torque
        self.publisher_.publish(wrench_msg)
        self.get_logger().info("Applied torque: %s" % str(wrench_msg))

def main(args=None):
    rclpy.init(args=args)
    settings = termios.tcgetattr(sys.stdin)
    wrench_controller = WrenchController()

    try:
        while rclpy.ok():
            key = getKey(settings)
            if key == 'k':
                wrench_controller.apply_wrench('front')
            elif key == 'l':
                wrench_controller.apply_wrench('back')
            elif key == 'q':
                break
    except Exception as e:
        print(e)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        wrench_controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
