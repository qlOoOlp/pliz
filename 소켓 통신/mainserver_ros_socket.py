import socket

def send_ros_command(command):
    # ROS 노드의 IP 주소와 포트 번호
    ros_ip = 'localhost'  # ROS 노드의 IP 주소
    ros_port = 9090  # ROS 노드의 포트 번호

    # 소켓 생성
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # ROS 노드에 연결
        sock.connect((ros_ip, ros_port))
        
        # 명령 전송
        sock.sendall(command.encode('utf-8'))
        
        # 응답 받기
        response = sock.recv(1024)
        
        # 응답 처리
        print('응답:', response.decode('utf-8'))
        
    finally:
        # 소켓 닫기
        sock.close()

# 명령 전송 예제
command = 'move_robot'  # ROS 노드로 보낼 명령
send_ros_command(command)
