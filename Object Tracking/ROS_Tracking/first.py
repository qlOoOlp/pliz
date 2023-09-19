"""
A. Realsense depth camera 영상 데이터를 서버(우분투)로 전송하는 코드:

먼저, Intel Realsense camera에서 데이터를 가져와서 ROS2 토픽에 publish하는 방법에 대해 설명하겠습니다.
Intel Realsense SDK2.0이 설치되어 있어야 하며, Intel Realsense ROS wrapper가 필요합니다.

다음은 Intel Realsense camera를 사용하여 depth image를 publish하는 node의 예입니다.
"realsense2_camera" 패키지에서 "rs_camera" 노드를 실행하면 됩니다.

터미널에서 다음 명령어를 실행하여 ROS 노드를 시작합니다:


이 코드는 realsense camera를 실행하고 모든 가능한 데이터 스트림을 ROS 토픽으로 publish합니다.
depth image는 "/camera/depth/image_rect_raw" 토픽에서 찾을 수 있습니다.
"""

# ros2 run realsense2_camera rs_camera
# run realsense2_camera realsense2_camera_node