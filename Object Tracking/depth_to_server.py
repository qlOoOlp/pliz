import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

class DepthSubscriber(Node):
    def __init__(self):
        super().__init__('depth_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/camera/depth/image_rect_raw',
            self.depth_callback,
            10
        )

    def depth_callback(self, msg):
        # 이미지의 가로, 세로 크기
        width = msg.width
        height = msg.height

        # 특정 픽셀 좌표 설정 (예: (x, y) = (320, 240))
        x = 320
        y = 240

        # 픽셀 좌표에 대한 인덱스 계산
        index = (y * width) + x

        # 깊이 데이터 추출
        depth_data = msg.data[index]

        # 깊이 데이터를 실제 거리로 변환 (예시: 16-bit 이미지에서 거리 변환)
        depth_scale = 0.001  # D435i의 경우, 1mm에 해당하는 값을 가짐
        distance = depth_data * depth_scale

        # 거리 출력
        self.get_logger().info(f"거리: {distance}m")

def main(args=None):
    rclpy.init(args=args)
    depth_subscriber = DepthSubscriber()
    rclpy.spin(depth_subscriber)
    depth_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()