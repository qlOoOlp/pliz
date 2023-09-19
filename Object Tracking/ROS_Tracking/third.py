from geometry_msgs.msg import Twist
from second2 import ImageProcessor
"""
C. second 코드에서 리턴한 거리값을 가져와 서버(우분투)에서 터틀봇으로 지정된 명령을 보내는 코드:

터틀봇에게 명령을 보내기 위해서는 ROS2 메시지를 publish하면 됩니다. 
일반적으로 터틀봇은 geometry_msgs/Twist 메시지를 이용하여 제어합니다.
"""

class CommandSender(Node):
    def __init__(self):
        super().__init__('command_sender')

        self.image_processor = ImageProcessor()

        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription_ = self.create_subscription(Point, 'tracked_object_distance', self.listener_callback,
                                                      qos_profile_sensor_data)
        self.target_distance = None

    def listener_callback(self, msg):
        self.target_distance = msg.z

        # timer_period = 0.5  # seconds
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i = 0

    def timer_callback(self):
        msg = Twist()
        target_distance = self.image_processor.distance

        # Go forward if target_distance is more than 0.3m
        # Go backward if target_distance is less than 0.3m
        if target_distance > 0.3:
            msg.linear.x = 0.1
        elif target_distance < 0.3:
            msg.linear.x = -0.1

        self.publisher_.publish(msg)
        self.get_logger().info('Sending command: "%s"' % msg.linear.x)
