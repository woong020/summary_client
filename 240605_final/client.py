import socket
import os


# def send_file(host='43.201.91.14', port=8080, signal=b'3'):
#     try:
#         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         client_socket.connect((host, port))
#         file_path = r'scan.jpg'
#
#         client_socket.send(signal)
#
#         with open(file_path, 'rb') as f:
#             data = f.read(1024)
#             while data:
#                 client_socket.sendall(data)
#                 data = f.read(1024)
#
#         # 파일 전송 완료 후 EOF 신호를 보내기
#         client_socket.shutdown(socket.SHUT_WR)
#
#         response = client_socket.recv(1024).decode('utf-8')
#         client_socket.close()
#         print(response)
#         return response == 'complete'
#     except Exception as e:
#         print(f"Error: {e}")
#         return False

def send_file(host='43.201.91.14', port=8080, signal=b'3'):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        file_path = r'scan.jpg'

        client_socket.send(signal)

        with open(file_path, 'rb') as f:
            data = f.read(1024)
            while data:
                client_socket.sendall(data)
                data = f.read(1024)

        # 파일 전송 완료 후 EOF 신호를 보내기
        client_socket.shutdown(socket.SHUT_WR)

        response = client_socket.recv(1024).decode('utf-8')
        client_socket.close()
        print(response)
        return response
    except Exception as e:
        print(f"Error: {e}")
        return str(e)

def send_file1():
    return send_file(signal=b'3')


def send_file2():
    return send_file(signal=b'4')


def send_file3():
    return send_file(signal=b'5')


def send_delete_signal(host='43.201.91.14', port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.send(b'1')

    response = client_socket.recv(1024).decode('utf-8')
    print(f"Server response: {response}")


def receive_all(socket, buffer_size):
    data = bytearray()
    while True:
        part = socket.recv(buffer_size)
        if not part:
            break
        data.extend(part)
        if len(part) < buffer_size:
            break
    return data


def send_summary_signal(host='43.201.91.14', port=8080):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        client_socket.send(b'7')
        buffer_size = 1024
        response = receive_all(client_socket, buffer_size).decode('utf-16')
        client_socket.close()
        return response
    except Exception as e:
        print(f"Error: {e}")
        return False


def send_test_signal(host='43.201.91.14', port=8080):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(b'9')
    response = client_socket.recv(1024).decode('utf-8')
    return response