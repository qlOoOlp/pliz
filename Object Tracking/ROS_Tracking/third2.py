import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point
from rclpy.qos import QoSProfile

class CommandSender(Node):
    def __init__(self):
        super().__init__('command_sender')

        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription_ = self.create_subscription(Point, 'tracked_object_distance', self.listener_callback, QoSProfile(depth=10))
        self.target_distance = None

    def listener_callback(self, msg):
        self.target_distance = msg.z
        self.send_command()

    def send_command(self):
        if self.target_distance is not None:
            msg = Twist()

            # Go forward if target_distance is more than 0.3m
            # Go backward if target_distance is less than 0.3m
            if self.target_distance > 0.3:
                msg.linear.x = 0.1
            elif self.target_distance < 0.3:
                msg.linear.x = -0.1

            self.publisher_.publish(msg)
            self.get_logger().info('Sending command: "%s"' % msg.linear.x)

def main(args=None):
    rclpy.init(args=args)

    command_sender = CommandSender()

    rclpy.spin(command_sender)

    command_sender.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
