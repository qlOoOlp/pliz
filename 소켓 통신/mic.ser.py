import socket

# 소켓 설정
host = '192.168.0.41'  # 클라이언트의 IP 주소
port = 50001
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(1)
    print('서버 시작')

    conn, addr = s.accept()
    print('클라이언트 접속:', addr)

    while True:
        data = conn.recv(1024)  # 버퍼 크기
        if not data:
            break
        text = data.decode()
        print('Received Text:', text)

    conn.close()
