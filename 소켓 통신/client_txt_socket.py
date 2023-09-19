import socket

# 서버의 IP 주소와 포트 번호
server_ip = '192.168.0.100'
server_port = 50001

# 서버에 전송할 텍스트 메시지
message = 'docking'

# 서버와의 연결 설정
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# 텍스트 메시지를 서버로 전송
client_socket.sendall(message.encode())

# 서버로부터의 응답 수신
response = client_socket.recv(1024).decode()

# 응답 출력
print('Server response:', response)

# 연결 종료
client_socket.close()
