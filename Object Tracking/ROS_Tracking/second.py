import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from deep_sort_pytorch.deep_sort import DeepSort

"""
B. 터틀봇으로부터 받은 데이터를 처리하고 deepsort 알고리즘 적용 후, 
타겟과의 거리를 return하는 코드:

bot1로부터 영상 데이터를 받아서 Deep SORT 알고리즘을 적용하려면, 
해당 알고리즘을 구현한 코드가 있어야 합니다. 여기서는 deep_sort_pytorch 패키지를 사용하겠습니다.
"""

class ImageProcessor(Node):
    def __init__(self):
        super().__init__('image_processor')
        self.subscription = self.create_subscription(
            Image,
            '/camera/depth/image_rect_raw',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.cv_bridge = CvBridge()
        self.deepsort = DeepSort("deep_sort_pytorch/ckpts/ckpt.t7")

    def listener_callback(self, msg):
        # Convert the ROS Image message to a cv::Mat.
        cv2_img = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

        # Apply deepsort algorithm
        bbox_xywh, cls_conf, cls_ids = self.deepsort(cv2_img)

        # TODO: Calculate the distance of the specific target and return
        target_distance = 0
        return target_distance

def main(args=None):
    rclpy.init(args=args)

    image_processor = ImageProcessor()

    rclpy.spin(image_processor)

    image_processor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
