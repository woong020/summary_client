import socket
import os


def send_file1(host='43.201.91.14', port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    file_path = r'/root/project/summary/scan.jpg'  # 전송할 파일의 경로를 설정

    # 신호 전송: 파일 전송 신호 (3)
    client_socket.send(b'3')

    # 파일명과 확장자 분리
    file_name = os.path.basename(file_path)
    file_name_bytes = file_name.encode('utf-8')
    file_name_length = len(file_name_bytes)

    # 파일명 길이를 먼저 전송
    client_socket.send(file_name_length.to_bytes(4, 'big'))
    # 파일명 전송
    client_socket.send(file_name_bytes)

    with open(file_path, 'rb') as f:
        data = f.read(1024)
        while data:
            client_socket.sendall(data)
            data = f.read(1024)

    print("File sent successfully.")
    client_socket.close()

def send_file2(host='43.201.91.14', port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    file_path = r'/root/project/summary/scan.jpg'  # 전송할 파일의 경로를 설정

    # 신호 전송: 파일 전송 신호 (3)
    client_socket.send(b'4')

    # 파일명과 확장자 분리
    file_name = os.path.basename(file_path)
    file_name_bytes = file_name.encode('utf-8')
    file_name_length = len(file_name_bytes)

    # 파일명 길이를 먼저 전송
    client_socket.send(file_name_length.to_bytes(4, 'big'))
    # 파일명 전송
    client_socket.send(file_name_bytes)

    with open(file_path, 'rb') as f:
        data = f.read(1024)
        while data:
            client_socket.sendall(data)
            data = f.read(1024)

    print("File sent successfully.")
    client_socket.close()

def send_file3(host='43.201.91.14', port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    file_path = r'/root/project/summary/scan.jpg'  # 전송할 파일의 경로를 설정

    # 신호 전송: 파일 전송 신호 (3)
    client_socket.send(b'5')

    # 파일명과 확장자 분리
    file_name = os.path.basename(file_path)
    file_name_bytes = file_name.encode('utf-8')
    file_name_length = len(file_name_bytes)

    # 파일명 길이를 먼저 전송
    client_socket.send(file_name_length.to_bytes(4, 'big'))
    # 파일명 전송
    client_socket.send(file_name_bytes)

    with open(file_path, 'rb') as f:
        data = f.read(1024)
        while data:
            client_socket.sendall(data)
            data = f.read(1024)

    print("File sent successfully.")
    client_socket.close()


def send_delete_signal(host='43.201.91.14', port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # 신호 전송: 파일 삭제 신호 (1)
    client_socket.send(b'1')

    # 서버의 응답 메시지 수신
    response = client_socket.recv(1024).decode('utf-8')
    print(f"Server response: {response}")

def receive_all(socket, buffer_size):
    data = bytearray()
    while True:
        part = socket.recv(buffer_size)
        if not part:
            break
        data.extend(part)
        # Here we can check if we've received the expected length of data
        # if we know the length in advance. Assuming we receive all data if
        # the incoming part is less than the buffer size.
        if len(part) < buffer_size:
            break
    return data

def send_summary_signal(host='43.201.91.14', port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(b'7')
    buffer_size = 1024  # or other suitable size
    response = receive_all(client_socket, buffer_size).decode('utf-16')
    print(response)
    return response

def send_test_signal(host='43.201.91.14', port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # 신호 전송: 테스트 신호 (9)
    client_socket.send(b'9')

    # 서버의 응답 메시지 수신
    response = client_socket.recv(1024).decode('utf-8')
    return response

