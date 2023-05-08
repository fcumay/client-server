import socket
import os
import argparse
from loguru import logger
logger.add("debugclient.log", format="{time} {level} {message}", level="DEBUG")
parser = argparse.ArgumentParser(description='Client for sending GET and POST requests.')
parser.add_argument('--host', type=str, required=True, help='Server host')
parser.add_argument('-p', '--port', type=int, required=True, help='Server port')
parser.add_argument('-f', '--file', type=str, required=True, help='File name')
parser.add_argument('-m', '--method', type=str, choices=['GET', 'POST', 'OPTIONS'], required=True, help='HTTP method')
parser.add_argument('-c', '--content', type=str, help='File content to send with POST request')

args = parser.parse_args()

HOST = args.host  # ip адрес сервера
PORT = args.port  # порт сервера


def send_get_request(filename):
    """Отправляет GET запрос"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((HOST, PORT))
        request = f"GET /{filename} HTTP/1.1\r\nHost: {HOST}:{PORT}\r\n\r\n".encode('utf-8')
        server.sendall(request)
        response = b''
        while True:
            data = server.recv(1024)
            if not data:
                break
            response += data
        headers, body = response.split(b'\r\n\r\n', 1)
        return headers, body


def send_post_request(path, file_content):
    """Отправляет POST запрос"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((HOST, PORT))
        headers = f"POST /{path} HTTP/1.1\r\nHost: {HOST}:{PORT}\r\nContent-Length: {len(file_content)}\r\n\r\n"
        request = bytes(headers.encode('utf-8')) + file_content.encode('utf-8')
        server.sendall(request)
        response = server.recv(1024)
        logger.info(f'Response: {response.decode()}')


def send_options_request():
    """Отправляет OPTIONS запрос"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.connect((HOST, PORT))
        request = f"OPTIONS * HTTP/1.1\r\nHost: {HOST}:{PORT}\r\n\r\n".encode('utf-8')
        server.sendall(request)
        response = b''
        while True:
            data = server.recv(1024)
            if not data:
                break
            response += data
        headers, _ = response.split(b'\r\n\r\n', 1)
        return headers


def get_file_content(filename):
    """Получает тело файла с сервера"""
    headers, body = send_get_request(filename)
    return body



def get_text_file_content(filename):
    """Получает тело текстового файла с сервера"""
    content = get_file_content(filename)
    return content.decode('cp1251')



def get_binary_file_content(filename):
    """Получает тело бинарного файла с  сервера"""
    return get_file_content(filename)


def get_file_content_by_type(filename):
    _, file_extension = os.path.splitext(filename)
    if file_extension == '.txt':
        return get_text_file_content(filename)
    else:
        return get_binary_file_content(filename)


if __name__ == '__main__':
    file_content = ''
    if args.method == 'OPTIONS':
        headers = send_options_request()
        logger.info(headers.decode())
    elif args.method == 'POST':
        if args.content:
            file_content = args.content
        send_post_request(args.file, file_content)
    elif args.method == 'GET':
        file_content = get_file_content_by_type(args.file)
        logger.info(f'\n{file_content}')

# python client1.py --host 127.0.0.1 --port 7000 --file hello.txt --method POST --content "Hello, world!"
# python client1.py --host 127.0.0.1 --port 7000 --file 1.txt --method GET
# python client1.py --host 127.0.0.1 -p 7000 -f 1.txt -m GET
# python client1.py --host 127.0.0.1 -p 7000 -f 1.txt -m OPTIONS

# python3 client1.py --host 192.168.100.77 -p 7000 -f 1.txt -m GET