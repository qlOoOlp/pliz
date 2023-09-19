import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from geometry_msgs.msg import Point
import cv2

from deep_sort import nn_matching
from deep_sort.tracker import Tracker
from deep_sort.detection import Detection
from tools import generate_detections as gdet

class ImageProcessor(Node):
    def __init__(self):
        super().__init__('image_processor')

        # Initialize deep sort
        max_cosine_distance = 0.2
        nn_budget = 100
        model_filename = 'deep_sort_model/mars-small128.pb'
        metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
        self.encoder = gdet.create_box_encoder(model_filename, batch_size=1)
        self.tracker = Tracker(metric)

        # Initialize cv_bridge
        self.cv_bridge = CvBridge()

        # Create a publisher
        self.distance_publisher = self.create_publisher(Point, 'tracked_object_distance', 10)

        self.distance = None

        # Create a subscription to depth images
        self.subscription = self.create_subscription(
            Image,
            '/camera/depth/image_rect_raw',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        # Convert the ROS Image message to a cv::Mat
        cv2_img = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

        # Get bounding box for object of interest
        bbox, _ = self.encoder(cv2_img)

        # Format the bounding box
        bbox_xywh = self.format_bbox(bbox)

        # Perform deep sort tracking
        detections = [Detection(bbox_xywh[i], 1.0, cv2_img) for i in range(len(bbox_xywh))]

        # Update the tracker based on the new detections
        self.tracker.predict()
        self.tracker.update(detections)

        # Publish the distance of each tracked object
        for track in self.tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue

            bbox = track.to_tlbr()
            centroid = [(bbox[0]+bbox[2])/2, (bbox[1]+bbox[3])/2]
            distance = self.calculate_distance(cv2_img, centroid)
            self.distance = distance

            # Publish the distance
            distance_msg = Point()
            distance_msg.x = centroid[0]
            distance_msg.y = centroid[1]
            distance_msg.z = distance
            self.distance_publisher.publish(distance_msg)

    def format_bbox(self, bbox):
        bbox_xywh = []
        for box in bbox:
            x1, y1, x2, y2 = box
            w = x2 - x1
            h = y2 - y1
            bbox_xywh.append([x1, y1, w, h])

        return bbox_xywh

    def calculate_distance(self, image, centroid):
        # Replace with your depth calculation here
        depth = image[int(centroid[1]), int(centroid[0])]  # Example: Get depth from image at centroid position
        distance = depth * 0.001  # Convert depth from millimeters to meters
        return distance

def main(args=None):
    rclpy.init(args=args)

    image_processor = ImageProcessor()

    rclpy.spin(image_processor)

    image_processor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
