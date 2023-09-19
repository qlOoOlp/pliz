import socket

# 서버의 IP 주소와 포트 번호
server_ip = '192.168.0.100'
server_port = 50001

# 서버 소켓 생성 및 바인딩
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))

# 클라이언트의 연결 대기
server_socket.listen(1)
print('Waiting for a client connection...')

# 클라이언트와의 연결 수락
client_socket, client_address = server_socket.accept()
print('Client connected:', client_address)

# 클라이언트로부터의 메시지 수신
message = client_socket.recv(1024).decode()
print('Received message:', message)

# 클라이언트에 응답 전송
response = 'docking'
client_socket.sendall(response.encode())

# 연결 종료
client_socket.close()
server_socket.close()
