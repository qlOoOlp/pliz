import socket
import pyaudio
import sys
import threading
import speech_recognition as sr

# 음성 출력 설정
RATE = 44100
CHANNELS = 1
FORMAT = pyaudio.paInt16
O_DEVICE_INDEX = 0  # 스피커 장치 인덱스 (마이크 정보를 확인하여 변경해야 함)
I_DEVICE_INDEX = 2  # 마이크 장치 인덱스 (마이크 정보를 확인하여 변경해야 함)
CHUNK = 1024

# 소켓 설정
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s1:
        print('클라이언트 시작')
        host = '192.168.0.41'
        port = 50001
        s.connect((host, port))
        s1.connect((host, port))
        print('서버 접속')

        # 오디오 스트림 설정
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=I_DEVICE_INDEX)
        stream.start_stream()

        # 음성 인식 설정
        r = sr.Recognizer()

        def speaker_thread():
            while True:
                # 소켓으로부터 데이터 수신
                data = s.recv(8192)  # 버퍼 크기
                # 데이터 출력
                stream.write(data)

        t1 = threading.Thread(target=speaker_thread)
        t1.start()

        while True:
            # 음성 데이터 받기
            audio_data = stream.read(CHUNK)

            # 음성 인식
            try:
                text = r.recognize_google(audio_data)
                print("Recognized Text:", text)

                # 텍스트를 소켓으로 전송
                s1.sendall(text.encode())
            except sr.UnknownValueError:
                print("Unable to recognize speech")

        # 스트림 정리
        stream.stop_stream()
        stream.close()
        p.terminate()
